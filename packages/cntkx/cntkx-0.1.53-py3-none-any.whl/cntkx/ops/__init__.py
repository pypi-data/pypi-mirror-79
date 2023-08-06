import cntk as C
import numpy as np
from . import sequence
from . import random
from cntk.layers.blocks import _inject_name


##########################################################################
# non_diff ops
##########################################################################
@C.typemap
def floor_division(left, right, name=''):
    """ Computers the element-wise floor division. Behaves like // operator in python.

    Examples:
        a = C.constant([-3, 1, 2, 3, 4])
        b = C.constant([2, 2, 2, 2, 2])

        desired = [-2, 0, 1, 1, 2]
        result = Cx.floor_division(a, b).eval().tolist()
        assert result == desired

    Arguments:
        left: left side tensor
        right: right side tensor
        name (str, optional): the name of the Function instance in the network

    Returns:
        :class:`~cntk.ops.functions.Function`
    """

    @C.BlockFunction('FloorDivision', name)
    def inner(x, y):
        quotient = C.element_divide(x, y)
        integers = C.floor(quotient)
        return integers

    return inner(left, right)


##########################################################################
# linear ops
##########################################################################
def split(x, n: int, name=""):
    """ Split tensor `x` into n equal tensors. Dimensions of `x` must be divisible by `n`

    Examples:
        a = C.input_variable(9)
        b, c, d = Cx.split(a, 3).outputs

        assert b.shape == c.shape == d.shape == (9 // 3, )

    Arguments:
        x: input tensor, must be flattened (i.e. single dimension axis)
        n: number of groups to split tensor into
        name (str, optional): the name of the Function instance in the network

    Returns:
        :class:`~cntk.ops.functions.Function`

    """

    @C.BlockFunction('Split', name)
    def inner(a):
        b = C.reshape(a, (n, -1))
        return tuple(C.squeeze(b[i]) for i in range(n))

    return inner(x)


def remainder(left, right, name=''):
    """ Computes the element-wise remainder of division. Behaves like % operator in python.

    Examples:
        x = [-3, 1, 2, 3, 4, 3]
        y = [2, 2, 2, 2, 2, -2]
        a = C.constant(x)
        b = C.constant(y)

        desired = [i % j for i, j in zip(x, y)]  # [1, 1, 0, 1, 0, -1]
        result = Cx.remainder(a, b).eval().tolist()
        assert result == desired

    Arguments:
        left: left side tensor
        right: right side tensor
        name (str, optional): the name of the Function instance in the network

    Returns:
        :class:`~cntk.ops.functions.Function`

    """

    @C.BlockFunction('Remainder', name)
    def inner(x, y):
        quotient = C.element_divide(x, y)
        integers = C.floor(quotient)
        decimals = quotient - integers
        remaining_value = decimals * y
        return remaining_value

    return inner(left, right)


def scalar(x, name=''):
    """ select first element of x with shape (1,)

    Arguments:
        x: input tensor

    Returns:
        :class:`~cntk.ops.functions.Function`
        a scalar of shape (1,)
    """
    @C.BlockFunction('scalar', name)
    def inner(a):
        return C.slice(C.reshape(a, (-1,)), 0, 0, 1)

    return inner(x)


def cumsum(x, axis: int = -1):
    """ Calculates the cumulative sum across a static axis

    Arguments:
        x: input tensor
        axis (int): static axis of tensor to cumsum over

    Returns:
        :class:`~cntk.ops.functions.Function`
    """
    d = x.shape[axis]
    u = C.constant(np.triu(np.ones((d, d))).astype(x.dtype))
    if axis != -1:
        x = C.swapaxes(x, -1, axis)
    z = C.times(x, u)
    if axis != -1:
        z = C.swapaxes(z, -1, axis)
    return z


def batchmatmul(left, right, output_rank=1, infer_input_rank_to_map=C.TIMES_NO_INFERRED_INPUT_RANK, name=''):
    """ Batch Matrix Multiplication

    The output of this operation is the matrix product of the two input batch matrices.

    This implementation is similar to tensorflow.matmul.

    Currently assumes the first axis to be the static batch axis. Does not accept multiple static batch axis.

    Example:
        a = C.sequence.input_variable((3, 4, 5))     # batch matrix
        b = C.sequence.input_variable((3, 5, 6))     # batch matrix
        c = Cx.batchmatmul(a, b)
        assert c.shape == (3, 4, 6)                  # 3 is treated as a batch axis


        a = C.sequence.input_variable((3, 4, 5))     # batch matrix
        b = C.sequence.input_variable((3, 5, 6, 7))  # batch tensor
        c = Cx.batchmatmul(a, b, output_rank=2)
        assert c.shape == (3, 4, 6, 7)               # 3 is treated as a batch axis


        a = C.input_variable((3, 4, 5))              # batch matrix
        b = C.input_variable((3, 5, 6, 7))           # batch tensor
        c = Cx.batchmatmul(a, b, output_rank=2)
        assert c.shape == (3, 4, 6, 7)


    Arguments:
        left: left side matrix or tensor
        right: right side matrix or tensor
        output_rank (int): in case we have tensors as arguments, output_rank represents
            the number of axes to be collapsed in order to transform the tensors
            into matrices, perform the operation and then reshape back (explode the axes)
        infer_input_rank_to_map (int): meant for internal use only. Always use default value
        name (str, optional): the name of the Function instance in the network

    Returns:
        :class:`~cntk.ops.functions.Function`
    """

    left_shape = left.shape
    right_shape = right.shape

    seq_axis_present = len(left.dynamic_axes) == 2
    static_batch_axis = left_shape[0]  # assumes the first axis to be the static batch axis.

    if left_shape[0] != right_shape[0]:
        raise ValueError("first axis of left operand and right operand must be the same")

    if (left_shape[0] < 0 or right_shape[0] < 0) and seq_axis_present:
        raise ValueError("Static batch axis cannot be a free axis when dynamic sequence axis is also present")

    # Combine dynamic sequence axis and static batch axis
    if not seq_axis_present:
        left_unpacked = left
        right_unpacked = right
    else:
        left_unpacked = C.sequence.unpack(left, padding_value=0, no_mask_output=True)
        right_unpacked = C.sequence.unpack(right, padding_value=0, no_mask_output=True)

        left_unpacked = C.reshape(left_unpacked, (-1,) + left_shape[1:])
        right_unpacked = C.reshape(right_unpacked, (-1,) + right_shape[1:])

    # Fold static batch axis into dynamic sequence axis
    left_folded = C.to_sequence(left_unpacked)  # do not set sequence length as batch axis has been folded in
    right_folded = C.to_sequence_like(right_unpacked, left_folded)  # seq_length / axis set here to tell cntk they have the same seq axis

    # Matrix Multiply when no static batch axis is present
    result = C.times(left_folded, right_folded, output_rank=output_rank, infer_input_rank_to_map=infer_input_rank_to_map)

    # Split dynamic sequence axis back to original dynamic sequence and static batch axis
    result_unpacked = C.sequence.unpack(result, padding_value=0, no_mask_output=True)
    if not seq_axis_present:
        result_packed = C.reshape(result_unpacked, (static_batch_axis, ) + result.shape)
    else:
        result_unfolded = C.reshape(result_unpacked, (-1, static_batch_axis) + result.shape)
        result_packed = C.to_sequence_like(result_unfolded, left)

    return _inject_name(result_packed, name)


def upsample(x, factor: int):
    """ Up sample image by a factor of 2 using nearest neighbour.

    Example:
        a = C.input_variable((3, 32, 32)
        b = UpSampling2D(a)

        assert b.shape == (3, 64, 64)

    Arguments:
        x: input image tensor, assumed (channel, row, col)

    Returns:
        :class:`~cntk.ops.functions.Function`

    """
    # old implementation for upsample by factor 2
    # xr = C.reshape(x, (x.shape[0], x.shape[1], 1, x.shape[2], 1))
    # xx = C.splice(xr, xr, axis=-1)  # axis=-1 refers to the last axis
    # xy = C.splice(xx, xx, axis=-3)  # axis=-3 refers to the middle axis
    # r = C.reshape(xy, (x.shape[0], x.shape[1] * 2, x.shape[2] * 2))

    xx = C.splice(*[x for __ in range(factor * 2)], axis=0)
    r = C.depth_to_space(xx, factor)
    return r


def centre_crop(larger_image, smaller_image, name: str = ''):
    """ Centre crop spatial dimensions only.

    Arguments:
        larger_image: class:`~cntk.ops.functions.Function` that outputs the tensor to be centre cropped
        smaller_image: class:`~cntk.ops.functions.Function` that outputs the reference tensor
        name (str, optional): the name of the Function instance in the network

    Returns:
        :class:`~cntk.ops.functions.Function`

    """
    input_shape = larger_image.shape  # larger
    referent_shape = smaller_image.shape  # smaller
    row_offset = int((input_shape[1] - referent_shape[1]) / 2)
    col_offset = int((input_shape[2] - referent_shape[2]) / 2)

    if row_offset == 0 and col_offset == 0:
        return larger_image

    elif row_offset < 0 or col_offset < 0:
        raise ValueError(f"offset became negative, check if image was passed correctly. "
                         f"larger image {larger_image.shape}, smaller image {smaller_image.shape}")

    return C.crop_manual(larger_image, smaller_image, row_offset, col_offset, name=name)


def centre_crop_and_splice(larger_image, smaller_image):
    """ Implementation of copy and crop found in UNET architecture.

    Arguments:
        larger_image: to be centre cropped and channel spliced into smaller image
        smaller_image: reference tensor

    Returns:
        :class:`~cntk.ops.functions.Function`

    """
    return C.splice(smaller_image, centre_crop(larger_image, smaller_image), axis=0)


##########################################################################
# non linear and nn ops
##########################################################################
@C.typemap
def swish(x, name=''):
    """ swish activation function first introduced in 'Searching for activation function' by Prajit et al.
    Paper can be found in https://arxiv.org/abs/1710.05941 and https://arxiv.org/abs/1901.02671

    It typically exhibits good performance in a variety of task in vision and nlp problems.
    Can be used as a drop-in replace for relu.
    """

    @C.BlockFunction('Swish', name=name)
    def inner(a):
        return a * C.sigmoid(a)

    return inner(x)


@C.typemap
def mish(x, name=''):
    """ Mish activation function is introduced in 'Mish: A Self Regularized Non-Monotonic Neural Activation Function'
    by Diganta Misra.

    Experiments show that Mish tends to work better than both ReLU and Swish along with other standard
    activation functions in many deep networks across challenging datasets. For instance,
    in Squeeze Excite Net-18 for CIFAR 100 classification, the network with Mish had an increase in
    Top-1 test accuracy by 0.494% and 1.671% as compared to the same network with Swish and ReLU respectively.
    The similarity to Swish along with providing a boost in performance and its simplicity in implementation
    makes it easier for researchers and developers to use Mish in their Neural Network Models.

    This activation function is adopted in Fast ai too. It should be noted that you are trading some
    computation complexity for a small performance boost.

    Minimum of f(x) is observed to be ≈-0.30884 at x≈-1.1924

    Maintainer's note:
        based on testing, the additional computation complexity is minimal.

    For more detail, the paper can be found here 'https://arxiv.org/abs/1908.08681v2'
    """
    @C.BlockFunction('Mish', name=name)
    def inner(a):
        return a * C.tanh(C.softplus(a))

    return inner(x)


@C.typemap
def hardmax(x, axis=-1, name=''):
    """
    This hardmax implementation can be applied on selected axis. Original cntk hardmax can only be applied on all axis.

    If ``axis`` is given as integer, then the hardmax will be computed along that axis.
    If the provided ``axis`` is -1, it will be computed along the last axis. if None, it will be applied to all axes.

    Arguments:
        x: input_tensor
        axis (int or :class:`~cntk.axis.Axis`): axis along which the hardmax operation will be performed
        name (str, optional): the name of the Function instance in the network

    Returns:
        :class:`~cntk.ops.functions.Function`:
    """

    @C.BlockFunction('Hardmax', name=name)
    def inner(a):
        return C.equal(C.reduce_max(a, axis=axis), a)

    return inner(x)


def erf(x, name=''):
    """
    Computes the element-wise error function of `x`:

    The output tensor has the same shape as ``x``.

    This implementation is from the Handbook of Mathematical Functions and
    has error less than 1.5 * 10-7 for all inputs.
    book can be found here 'http://people.math.sfu.ca/~cbm/aands/frameindex.htm'

    """

    # constants
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911

    @C.BlockFunction('Erf', name=name)
    def inner(a):
        not_negative = C.greater_equal(a, 0)
        sign = C.element_select(not_negative, not_negative, -1)

        abs_x = C.abs(a)

        # A&S formula 7.1.26
        t = 1.0 / (1.0 + p * a)
        y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * C.exp(-abs_x * abs_x)
        return C.element_times(sign, y)

    return inner(x)


def gelu(x, name=''):
    """ Gaussian Error Linear Unit (GELU), a high-performing neuralnetwork activation function.
    The GELU nonlinearity is the expected transforma-tion of a stochastic regularizer which randomly
    applies the identity or zero mapto a neuron’s input.  The GELU nonlinearity weights inputs by their
    magnitude,rather than gates inputs by their sign as in ReLUs.

    For more detail please refer to 'Gaussian Error Linear Units (GELU)'
    by Hendrycks and Gimpel (https://arxiv.org/abs/1606.08415)

    This activation is used in BERT and OpenAI GPT & GPT-2.

    Its computationally x2 times slower than relu with some negligible increase in memory footprint.

    Arguments:
        x: input_tensor
        name (str, optional): the name of the Function instance in the network

    Returns:
        :class:`~cntk.ops.functions.Function`:

    """
    @C.BlockFunction('Gelu', name=name)
    def inner(a):
        return 0.5 * a * (1 + erf(a / 1.41421356237))

    return inner(x)


def gelu_fast(x, name=''):
    """ This version is an less good approximation of gelu but it is x2 times faster on GPU and x3.8 faster on CPU.
    This implementation just as fast as relu on GPU but x2 slower on CPU.

    Roughly the same memory footprint as relu.

    Arguments:
        x: input_tensor
        name (str, optional): the name of the Function instance in the network

    Returns:
        :class:`~cntk.ops.functions.Function`:

    """
    @C.BlockFunction('GeluFast', name=name)
    def inner(a):
        return a * C.sigmoid(1.702 * a)

    return inner(x)


def scaled_dot_product_attention(query, key, value, obey_sequence_order: bool = None, max_seq_len: int = None, name=''):
    """
    Scaled dot-product attention implementation of "Attention is all you need", https://arxiv.org/abs/1706.03762

    An attention function can be described as mapping a query and a set of key-value pairs to an output,
    where the query, keys, values, and output are all vectors. The output is computed as a weighted sum
    of the values, where the weight assigned to each value is computed by a compatibility function of the
    query with the corresponding key.

    scaled_dot_product_attention(Q, K, V) = softmax(QV.T / sqrt(dk)) * V

    When query, key and value are all the same, it becomes self-attention.

    Note:
        Query and key must have the same dimension
        Key and value must have the same sequence length

    Example:
        a = C.sequence.input_variable(10)
        b = ScaledDotProductAttention()(a, a, a)

        assert b.shape == (10, )

        obey_sequence_order: do not let attention peek into future values
        max_seq_len: max sequence length possible, used to ensure that sequence order is obeyed

    Returns:
        :class:`~cntk.ops.functions.Function`:
        A function that returns a weighted sum of value

    """

    @C.BlockFunction('ScaledDotProductAttention', name)
    def attention(query, key, value):
        dk = C.sqrt(C.reduce_sum(C.ones_like(query)))  # cannot use sequence.last, will conflict with recurrence
        # dk: [#, *] [1, ] and value = int(dim_of_query)

        unpacked_key = C.sequence.unpack(key, padding_value=0, no_mask_output=True)  # [#] [-3, key_dim]
        unpacked_value = C.sequence.unpack(value, padding_value=0, no_mask_output=True)  # [#] [-3, value_dim]

        broadcasted_key = C.sequence.broadcast_as(unpacked_key, query)  # [#, *] [-3, key_dim]
        scaled = C.times_transpose(query, broadcasted_key) / dk
        # [#, *] [q_dim] @ [#, *] [key_dim, -3], assert q_dim == key_dim
        # scaled: [#, *] [-3, ] => for every key seq element, there is a corresponding score

        # masked out invalid temporal connections to obey_sequence_order
        if obey_sequence_order and max_seq_len:
            unpacked_scaled, scaled_mask = C.sequence.unpack(scaled, padding_value=0).outputs
            # unpacked_scaled: [#] [-3, -3]  <== matrix will be top right diagonally zero-ed
            # scaled_mask: [#] [-3,]

            minus_inf = C.constant(-1e+30)
            valid_connections = C.Constant(np.tril(np.ones((max_seq_len, max_seq_len)), k=0))  # [] [max_seq, max_seq]
            valid_connections = C.reconcile_dynamic_axes(valid_connections, unpacked_scaled)  # [#] [max_seq, max_seq]
            valid_connections = C.crop_manual(valid_connections, unpacked_scaled, 0, 0)  # [#] [-3, -3]
            unpacked_scaled = C.element_select(valid_connections, unpacked_scaled, minus_inf)  # [#] [-3, -3]
            scaled = C.to_sequence_like(unpacked_scaled, query)  # [#, *] [-3]

        elif obey_sequence_order and not max_seq_len:
            raise ValueError("max_seq_len must be defined when obey_sequence_order is True")

        attended = C.times(C.softmax(scaled, axis=-1), C.sequence.broadcast_as(unpacked_value, query))  # [#, *] [value_dim,]
        return attended

    return attention(query, key, value)


##########################################################################
# mixture density network ops
##########################################################################
@C.typemap
def gaussian_mdn_coeff(x, nmix: int, ndim: int):
    """
    Extracts the coefficients for gaussian mixture density network.
    Assumes independence between gaussian dimensions.

    Example:
        ndim, nmix = 1, 3
        a = C.input_variable(ndim)
        prediction = Dense((ndim + 2) * nmix)(a)
        coeffs = C.combine(gaussian_mdn_coeff(prediction_tensor, nmix=nmix, ndim=ndim)).eval({a: x})

        alpha, mu, sigma = coeffs.values()

    Arguments:
        x: input tensor
        nmix (int): number of mixture
        ndim (int): number of dimension of gaussian

    Returns:
        tuple

    """

    if len(x.shape) != 1:
        raise ValueError("Must be a 1d tensor, but input has shape {0}".format(x.shape))

    alpha = C.softmax(C.slice(x, 0, 0, nmix), name='alpha')
    sigma = C.exp(C.slice(x, 0, nmix, 2 * nmix), name='sigma')  # common variance for all components in single gaussian kernel
    mu = C.reshape(C.slice(x, 0,  2 * nmix, (ndim + 2) * nmix), shape=(nmix, ndim), name='mu')
    return alpha, mu, sigma


def sample_gaussian_mdn(prediction_tensor, nmix: int, ndim: int):
    """ Constructs sampling nodes from mixture density network outputs

    Example:
        ndim, nmix = 1, 3
        a = C.input_variable(ndim)
        prediction = Dense((ndim + 2) * nmix)(a)
        sampled = sample_gaussian_mdn(prediction, nmix, ndim)

        results = sampled.eval({a: x})  # different results every time you eval

    Arguments:
        prediction_tensor: input tensor
        nmix (int): number of mixture
        ndim (int): number of dimension of gaussian

    Returns:
        :class:`~cntk.ops.functions.Function`

    """
    alpha_tensor, mu_tensor, sigma_tensor = gaussian_mdn_coeff(prediction_tensor, nmix=nmix, ndim=ndim)

    selected_alpha = random.sample(alpha_tensor)
    selected_mu_tensor = C.reduce_sum(mu_tensor * C.expand_dims(selected_alpha, axis=-1), axis=0)
    selected_sigma_tensor = C.reduce_sum(sigma_tensor * selected_alpha, axis=0)

    sampled = C.random.normal_like(selected_sigma_tensor) * selected_sigma_tensor + selected_mu_tensor
    return sampled
