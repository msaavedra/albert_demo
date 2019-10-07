
from django.views.decorators.cache import never_cache
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView, Response

from .lib import const
from .lib.formatting import CardData, create_random_cc_number
from . import serializers


CARD_NETWORKS = ', '.join(const.NETWORK_NAME_TO_ENUM)

# Set up a standard error reporting format for use in all views.
ERROR_SERIALIZER_CLASS = serializers.ErrorSerializer
SWAGGER_ERROR_RESPONSE = openapi.Response(
    'BAD REQUEST',
    ERROR_SERIALIZER_CLASS(),
    )


class ValidationView(APIView):
    """An API endpoint view for validating credit card data.
    
    This is the main part of the API described in the project overview.
    """
    serializer_class = serializers.ValidationSerializer
    
    # Some OpenAPI documentation hints
    ok_response = openapi.Response('OK', serializer_class())
    card_num_param = openapi.Parameter(
        'card_number',
        openapi.IN_PATH,
        description=(
            'Numeric values, spaces, and hyphens are allowed. There must '
            'be at least 12 numeric digits and no more than 19.'
            ),
        type=openapi.TYPE_STRING,
        )
    
    @swagger_auto_schema(
        operation_id=' ',
        manual_parameters=[card_num_param],
        responses={
            200: ok_response,
            status.HTTP_400_BAD_REQUEST: SWAGGER_ERROR_RESPONSE,
            }
        )
    def get(self, request, card_number):
        """Get validated credit card data extracted from the provided number.
        
        For the purposes of this API, validated means only that the number
        has been algorithmically determined to be self-consistent. No
        determination has been made whether the number is tied to an
        actual financial account.
        
        A few implementation notes:
            * We use a GET method here because it is simplest, for both the
              service and for clients. A POST method would have worked, as the
              HTTP standard allows for using POST to access endpoints that are
              essentially procedure calls where complex parameters may be
              needed. However, our parameter needs are very simple. Also,
              using GET to retrieve data in a Restful service just feels
              better.
            * There is an extra "network" field in the response that is not
              included in the API description from the case study doc. However,
              the requirements from that doc specify that the API should
              "Detect (at least) the 4 major US networks," so that requirement
              is demonstrated here.
        """
        try:
            card_data = CardData(card_number)
        except TypeError as e:
            error_serializer = ERROR_SERIALIZER_CLASS(error=str(e))
            return Response(
                error_serializer.data,
                status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = self.serializer_class(card_data)
        return Response(serializer.data)


class RandomCardNumberView(APIView):
    """An API endpoint view for generating random credit card numbers.
    
    This is the "bonus" endpoint described in the project overview.
    """
    serializer_class = serializers.CardNumberSerializer
    
    # Some OpenAPI documentation hints
    ok_response = openapi.Response('OK', serializer_class())
    network_param = openapi.Parameter(
        'network',
        openapi.IN_QUERY,
        description=(
            'Valid values are: {}. '
            'If this parameter is omitted, a network is chosen at random.'
            ).format(CARD_NETWORKS),
        type=openapi.TYPE_STRING,
        list=list(const.NETWORK_NAME_TO_ENUM),
        )

    
    @never_cache
    @swagger_auto_schema(
        operation_id=' ',
        manual_parameters=[network_param],
        responses={
            200: ok_response,
            status.HTTP_400_BAD_REQUEST: SWAGGER_ERROR_RESPONSE,
            }
        )
    def get(self, request):
        """Get a randomly generated, validly formatted credit card number.
        
        The output card number is restricted to the networks and IIN ranges
        known to this app.
        
        A few implementation notes:
            * The rationale for using GET from the validation endpoint applies
              here as well.
            * Since this returns a new value every time, disabling client-side
              caching is important.
        """
        network_name = request.GET.get('network')
        try:
            card_number = create_random_cc_number(network_name)
        except KeyError:
            error_serializer = ERROR_SERIALIZER_CLASS(
                error=f'Invalid network. Valid values are {CARD_NETWORKS}.'
                )
            return Response(
                error_serializer.data,
                status=status.HTTP_400_BAD_REQUEST
                )
        
        validation_link = request.build_absolute_uri(
            reverse('validation', args=[card_number])
            )
        serializer = self.serializer_class(
            card_number,
            validation_link
            )
        return Response(serializer.data)


# For the swagger online documentation.
schema_view = get_schema_view(
   openapi.Info(
      title="Credit Card Numbers Project",
      default_version='', # No versioning for this simple demo.
      description="A demo project that validates credit card numbers.",
      terms_of_service='',
      contact=openapi.Contact(email="mtsaavedra@gmail.com"),
   ),
   public=True,
   permission_classes=(),
)
