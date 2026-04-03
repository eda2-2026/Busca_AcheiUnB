import django_filters

from users.models import Item


class ItemFilter(django_filters.FilterSet):
    category_name = django_filters.CharFilter(
        field_name="category__name", lookup_expr="icontains"
    )
    location_name = django_filters.CharFilter(
        field_name="location__name", lookup_expr="icontains"
    )
    color_name = django_filters.CharFilter(field_name="color__name", lookup_expr="icontains")
    brand_name = django_filters.CharFilter(field_name="brand__name", lookup_expr="icontains")

    class Meta:
        model = Item
        fields = ["category_name", "location_name", "color_name", "brand_name", "status"]
