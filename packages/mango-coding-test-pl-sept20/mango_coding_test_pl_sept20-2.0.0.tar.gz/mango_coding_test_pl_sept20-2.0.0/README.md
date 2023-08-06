# mango_test

Package containing Peter Ling's solutions to the Mango Python coding test, September 2020.

## Installation

The package can be installed from PyPI via the command line by typing
`pip install mango_coding_test_pl_sept20`.

## Usage

The solutions can then be used in a Python 3 environment after using the import statement
`from mango_test import mango_test as mt`

#### Functions
The 'Functions' part of the exercise is called with the `random_draw(nsamples, dist, **params)` function, where `params` relate to the given distribution.

##### Examples
To return a 10 random samples (as a numpy array) from a Normal distribution with mean 100 and standard deviation 10:

    mt.random_draw(10, 'normal', mean=100, sd=10)

To return a 20 random samples from a Binomial distribution with _n_=100, _p_=0.5:

    mt.random_draw(20, 'binomial', n=100, p=0.5)

To return a 100 random samples from a Poisson distribution with $\lambda$=100:

    mt.random_draw(100, 'poisson', lam=100)

#### Object-oriented Programming
The 'Object-oriented Programming' part of the exercise is called with the `Sample` class.

##### Example
To create an instance of the `Sample` class, using the Normal distribution:

    s = mt.Sample('normal')

To set the parameters of `s` (mean and standard deviation):

    s.mean = 100
    s.sd = 100

To draw a 1000 samples from `s`, then summarise:

    s.draw(1000)
    s.summarise()
 