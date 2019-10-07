"""Some constant data structures related to credit card data.

Although the structure design here is sufficient for handling everything
this app needs, the data contained in the structures is far from
comprehensive. For instance, the networks listed here are only a small
subset of the existing networks, though they are the most common ones.
Likewise, the IIN ranges only cover roughly 25% of the possible IIN space.

Unfortunately, authoritative and complete data is not publicly
available. The data here is cobbled together from various internet sources.

If we were able to expand this and needed the ability to add new data as
it is acquired, this design would quickly become burdensome. Probably,
using DB models would be a good option in that case. For a simple demo
project, this static data is probably good enough, with very efficient
performance that a DB system would not be able to match.
"""

# The number of digits in an Issuer Identification Number
# This number is scheduled to increase to 8
IIN_DIGITS = 6

# Enums for each network. This could become cumbersome if we add too many.
NETWORK_VISA = 1
NETWORK_MASTERCARD = 2
NETWORK_AMEX = 3
NETWORK_DISCOVER = 4
NETWORK_DINERS = 5
NETWORK_JCB = 6

# Map a string name to each enum.
NETWORK_NAME_TO_ENUM = {
    'visa': NETWORK_VISA,
    'mastercard': NETWORK_MASTERCARD,
    'amex': NETWORK_AMEX,
    'discover': NETWORK_DISCOVER,
    'diners': NETWORK_DINERS,
    'jcb': NETWORK_JCB,
    }
# Map the enum back to the string name.
NETWORK_ENUM_TO_NAME = {v: k for (k, v) in NETWORK_NAME_TO_ENUM.items()}

# For each network, a tuple of possible card number lengths.
NETWORK_DIGITS = {
    NETWORK_VISA: (13, 16),
    NETWORK_MASTERCARD: (16,),
    NETWORK_AMEX: (15,),
    NETWORK_DISCOVER: (16,),
    NETWORK_DINERS: (15, 16),
    NETWORK_JCB: (14,),
    }

# Ranges of IINs reserved for issuers who use each network.
# This would need to be reworked for 8-digit IINs.
NETWORK_IIN_RANGES = {
    NETWORK_VISA: (
        (400_000, 499_999),
        ),
    NETWORK_MASTERCARD: (
        (222_100, 272_999),
        (510_000, 559_999),
        ),
    NETWORK_AMEX: (
        (340_000, 349_999),
        (370_000, 379_999)
        ),
    NETWORK_DISCOVER: (
        (601_100, 601_199),
        (622_126, 622_925),
        (624_000, 626_999),
        (628_200, 628_899),
        (640_000, 659_999),
        ),
    NETWORK_DINERS: (
        (360_000, 369_999),
        (380_000, 389_999),
        ),
    NETWORK_JCB: (
        (352_800, 358_999),
        ),
    }

# Create a convenient lookup dict for getting the network of an IIN.
IIN_NETWORKS = {}
for _network, _ranges in NETWORK_IIN_RANGES.items():
    for (_lower, _upper) in _ranges:
        IIN_NETWORKS.update({i: _network for i in range(_lower, _upper + 1)})
