# fonc

<small>multiline inline anonymous functions in python</small>

```python
>>> from fonc import fonc
>>> [
...     fonc("""
... def x(input): # doesn't matter what this function is called
...     value = input * 3.14
...     return int(value)
...     """)(value) for value in [1, 2, 3, 4]
... ]
[3, 6, 9, 12]
```

## why would you do this terrible thing

:) :) :) :) :) :) :) :) :) :) :) :)

## does this pollute my global namespace?

nope!

imagine this inline function:

```python
>>> from fonc import fonc
>>> [
...     fonc("""
... def x(input): # doesn't matter what this function is called
...     value = input * 3.14
...     return int(value)
...     """)(value) for value in [1, 2, 3, 4]
... ]
[3, 6, 9, 12]
```

One might imagine that this means that the `x` function name is overwritten to the global namespace. It is not!

```py
>>> x(1)
```

```
NameError: name 'x' is not defined
```

## how this works pls?

-   parse the string and determine the name of the defined function
-   replace that with a known random value
-   replace calls to that inline function with calls to the renamed function

## never-asked questions

-   Do I have access to global vars inside this function?

    ya

-   Can I use this in production?

    absolutely not u fool
