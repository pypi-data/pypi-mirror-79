from typing import Union

import numpy as np
from src.pysigfig.number import Const, Float


def _type_check_internal(x: Union[Const, Float]):
    """Internal type checking function

    :param x: the object
    :return: None
    """
    if not (isinstance(x, Float) | isinstance(x, Const)):
        raise TypeError("x must be a Float or Const object")


def _log_internal(x: Union[Const, Float], value: float) -> Union[Const, Float]:
    """Internal logarithm function

    :param x: the object
    :param value: the pre-computed logged value
    :return: the new logged object
    """
    if isinstance(x, Float):
        value = float(value)
        new_sf = Float._calc_sf(value, -x.sf)
        return Float(value, new_sf)
    elif isinstance(x, Const):
        return Const(value)
    else:
        raise TypeError("x must be a Float or Const object")


def _exp_internal(base: Union[Const, Float], expo: Float) -> Union[Const, Float]:
    """Internal exponentiation helper

    :param base: The base of the exponent
    :param expo: The exponent
    :return: The resulting number
    """
    if isinstance(expo, Float):
        return base ** expo
    else:
        raise TypeError("exponent must be a Float object")


def log(x: Union[Const, Float]) -> Union[Const, Float]:
    """Natural logarithm

    :param x: value to be logged
    :return: the result
    """
    _type_check_internal(x)
    return _log_internal(x, np.log(x.v))


def ln(x: Union[Const, Float]) -> Union[Const, Float]:
    """Natural logarithm

    :param x: value to be logged
    :return: the result
    """
    _type_check_internal(x)
    return _log_internal(x, np.log(x.v))


def log10(x: Union[Const, Float]) -> Union[Const, Float]:
    """Base 10 logarithm

    :param x: value to be logged
    :return: the result
    """
    _type_check_internal(x)
    return _log_internal(x, np.log10(x.v))


def log2(x: Union[Const, Float]) -> Union[Const, Float]:
    """Base 2 logarithm

    :param x: value to be logged
    :return: the result
    """
    _type_check_internal(x)
    return _log_internal(x, np.log2(x.v))


def log1p(x: Union[Const, Float]) -> Union[Const, Float]:
    """Natural logarithm of 1 plus x

    :param x: value to be logged
    :return: the result
    """
    _type_check_internal(x)
    return _log_internal(x, np.log1p(x.v))


def exp(x: Union[Const, Float]) -> Union[Const, Float]:
    """Exponential

    :param x: Exponent value
    :return: the result
    """
    _type_check_internal(x)
    return _exp_internal(Const(np.exp(1.0)), x)


def exp2(x: Union[Const, Float]) -> Union[Const, Float]:
    """Base 2 Exponential

    :param x: Exponent value
    :return: the result
    """
    _type_check_internal(x)
    return _exp_internal(Const(2.0), x)


def exp10(x: Union[Const, Float]) -> Union[Const, Float]:
    """Base 10 Exponential

    :param x: Exponent value
    :return: the result
    """
    _type_check_internal(x)
    return _exp_internal(Const(10.0), x)
