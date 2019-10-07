"""Routines related to testing credit card numbers for correctness.

The Luhn algorithm is the basis of the code here. An overview can be found
here:

https://en.wikipedia.org/wiki/Luhn_algorithm

Though the functions here are optimized for use in credit card validation,
they can be used for other numbers as well. IMEI numbers used in mobile
phones, for instance, also use Luhn validation, and these routines would
work well in that scenario.
"""


def check_luhn_validity(num: int, check_digit: int) -> bool:
    """Return True if the given number and check digit are consistent.
    
    Note that this doesn't catch all types of errors, due to limitations
    of the luhn algorithm. For instance transposing, 09 and 90 in the num
    will still return True.
    """
    return (get_luhn_sum(num) + check_digit) % 10 == 0


def generate_luhn_check_digit(num: int) -> int:
    """Return an integer from 0 to 9 that can validate the provided num.
    """
    return (get_luhn_sum(num) * 9) % 10


def get_luhn_sum(num: int) -> int:
    """Return a processed sum of the digits of an int using the Luhn algorithm.
    
    The returned sum can be used to generate a check digit, or, when checked
    against a preexisting check digit, it can ensure against many forms of
    data entry mistakes such as most transposed or off-by-one numbers.
    
    This implementation uses pure integer math instead of string operations.
    At typical credit card number lengths, it is about twice as fast as
    string-based implementations while still being easy to understand.
    
    One limitation is that the modulo and floor division operations used here
    do not scale linearly (the exact time complexity depends on the python
    version). On extremely large numbers of more than about 200 decimal
    digits, a linear-scaling string-based implementation performs better.
    """
    total = 0
    
    # Consume the num until it reaches zero
    while num > 0:
        # Calculate the two least significant digits using modulo.
        last_two_digits = num % 100
        
        # Get the left digit using floor division and add it to the total
        total += last_two_digits // 10
        
        # Get the right digit using modulo and double it. If the doubled
        # number is two digits, subtract 9. Add the result to the total.
        right = last_two_digits % 10 * 2
        if right > 9:
            right -= 9
        total += right
        
        # Remove the two digits we processed from the num before looping.
        num //= 100
    
    return total


# Below is a reasonably efficient string-based implementation of the luhn
# algorithm. It was used for comparison purposes and is no longer needed.
# It is retained here purely for reference.


def _get_luhn_sum_using_string(num: int) -> int:
    num_str = str(num)
    digit_is_odd = True
    total = 0
    for char in reversed(num_str):
        digit_value = int(char)
        
        if digit_is_odd:
            digit_value *= 2
            if digit_value > 9:
                digit_value -= 9
        
        total += digit_value
        digit_is_odd = not digit_is_odd
    
    return total