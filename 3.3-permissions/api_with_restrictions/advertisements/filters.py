from django_filters import rest_framework as filters, DateFromToRangeFilter, ChoiceFilter

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = DateFromToRangeFilter()
    # Поиск по статусу /?status=OPEN or CLOSED
    status = ChoiceFilter(choices=AdvertisementStatusChoices)

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status', 'creator']
