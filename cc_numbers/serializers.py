
import types

from rest_framework import serializers

from .lib.const import IIN_DIGITS


class ValidationSerializer(serializers.Serializer):
    """Validation data related to a credit card number.
    
    Though this is pretty straightforward, one thing to point out is
    the frequent use of CharField, even though the data in mostly numeric.
    However, almost all of the fields can have leading zeroes, and the
    IntField would not allow this.
    """
    is_valid = serializers.BooleanField(read_only=True)
    major_industry_identifier = serializers.CharField(
        read_only=True,
        min_length=1,
        max_length=1,
        )
    issuer_identification_number = serializers.CharField(
        read_only=True,
        min_length=IIN_DIGITS,
        max_length=IIN_DIGITS,
        )
    personal_account_number = serializers.CharField(
        read_only=True,
        source='individual_account_identifier',
        )
    check_digit = serializers.CharField(
        read_only=True,
        min_length=1,
        max_length=9,
        )
    network = serializers.CharField(read_only=True)


class CardNumberSerializer(serializers.Serializer):
    """Basic data for a credit card number and validation link.
    """
    card_number = serializers.IntegerField(read_only=True)
    validation_link = serializers.URLField()
    
    def __init__(self, card_number=None, validation_link=None):
        """Set up a new instance.
        
        We override this to modify the signature so that callers don't
        need to create an object instance, as is required by the parent
        class.
        """
        instance = types.SimpleNamespace(
            card_number=card_number,
            validation_link=validation_link,
            )
        super().__init__(instance)


class ErrorSerializer(serializers.Serializer):
    """A standardized data format for reporting errors.
    """
    error = serializers.CharField(read_only=True)
    
    def __init__(self, error=''):
        """Set up a new instance.

        We override this to modify the signature so that callers don't
        need to create an object instance, as is required by the parent
        class.
        """
        instance = types.SimpleNamespace(
            error=error,
            )
        super().__init__(instance)