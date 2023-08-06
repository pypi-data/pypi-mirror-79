# pysigfig
A package for creating and manipulating floating point numbers accounting for significant figures

![Python package](https://github.com/bertcarnell/pysigfig/workflows/Python%20package/badge.svg)

## Quickstart

```{python}
import math

import pysigfig as pysf


# a number with 4 singificant digits
x = pysf.Float("1.234")
# a number with 3 significant digits
y = pysf.Float("31.1")

z1 = x + y
z2 = x * y

# z1 should have tenths digit as the least significant
print(z1)
# z2 should have 3 significant digits
print(z2)

area = pysf.Const(math.pi) * pysf.Float("2.0")**2
# area should have 2 significant digits
print(area)
```

### Methods of Entry

```{python}
# Enter a floating point number and specify the number of significant digits
pysf.Float(1.2345, 2)
pysf.Float(1.2, 8)

# Enter the string representation
pysf.Float("1.23") # 3 sig figs
pysf.Float("1.230000") # 7 sig figs
pysf.Float("0.0045") # 2 sig figs
pysf.Float("100000") # 6 sig figs
pysf.Float("1.0E+06") # 2 sig figs

# Enter a constant
pysf.Const(2)
pysf.Const(math.pi)
```
