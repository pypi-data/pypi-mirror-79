import cntk as C
import math
import numpy as np
from typing import List
from cntk.learners import _infer_learning_rate_schedule_and_ref_minibatch_size, _infer_learning_parameter_schedule, _verify_momentum_type
from cntk import cntk_py


class CyclicalLearningRate(object):
    """
    Cyclical learning rate is an implementation to that  practically eliminates
    the need to experimentally find the best values and schedule  for  the
    global  learning  rates.

    Instead  of  monotonically decreasing the learning rate, this method lets the
    learning  rate  cyclically  vary  between  reasonable  boundary  values

    Training  with  cyclical  learning  rates  instead of  fixed  values  achieves
    improved  classification  accuracy without a need to tune and often in fewer iterations.

    This is an CNTK implementation of the following paper:
    Cyclical Learning Rates for Training Neural Networks by Leslie N. Smith: https://arxiv.org/abs/1506.01186

    The policy cycles the learning rate between two boundaries with a constant frequency, as detailed in
    the paper.
    The distance between the two boundaries can be scaled on a per-iteration
    or per-cycle basis.

    Cyclical learning rate policy changes the learning rate after every batch.
    `batch_step` should be called after a batch has been used for training.
    To resume training, save `last_batch_iteration` and use it to instantiate `CyclicalLeaningRate`.

    This class has three built-in policies, as put forth in the paper:
    "triangular":
        A basic triangular cycle w/ no amplitude scaling.
    "triangular2":
        A basic triangular cycle that scales initial amplitude by half each cycle.
    "exp_range":
        A cycle that scales initial amplitude by gamma**(cycle iterations) at each
        cycle iteration.

    This implementation was adapted from the github repo:
    `bckenstler/CLR` and 'anandsaha/pytorch.cyclic.learning.rate'


    Args:
        parameter_learner (learner): list of cntk learner
        base_lr (float or list): Initial learning rate which is the
            lower boundary in the cycle for eachparam groups.
            Default: 0.001
        max_lr (float or list): Upper boundaries in the cycle for
            each parameter group. Functionally,
            it defines the cycle amplitude (max_lr - base_lr).
            The lr at any cycle is the sum of base_lr
            and some scaling of the amplitude; therefore
            max_lr may not actually be reached depending on
            scaling function. Default: 0.006
        ramp_up_step_size (int): Number of training iterations in the
            lr ramp up phase. Authors suggest setting step_size
            2-8 x training iterations in epoch. Default: 2000
        ramp_down_step_size (int): Number of training iterations in the
            lr ramp down phase. If not set, it will take the value of
            ramp_up_step_size making the lr curve symmetric.
        minibatch_size (int): Number of samples in one minibatch
        lr_policy (str): One of {triangular, triangular2, exp_range}.
            Values correspond to policies detailed above.
            If scale_fn is not None, this argument is ignored.
            Default: 'triangular2'
        gamma (float): Constant in 'exp_range' scaling function:
            gamma ** iterations
            Default: 0.99994
        scale_fn (function): Custom scaling policy defined by a single
            argument lambda function, where
            0 <= scale_fn(x) <= 1 for all x >= 0.
            lr_policy is ignored
            Default: None
        scale_by (str): scale by either number of training iterations or training cycles.
            Only used if custom scaling policy scale_fn is defined.
        record_history (bool): If True, loss & learn rate will be recorded. get loss lr
            history functions can then be used.
        last_batch_iteration (int): The index of the last batch. Default: -1
    Example:
     >>> model = C.layers.Dense(10)(C.input_variable(10))
     >>> sgd_momentum = C.momentum_sgd(model.parameters, 0.1, 0.9)
     >>> clr = CyclicalLeaningRate(sgd_momentum, minibatch_size=32)

     >>> for epoch in range(10):
     ...     for batch in range(100):
     ...         # trainer.train_minibatch(...)
     ...         clr.batch_step()  # must be called once for every training iteration/update
    """

    def __init__(self, parameter_learner, base_lr=1e-3, max_lr=6e-3, warm_up_lr: float = 0., warm_up_size: int = 0,
                 ramp_up_step_size: int = 2000, ramp_down_step_size: int = None, minibatch_size=None,
                 lr_policy: str = 'triangular2', gamma: float = 0.99994, scale_fn=None, scale_by: str = None,
                 record_history: bool = False, last_batch_iteration: int = -1):

        if lr_policy not in ['triangular', 'triangular2', 'exp_range'] and scale_fn is None:
            raise ValueError('lr_policy is invalid and scale_fn is None')

        if scale_by is not None and scale_by not in ['iteration', 'cycle']:
            raise ValueError("Can only scale by iteration or cycle")

        if scale_by is not None and scale_fn is None:
            raise ValueError('scale_by can only be used when custom scale function is used')

        self.parameter_learner = parameter_learner
        self.base_lr = base_lr
        self.max_lr = max_lr
        self.warm_up_lr = warm_up_lr or self.base_lr

        self.warm_up_size = warm_up_size
        self.ramp_up_step_size = ramp_up_step_size
        self.ramp_down_step_size = ramp_down_step_size or ramp_up_step_size
        self.cycle_size = self.ramp_up_step_size + self.ramp_down_step_size
        self.minibatch_size = minibatch_size

        self.lr_policy = lr_policy
        self.gamma = gamma
        self.record_history = record_history

        if scale_fn is None:
            if self.lr_policy == 'triangular':
                self.scale_fn = self._triangular_scale_fn
                self.scale_by = 'cycle'
            elif self.lr_policy == 'triangular2':
                self.scale_fn = self._triangular2_scale_fn
                self.scale_by = 'cycle'
            elif self.lr_policy == 'exp_range':
                self.scale_fn = self._exp_range_scale_fn
                self.scale_by = 'iteration'
        else:
            self.scale_fn = scale_fn
            self.scale_by = scale_by

        self.loss = []
        self.lrs: List[float] = []  # [(learn1_lr, ), (learner1_lr, ), ... ]
        self.current_lr = 0
        self.last_batch_iteration = last_batch_iteration
        self.batch_step()

    def _triangular_scale_fn(self, x) -> float:
        return 1.

    def _triangular2_scale_fn(self, x) -> float:
        return 1 / (2. ** (x - 1))

    def _exp_range_scale_fn(self, x) -> float:
        return self.gamma ** x

    def batch_step(self, previous_minibatch_loss=None):
        """
        Updates learners with new learning rate after one training iteration is complete.
        Must be called once for every training iteration/update.
        """

        self.last_batch_iteration += 1
        lr = self.get_lr()
        self.current_lr = lr
        
        # loss and learn rate gets recorded in pre-training mode
        if self.record_history and previous_minibatch_loss:
            self.loss.append(previous_minibatch_loss)
            self.lrs.append(lr)

        self.parameter_learner.reset_learning_rate(C.learning_parameter_schedule(lr, minibatch_size=self.minibatch_size))
        return None

    def get_lr(self) -> float:
        """ Get learning rate based on last_batch_iteration count """
        current_iteration_num = self.last_batch_iteration

        iterations_after_warmup = current_iteration_num
        if current_iteration_num < self.warm_up_size:
            return self.warm_up_lr

        else:
            iterations_after_warmup -= self.warm_up_size

        # Cycle number
        cycle_num: int = math.floor(1 + iterations_after_warmup / self.cycle_size)

        # number of batch steps made since last complete cycle
        iteration_since_last_cycle = iterations_after_warmup % self.cycle_size

        # ramping up or down
        is_ramp_up = True if iteration_since_last_cycle <= self.ramp_up_step_size else False

        num_batch_steps_in_ramp = iteration_since_last_cycle
        if is_ramp_up:
            base_height = (self.max_lr - self.base_lr) * (num_batch_steps_in_ramp / self.ramp_up_step_size)
        else:  # ramp_down
            num_batch_steps_in_ramp = iteration_since_last_cycle - self.ramp_up_step_size
            base_height = (self.max_lr - self.base_lr) * (1 - num_batch_steps_in_ramp / self.ramp_down_step_size)

        # base_height = (self.max_lr - self.base_lr) * max(0., (1 - proportion_of_step_completed))
        xx = cycle_num if self.scale_by == "cycle" else iterations_after_warmup
        lr = self.base_lr + base_height * self.scale_fn(xx)
        return lr

    def get_lr_schedule(self, number_of_cycles=4) -> np.ndarray:
        """ returns how the learn rate schedule will be like. Useful to check if your
        custom learning policy is working as intended.

        The returned lr_schedule can be visualised in the following:
            import matplotlib.pyplot as plt

            plt.scatter(range(lr_schedule.shape[0]), lr_schedule, s=1)
            plt.show()

        Arguments:
            number_of_cycles (int):

        Returns:
            np.ndarray 1-d

        """
        store_last_iteration = self.last_batch_iteration
        self.last_batch_iteration = 0

        lr_schedule = []
        for i in range(number_of_cycles * self.cycle_size):
            lr_schedule.append(self.get_lr())
            self.last_batch_iteration += 1

        self.last_batch_iteration = store_last_iteration
        lr_schedule = np.array(lr_schedule)
        assert lr_schedule.ndim == 1
        return lr_schedule

    def get_loss_lr_history(self) -> np.ndarray:
        assert self.record_history, "Cannot be used outside of pre-training as loss is not captured"
        return np.array([(loss, *lrs) for loss, lrs in zip(self.loss, self.lrs)])

    def get_averaged_loss_lr_history(self, window=100) -> np.ndarray:
        """ Average loss and learn rate value within window size

        Any remainder outside of window size will not be included in the average returned.

        Mean values returned can be visualised in the follow:

            import matplotlib.pyplot as plt
            plt.scatter(mean_loss_lr[1], mean_loss_lr[0], s=1)
            plt.show()

        Using the graph, determine the base_lr and max_lr.

        Base_lr is the smallest lr value that results in loss decreasing.
        Max_lr is the largest lr before loss becomes unstable.

        """
        assert self.record_history, "Cannot be used outside of pre-training as loss is not captured"
        assert window > 0, "window size cannot be zero or smaller"

        history = self.get_loss_lr_history()

        if window > 1:
            remainder = history.shape[0] % window
            if remainder:
                print(f"last {remainder} rows are exlcuded from average calculation")
                history = history[:-remainder, ...]

            history = history.reshape((-1, window, history.shape[1]))
            history = np.mean(history, axis=1)

        return history


def exponential_warmup_schedule(lr: float, tau: float) -> List[float]:
    return [lr * min(1., 1 - math.exp(- 1 / tau * (i + 1))) for i in range(10_000)] + [lr]


def adam_exponential_warmup_schedule(lr: float, beta2: float) -> List[float]:
    return exponential_warmup_schedule(lr, 1 / (1 - beta2))


@C.typemap
def RAdam(parameters, lr, momentum=0.9, unit_gain=C.default_unit_gain_value(),
         beta2=0.999, l1_regularization_weight=0.0, l2_regularization_weight=0.0,
         gaussian_noise_injection_std_dev=0.0, gradient_clipping_threshold_per_sample=np.inf,
         gradient_clipping_with_truncation=True, use_mean_gradient=None, epsilon=1e-8, adamax=False,
         minibatch_size=None, epoch_size=None):
    """ RAdam like implementation using Adam with exponential warmup schedule. No tuning of
    warmup schedule required, unlike Adam.

    This is a simple untuned warmup of Adam with 'rule-of-thumb' warmup schedule that performs
    more-or-less identically to RAdam in typical practical settings based on
    'On the adequacy of untuned warmup for adaptive optimization' by Jerry Ma and Denis Yarats.

    For more details, paper can be found here 'https://arxiv.org/abs/1910.04209'

    Args:
        ... please look at original documentation in cntk.learner.adam
        epoch_size (optional, int): number of samples as a scheduling unit for learning rate, momentum and variance_momentum. See also:  :func:`learning_parameter_schedule`

    Returns:
        :class:`~cntk.learners.Learner`: learner instance that can be passed to
        the :class:`~cntk.train.trainer.Trainer`

    See also:
        [1] D. Kingma, J. Ba. `Adam: A Method for Stochastic Optimization
        <https://arxiv.org/abs/1412.6980>`_. International Conference for
        Learning Representations, 2015.
    """
    if epoch_size is None:
        raise ValueError("epoch size should be set to the number of samples per minibatch "
                         "(i.e. number of samples trained in every training update) so that "
                         "learning rate factor can be updated after every training update")

    lr = adam_exponential_warmup_schedule(lr, beta2)  # rule-of-thumb exponential warmup schedule

    lr, minibatch_size = _infer_learning_rate_schedule_and_ref_minibatch_size(use_mean_gradient, minibatch_size, lr, epoch_size)

    momentum = _infer_learning_parameter_schedule(momentum, minibatch_size, epoch_size)
    _verify_momentum_type(momentum)
    variance_momentum = _infer_learning_parameter_schedule(beta2, minibatch_size, epoch_size)
    _verify_momentum_type(variance_momentum)
    gaussian_noise_injection_std_dev = C.training_parameter_schedule(gaussian_noise_injection_std_dev)

    additional_options = cntk_py.AdditionalLearningOptions()
    additional_options.l1_regularization_weight = l1_regularization_weight
    additional_options.l2_regularization_weight = l2_regularization_weight
    additional_options.gaussian_noise_injection_std_dev = gaussian_noise_injection_std_dev
    additional_options.gradient_clipping_threshold_per_sample = gradient_clipping_threshold_per_sample
    additional_options.gradient_clipping_with_truncation = gradient_clipping_with_truncation
    if minibatch_size is not None:
        additional_options.dict_options[cntk_py.Learner._MINIBATCH_SIZE] = cntk_py.SizeTWrapper(minibatch_size)  # need this to make proper typed DictionaryValue

    opt = cntk_py.adam_learner(parameters, lr, momentum, unit_gain, variance_momentum, epsilon, adamax, additional_options)
    opt.is_minibatch_size_explicitly_specified = minibatch_size is not None
    return opt
