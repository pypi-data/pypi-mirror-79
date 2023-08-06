# destructipy
es6 style dict/object destructure for python

#### install:
```
$ pip install destructipy
```

#### usage:
```python
# must import this way...
from destructipy import _ as ds

# support dicts
abcd = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# ds.i()/ds.item() - using operator.itemgetter
# dict safe, will probably raise error if not dict
d, c, \
b, a = ds.i(abcd)
print(a, b, c, d)
```
```python
# func can be named however you wish...
from destructipy import _ as unpack

# supports objects
class ABCD:
    a = 1
    b = 2
abcd = ABCD()
abcd.c = 3
abcd.d = 4

# unpack.a()/unpack.attr() - using operator.attrgetter
# notice: dicts can also be passed but it will get their attributes, not items)
d, c, \
b, a = unpack.a(abcd)
print(a, b, c, d)
```
```python
from destructipy import _ as ds

abcd_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

class ABCD:
    a = 5
    b = 6
abcd_obj = ABCD()
abcd_obj.c = 7
abcd_obj.d = 8

# ds() - auto decide if it's dict or object
# good for one time or mixed dict-object/small lists
# got minor performance penalty, see benchmark below
d, c, b, a = ds(abcd_dict)
print(a, b, c, d)

d, c, b, a = ds(abcd_obj)
print(a, b, c, d)
```

#### caveats:  
* Does not work on the Interactive Python Console (no source to analyze...)
* If you plan to compile your `.py` to `.pyc` and delete the source, run `$ python -m destructipy` in your project root to create `.destructipy` cache file before doing so
* It is recommended to place a `import destructipy` on your project init for destructipy to keep the initial cwd (current working directory), just incase you switch the cwd later on using `os.chdir` or such...
* using sys._getframe which is only implemented at CPython. tested on 2.7 and 3.8

#### benchmark:
```
$ python benchmark.py

9 iterations:
regular   : 0:00:00.000009
ds        : 0:00:00.000100
ds.i/ds.a : 0:00:00.000024

99 iterations:
regular   : 0:00:00.000020
ds        : 0:00:00.000066
ds.i/ds.a : 0:00:00.000061

999 iterations:
regular   : 0:00:00.000164
ds        : 0:00:00.000568
ds.i/ds.a : 0:00:00.000521

9999 iterations:
regular   : 0:00:00.001409
ds        : 0:00:00.005194
ds.i/ds.a : 0:00:00.004448

99999 iterations:
regular   : 0:00:00.011635
ds        : 0:00:00.045619
ds.i/ds.a : 0:00:00.040462

999999 iterations:
regular   : 0:00:00.104921
ds        : 0:00:00.396913
ds.i/ds.a : 0:00:00.377507

9999999 iterations:
regular   : 0:00:01.034074
ds        : 0:00:03.985506
ds.i/ds.a : 0:00:03.883992

99999999 iterations:
regular   : 0:00:10.758053
ds        : 0:00:46.962093
ds.i/ds.a : 0:00:45.535044

999999999 iterations:
regular   : 0:02:00.999255
ds        : 0:08:04.748202
ds.i/ds.a : 0:07:42.837535
```
