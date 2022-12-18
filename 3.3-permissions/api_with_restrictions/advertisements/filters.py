from django_filters import ChoiceFilter
from django_filters.rest_framework import DateFromToRangeFilter, FilterSet

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(FilterSet):
    """Фильтры для объявлений."""

    created_at = DateFromToRangeFilter()
    status = ChoiceFilter(field_name='status', choices=AdvertisementStatusChoices.choices)

    class Meta:
        model = Advertisement
        fields = ['created_at', 'creator', 'status']
