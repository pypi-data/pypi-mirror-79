[![Downloads](https://pepy.tech/badge/randomless)](https://pepy.tech/project/randomless)
# Randomless
A python module which provides a True Random Number Generator (TRNG) based on the electronic noise captured by your webcam. The api is mostly compatible with Python's default random module.
## Requirements
Python 3 \
opencv-python \
numpy \
A webcam with drivers installed.
## Installation
```sh
pip install randomless
```
## Usage
Import.
```python
from randomless import Random
```
Create a Random class instance.
```python
random = Random()
```
Generate a random number just like you would with Python's default random module.
```python
random.random()
```
Use any other random method the same way as it is with Python's RNG.
```python
print('randrange:', random.randrange(0, 5, 1))

print('randint:', random.randint(0, 5))

print('choice:', random.choice([1, 2, 3, 4, 5]))

l = [1, 2, 3, 4, 5]
random.shuffle(l)
print('shuffle:', l)

print('sample:', random.sample([1, 2, 3, 4, 5], 3))

print('random:', random.random())

print('uniform:', random.uniform(0, 5))

print('triangular:', random.triangular(0, 1, 0.5))

print('betavariate:', random.betavariate(1, 1))

print('expovariate:', random.expovariate(5))

print('gammavariate:', random.gammavariate(1, 1))

print('gauss:', random.gauss(1, 1))

print('lognormvariate:', random.lognormvariate(1, 1))

print('normalvariate:', random.normalvariate(1, 1))

print('vonmisesvariate:', random.vonmisesvariate(1, 1))

print('paretovariate:', random.paretovariate(1))

print('weibullvariate:', random.weibullvariate(1, 1))
```
Stop the process of collecting noise from your webcam.
```python
random.release()
```
