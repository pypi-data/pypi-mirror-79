"""
Random Number Generator
-----------------------
This module generates random numbers as many as you wish. Do not forget to mention the number of random number you need. 

.. code-block:: python
	:linenos:

	print_random(n_numbers=5)

"""

import numpy as np


def print_random(n_numbers=1):
    """
	:param name: n_numbers - How many random number you need.
	:param type: int
	:return: numpy.array
	"""
    ra = np.random.rand(n_numbers)
    print(f"Printing a random number: \n \t {ra}")
    return ra


def chappu():
    """
		This is how chimmili is.
    """
    print(
        "Chimmili is a short temper girl, Who forgets every thing when in angry. Keep a safe distance from her."
    )


def help():
    print("function - print_random,\n function - chappu")


if __name__ == "__main__":
    print_random(5)
    chappu()
