"""Code dealing with how credit card numbers are formatted.

The format is standardized in ISO/IEC 7812, which is a proprietary standard
and not freely available. This implementation is based mostly on:

https://en.wikipedia.org/wiki/ISO/IEC_7812
"""

import random
from typing import Union

from . import const
from . import validation


class CardData:
    """A simple data class for describing the parts of a credit card number.
    """
    def __init__(self, card_number: str):
        card_number = card_number.replace(' ', '').replace('-', '')
        if not card_number.isnumeric():
            raise TypeError(
                'A card number can only contain numbers, spaces, and hyphens'
                )
        if not 12 <= len(card_number) <= 19:
            raise TypeError('A card number must be between 12 and 19 digits.')
            
        self.primary_account_number = card_number
        
        # These are defined in ISO/IEC 7812.
        self.major_industry_identifier = card_number[0]
        self.issuer_identification_number = card_number[:const.IIN_DIGITS]
        self.check_digit = card_number[-1]
        
        # This is the number with the IIN and check digit stripped.
        self.individual_account_identifier = card_number[const.IIN_DIGITS:-1]
        
        self.is_valid = validation.check_luhn_validity(
            int(card_number[:-1]),
            int(self.check_digit),
            )
        
        self.network = const.NETWORK_ENUM_TO_NAME.get(
            const.IIN_NETWORKS.get(int(self.issuer_identification_number)),
            'unknown',
            )


def create_random_cc_number(network_name: Union[None, str]) -> str:
    """Create a valid credit card number using random data.
    """
    # If the network is None, pick at random
    if network_name is None:
        network_number = random.choice(list(const.NETWORK_IIN_RANGES.keys()))
    else:
        network_number = const.NETWORK_NAME_TO_ENUM[network_name]
    
    # Find a random IIN from within the network's IIN ranges.
    iin_range = random.choice(const.NETWORK_IIN_RANGES[network_number])
    iin = str(random.randint(*iin_range))
    
    # Create an individual account number such that its length, plus the
    # IIN and the check digit, will add up to an appropriate value for
    # the network.
    full_card_digits = random.choice(const.NETWORK_DIGITS[network_number])
    account_digits = full_card_digits - const.IIN_DIGITS - 1
    account_upper_bound = int('9' * account_digits)
    account_number = str(random.randint(0, account_upper_bound))
    
    base_number = '{}{}'.format(
        iin.zfill(const.IIN_DIGITS),
        account_number.zfill(account_digits),
        )
    check_digit = validation.generate_luhn_check_digit(int(base_number))
    return f'{base_number}{check_digit}'
