import re
from typing import Optional, Union

import numpy as np


class Number:
    """Base class for both Floats with significant figures and Const"""

    def __init__(self, value: Union[int, float, str]):
        """Initialize Number

        :param value: internal number value
        """
        self.__v = float(value)

    @property
    def v(self):
        """Value Property

        :return: value
        :rtype: float
        """
        return self.__v


class Float(Number):
    """A number with significant figures"""

    @staticmethod
    def __find_largest_lsd(x, y) -> int:
        """Find the largest 'least significant digit' between two Floats

        :param x: fist Float
        :type x: Float
        :param y: second Float
        :type y: Float
        :return: largest least significant digits
        """
        if x.lsd > y.lsd:
            new_lsd = x.lsd
        else:
            new_lsd = y.lsd
        return new_lsd

    @staticmethod
    def __find_smallest_sf(x, y) -> int:
        """Find the smallest significant figures between two Floats

        :param x: first Float
        :type x: Float
        :param y: second Float
        :type y: Float
        :return: smallest significant figures
        """
        if x.sf > y.sf:
            new_sf = y.sf
        else:
            new_sf = x.sf
        return new_sf

    @staticmethod
    def _calc_lsd(value: float, num_sig_figs: int) -> int:
        """Calculate the least significant digit from the value and number of significant figures

        :param value: The Float value
        :param num_sig_figs: the number of significant figures
        :return: the power of 10 of the least significant digit
        """
        return int(np.floor(np.log10(np.abs(value)))) - num_sig_figs + 1

    @staticmethod
    def _calc_sf(value: float, lsd: int) -> int:
        """Calculate the number of significant figures from the value and least significant digit

        :param value: The Float value
        :param lsd: the power of 10 of the least significant digit
        :return: the number of significant figures
        """
        return int(np.floor(np.log10(np.abs(value)))) - lsd + 1

    def __init__(self, value: Union[str, float], num_sig_figs: Optional[int] = None):
        """Initialize a Float

        :param value: the value of the Float
        :param num_sig_figs: the number of significant figures or None
        """
        # super().__init__ checks that the value is convertible to a float
        super().__init__(value)
        if isinstance(value, str) & (num_sig_figs is None):
            # if exponential 2.3450E1223
            # need to help the mypy type checker
            str_value = str(value)
            is_exponential = re.match("[-0-9.]*[Ee][0-9+-]*", str_value)
            if is_exponential:
                new_str = (str_value.split("E"))[0].replace("-", "").replace(".", "")
            else:
                new_str = re.sub("^[0.]*", "", str_value).replace(".", "")
            self.__sf = len(new_str)
            self.__lsd = Float._calc_lsd(self.v, self.__sf)
            rounded_value = np.around(self.v, decimals=-self.__lsd)
            self.__sv = "{0:.{1:d}E}".format(float(rounded_value), (self.__sf - 1))
        elif num_sig_figs is not None:
            # convert to float so that the initialization can handle ints or floats or strings
            self.__sf = int(num_sig_figs)
            self.__lsd = Float._calc_lsd(self.v, self.__sf)
            rounded_value = np.around(self.v, decimals=-self.__lsd)
            self.__sv = "{0:.{1:d}E}".format(float(rounded_value), (self.__sf - 1))
        else:
            raise ValueError("Unexpected Initialization Inputs")

    @property
    def sf(self) -> int:
        """Significant figure property"""
        return self.__sf

    @property
    def lsd(self) -> int:
        """Power of 10 of the least significant digit"""
        return self.__lsd

    @property
    def str(self) -> str:
        """String representation of the number using significant figures"""
        return self.__sv

    def __str__(self):
        return str(
            "%s \t (significant figures = %i) (least significant digit = %g)\n"
            % (self.__sv, self.__sf, (10.0 ** self.__lsd))
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.v}, {self.__sf})"

    def __add__(self, other):
        """Addition"""
        if isinstance(other, Float):
            value = self.v + other.v
            new_lsd = Float.__find_largest_lsd(self, other)
            new_sf = Float._calc_sf(value, new_lsd)
            return Float(value, new_sf)
        elif isinstance(other, Const):
            value = self.v + other.v
            new_lsd = Float._calc_lsd(value, self.__sf)
            new_sf = Float._calc_sf(value, new_lsd)
            return Float(value, new_sf)
        else:
            raise TypeError("only Floats and Const can be added or subtracted in pysigfig")

    def __neg__(self):
        """Negation"""
        value = -1.0 * self.v
        return Float(value, self.__sf)

    def __abs__(self):
        """Absolute Value"""
        value = np.abs(self.v)
        return Float(value, self.__sf)

    def __sub__(self, other):
        """Subtraction"""
        return self + (-other)

    def __mul__(self, other):
        """Mutliplication"""
        if isinstance(other, Float):
            value = self.v * other.v
            new_sf = Float.__find_smallest_sf(self, other)
            return Float(value, new_sf)
        elif isinstance(other, Const):
            value = self.v * other.v
            return Float(value, self.__sf)
        else:
            raise TypeError("only Float and Const can be multiplied or divided in pysigfig")

    def __invert__(self):
        """Inversion"""
        value = 1.0 / self.v
        return Float(value, self.__sf)

    def __truediv__(self, other):
        """Double precision division"""
        return self * (~other)

    @staticmethod
    def __check_type_comparison(x):
        """Check for object type (Internal)"""
        if not isinstance(x, Float):
            raise TypeError("only Float can be compared using comparison operators in pysigfig")

    def __eq__(self, other):
        """Equality"""
        Float.__check_type_comparison(other)
        # Two numbers are the same if their significant digit representations are the same
        return self.__sv == other.str

    def __ne__(self, other):
        """Not Equal"""
        Float.__check_type_comparison(other)
        return self.__sv != other.str

    def __lt__(self, other):
        """Less than"""
        Float.__check_type_comparison(other)
        return (self.v < other.v) & (self.__sv != other.str)

    def __gt__(self, other):
        """Greater than"""
        Float.__check_type_comparison(other)
        return (self.v > other.v) & (self.__sv != other.str)

    def __le__(self, other):
        """Less than or equal to"""
        Float.__check_type_comparison(other)
        return (self.v < other.v) | (self.__sv == other.str)

    def __ge__(self, other):
        """Greater than or equal to"""
        Float.__check_type_comparison(other)
        return (self.v > other.v) | (self.__sv == other.str)

    def __pow__(self, other):
        """Power (**)"""
        if isinstance(other, Const):
            value = self.v ** other.v
            return Float(value, self.__sf)
        elif isinstance(other, int):
            value = self.v ** other
            return Float(value, self.__sf)
        elif isinstance(other, Float):
            # interpretation is that the exponent is the number of times we will
            # multiply the number times iteself
            # even if we are uncertain about the exponent, the sig figs of the base control
            value = self.v ** other.v
            return Float(value, self.__sf)
        else:
            raise TypeError("only Float, Const, and int are accepted as exponents of Floats")

    def __int__(self):
        """Integer conversion"""
        return int(self.v)

    def __float__(self):
        """float conversion"""
        return self.v

    def __iadd__(self, other):
        """Increment by addition"""
        new_float = self + other
        self.__init__(new_float.v, new_float.sf)

    def __imul__(self, other):
        """Increment by multiplication"""
        new_float = self * other
        self.__init__(new_float.v, new_float.sf)

    def __itruediv__(self, other):
        """Increment by division"""
        new_float = self / other
        self.__init__(new_float.v, new_float.sf)

    def __isub__(self, other):
        """Increment by subtraction"""
        new_float = self - other
        self.__init__(new_float.v, new_float.sf)


class Const(Number):
    """An exact number with infinite significant figures"""

    def __init__(self, value: Union[int, float]):
        super().__init__(value)

    def __str__(self):
        return str("%g \t (constant)\n" % self.v)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.v})"

    def __add__(self, other):
        """Addition"""
        if isinstance(other, Float):
            # Const + Float = Float + Const
            return other + self
        elif isinstance(other, Const):
            return Const(self.v + other.v)
        else:
            raise TypeError("Only Const and Float can be added")

    def __neg__(self):
        """Negation"""
        return Const(-1.0 * self.v)

    def __abs__(self):
        """Absolute Value"""
        return Const(np.abs(self.v))

    def __sub__(self, other):
        """Subtraction"""
        if isinstance(other, Float):
            # Const - Float = -Float + Const
            return (-other) + self
        else:
            return self + (-other)

    def __mul__(self, other):
        """Multiplication"""
        if isinstance(other, Float):
            # Const * Float = Float * Const
            return other * self
        elif isinstance(other, Const):
            return Const(self.v * other.v)
        else:
            raise TypeError("Only Const and Float can be multiplied")

    def __invert__(self):
        """Inversion"""
        return Const(1.0 / self.v)

    def __truediv__(self, other):
        """Double precision division"""
        if isinstance(other, Float):
            # Const / Float = (1/Float) * Const
            return (~other) * self
        else:
            return self * (~other)

    @staticmethod
    def __check_type_comparison(x):
        """Type checking for comparison operators"""
        if not isinstance(x, Const):
            raise TypeError("only Const can be compared using comparison operators in pysigfig")

    def __eq__(self, other):
        """Equality"""
        Const.__check_type_comparison(other)
        return self.v == other.v

    def __ne__(self, other):
        """Not equal"""
        Const.__check_type_comparison(other)
        return self.v != other.v

    def __lt__(self, other):
        """Less than"""
        Const.__check_type_comparison(other)
        return self.v < other.v

    def __gt__(self, other):
        """Greater than"""
        Const.__check_type_comparison(other)
        return self.v > other.v

    def __le__(self, other):
        """Less than or Equal to"""
        Const.__check_type_comparison(other)
        return self.v <= other.v

    def __ge__(self, other):
        """Greater than or Equal to"""
        Const.__check_type_comparison(other)
        return self.v >= other.v

    def __pow__(self, other):
        """Power (**)"""
        if isinstance(other, Const):
            return Const(self.v ** other.v)
        elif isinstance(other, int):
            return Const(self.v ** other)
        elif isinstance(other, Float):
            # for base 10 the sig figs of the result are equal to the number of
            # significant decimal places in the exponent
            if self.v == 10.0:
                if other.lsd < 0:
                    return Float(10.0 ** other.v, int(np.abs(other.lsd)))
                elif other.lsd <= 0:
                    raise Float(10.0 ** other.v, 1)
            else:
                # for other bases, use the fact that the derivative of x^y is ln(x)*x^y
                # therefore a change of z yields a change in result of z * ln(x)*x^y
                deriv = np.log(self.v) * self.v ** other.v
                new_sf = int(np.floor(other.v - np.log10(deriv * 10 ** other.lsd))) + 1
                return Float(self.v ** other.v, new_sf)
        else:
            raise TypeError("only Float, Const, and int are accepted as exponents of Const")

    def __int__(self):
        """Integer Conversion"""
        return int(self.v)

    def __float__(self):
        """float conversion"""
        return self.v

    def __iadd__(self, other):
        """Increment by addition"""
        new_float = self + other
        self.__init__(new_float.v)

    def __imul__(self, other):
        """Increment by multiplication"""
        new_float = self * other
        self.__init__(new_float.v)

    def __itruediv__(self, other):
        """Increment by division"""
        new_float = self / other
        self.__init__(new_float.v)

    def __isub__(self, other):
        """Increment by subtraction"""
        new_float = self - other
        self.__init__(new_float.v)
