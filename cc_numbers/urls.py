
from django.urls import path

from . import views


urlpatterns = [
    path(
        'validation/<card_number>',
        views.ValidationView.as_view(),
        name='validation',
        ),
    path(
        'random',
        views.RandomCardNumberView.as_view(),
        name='random',
        ),
    path(
        'swagger',
        views.schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
        ),
    ]
