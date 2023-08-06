# PMXUtils

Tools for ProgModX

Note that the package is in development and may undergo frequent updates

Install with `python -m pip install pmxutils` for windows and `python3 -m pip install pmxutils` for unix/linux

# Table of content
* [Mathtools](https://github.com/Areskiko/pmxutils/blob/master/README.md#mathtools-pmxutilsmathtools)
  * [construct](https://github.com/Areskiko/pmxutils/blob/master/README.md#constructexpression-varx)
  * [advConstruct](https://github.com/Areskiko/pmxutils#advconstructexpression-args-constants--)
  * [computeList](https://github.com/Areskiko/pmxutils/blob/master/README.md#computelistsfunction-low-high-step1)
  * [newton](https://github.com/Areskiko/pmxutils/blob/master/README.md#newtonfunction-derivative-low-high-tolerance1e-8-rounding--3-iterations--1000)
  * [isInbetween](https://github.com/Areskiko/pmxutils/blob/master/README.md#isinbetweennumber-low-high)
  * [rectangleIntegral](https://github.com/Areskiko/pmxutils/blob/master/README.md#rectangleintegralfunction-low-high-n)
  * [trapezoidIntegral](https://github.com/Areskiko/pmxutils/blob/master/README.md#trapezoidintegralfunction-low-high-n)
  * [simpsonIntegral](https://github.com/Areskiko/pmxutils/blob/master/README.md#simpsonintegralfunction-low-high-n)
  * [euler](https://github.com/Areskiko/pmxutils/blob/master/README.md#eulerfunctionderivative-low-high-y0-n)
  * [lemma](https://github.com/Areskiko/pmxutils/blob/master/README.md#lemmaa-b)
* [Other](https://github.com/Areskiko/pmxutils/blob/master/README.md#other-pmxutilsother)
  * [profile](https://github.com/Areskiko/pmxutils/blob/master/README.md#profilefunction)
  * [loading](https://github.com/Areskiko/pmxutils/blob/master/README.md#loading)
    * [start](https://github.com/Areskiko/pmxutils/blob/master/README.md#startflavorloading)
    * [stop](https://github.com/Areskiko/pmxutils/blob/master/README.md#stop)
    * [animate](https://github.com/Areskiko/pmxutils/blob/master/README.md#animate)

## Mathtools (`pmxutils.mathtools`)

* #### `construct(expression, var=x)`
    >Returns a function computing the given expression
    
    * `expression` - The mathematical expression to compute, type = string
    * `var` - The variable used in the mathematical expression, defaults tp 'x', type = string

* #### `advConstruct(expression, *args, constants = {})
    >Returns a function computing the given expression

    * `expression` - The mathematical expression to compute, type = string
    * `args` - Any number of individual arguments naming the variables used in the expresion, type = string
    * `constants` - A dictionary with any numerical constants in the expression, type = dict

* #### `computeLists(function, low, high, step=1)`
    >Returns a touple of two lists containing x values inbetween low and high, and the computed results for y. In the format of (x_list, y_list)
    
    * `low` - The lower end of the function limit, type = number
    * `high` - The upper end of the function limit, type = number
    * `function` - The mathematical expression to use for y value computation, type = string or function from construct
    * `step` - The step size in the x value list, defaults to '1', type = number

* #### `newton(function, derivative, low, high, tolerance=1e-8, rounding = 3, iterations = 1000)`
    >Uses Newtons way of finding the root of a function, using the function and its derivative, within the given limits.Returns None if it can't find a solution that satisfies the tolerance after the defined number of terations
    
    * `function` - The target mathematical expression, type = string or function from construct
    * `derivative` - The derivative of the target mathematical expression, type = string or function from construct
    * `low` - The lower end of the are which should be checked for roots, type = number
    * `high` - The upper end of the are which should be checked for roots, type = number
    * `tolerance` - The tolerance for error to speed up computation, defaults to '1e-8', type = number
    * `rounding` - Rounds the x value for the root to the specified amount of decimals, defaults to '3', type = number
    * `iterations` - The number of tries, after which the function will end early

* #### `isInbetween(number, low, high)`
    >Returns True if number is inbetween limOne and limTwo, returns False otherwise
    
    * `number` - The number to be checked, type = number
    * `low` - The lower limit for which the number is checked, type = number
    * `high` - The upper limit for which the number is checked, type = number

* #### `rectangleIntegral(function, low, high, n)`
    >Returns the numerically calculated integral of the function f inbetween a and b using n rectangles

    * `function` - The function to integrate, type = string or function from construct
    * `low` - The low end of the area to be computed, type = number
    * `high` - The high end of the area to be computed, type = number
    * `n` - The number of rectangles to use, type = int

* #### `trapezoidIntegral(function, low, high, n)`
    >Returns the numerically calculated integral of the function f inbetween a and b using n trapezoids

    * `function` - The function to integrate, type = string or function from construct
    * `low` - The low end of the area to be computed, type = number
    * `high` - The high end of the area to be computed, type = number
    * `n` - The number of trapezoids to use, type = int

* #### `simpsonIntegral(function, low, high, n)`
    >Returns the numerically calculated integral of the function inbetween low and high using n quadratic splines

    * `function` - The function to integrate, type = string or function from construct
    * `low` - The low end of the area to be computed, type = number
    * `high` - The high end of the area to be computed, type = number
    * `n` - The number of quadratic splines to use, type = int

* #### `euler(functionDerivative, low, high, y0, n)`
    >Returns a numpy array x, containing the x values of the function, and an array F, containing the computed values for the antiderivative function of the given function functionDerivative inbetween low and high with N steps
    
    >Only supports functions with one variable

    * `functionDerivative` - The derivative of the goal function, type = string or function from construct
    * `low` - The low end of the function to be computed, type = number
    * `high` - The high end of the area to be computed, type = number
    * `y0` - The initial value of the goal function
    * `n` - The number of computations to perform

* #### `lemma(a, b)`
    >Returns the greatest common denominator of a and b using the lemma algorithm

    * `a` - The first number
    * `b` - The second number


## Other (`pmxutils.other`)

* #### `profile(function)`
    >Time profiler. Prints out the elapsed time during function execution

    * `function` - The function to profile, type = function

### `loading()`
Loading class
    
* #### `start(flavor="loading")`
    >Starts a loading sequence
        
    * `flavor` - The message to be displayed during loading, defaults to 'loading', type = string
* #### `stop()`
    >Stops the loading sequence
        
* #### `animate()`
    >DO NOT USE, internal function
