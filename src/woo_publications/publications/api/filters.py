from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters
from django_filters.widgets import CSVWidget

from woo_publications.logging.service import OwnerFilter
from woo_publications.metadata.models import InformationCategory

from ..constants import PublicationStatusOptions
from ..models import Document, Publication


class DocumentFilterSet(FilterSet):
    # TODO: change this filter to custom named filter with `@extend_schema_field(UUID)` once bug is fixed in drf-spectacular
    publicatie = filters.ModelChoiceFilter(
        queryset=Publication.objects.all(),
        to_field_name="uuid",
        help_text=_(
            "Search the document based on the unique identifier (UUID) that represents a publication. "
            "**Disclaimer**: disregard the documented type `integer` the correct type is `UUID`."
        ),
    )
    registratiedatum_vanaf = filters.DateTimeFilter(
        help_text=_(
            "Filter documents that were registered after or on the given value."
        ),
        field_name="registratiedatum",
        lookup_expr="gte",
    )
    registratiedatum_tot = filters.DateTimeFilter(
        help_text=_("Filter documents that were registered before the given value."),
        field_name="registratiedatum",
        lookup_expr="lt",
    )
    creatiedatum_vanaf = filters.DateTimeFilter(
        help_text=_("Filter documents that were created after or on the given value."),
        field_name="creatiedatum",
        lookup_expr="gte",
    )
    creatiedatum_tot = filters.DateTimeFilter(
        help_text=_("Filter documents that were created before the given value."),
        field_name="creatiedatum",
        lookup_expr="lt",
    )
    laatst_gewijzigd_datum_vanaf = filters.DateTimeFilter(
        help_text=_(
            "Filter documents that were last modified after or on the given value."
        ),
        field_name="laatst_gewijzigd_datum",
        lookup_expr="gte",
    )
    laatst_gewijzigd_datum_tot = filters.DateTimeFilter(
        help_text=_("Filter documents that were last modified before the given value."),
        field_name="laatst_gewijzigd_datum",
        lookup_expr="lt",
    )
    eigenaar = OwnerFilter(
        help_text=_("Filter documents based on the owner identifier of the object."),
    )
    publicatiestatus = filters.ChoiceFilter(
        help_text=_("Filter documents based on the publication status."),
        choices=PublicationStatusOptions.choices,
    )
    identifier = filters.CharFilter(
        help_text="Search the document based on the identifier field.",
    )
    sorteer = filters.OrderingFilter(
        help_text=_("Order on."),
        fields=(
            "creatiedatum",
            "officiele_titel",
            "verkorte_titel",
        ),
    )

    class Meta:
        model = Document
        fields = (
            "publicatie",
            "eigenaar",
            "publicatiestatus",
            "identifier",
            "registratiedatum_vanaf",
            "registratiedatum_tot",
            "creatiedatum_vanaf",
            "creatiedatum_tot",
            "laatst_gewijzigd_datum_vanaf",
            "laatst_gewijzigd_datum_tot",
            "sorteer",
        )


class PublicationFilterSet(FilterSet):
    search = filters.CharFilter(
        help_text=_("Searches publications based on the official and short title."),
        method="search_official_and_short_title",
    )
    eigenaar = OwnerFilter(
        help_text=_("Filter publications based on the owner identifier of the object."),
    )
    publicatiestatus = filters.ChoiceFilter(
        help_text=_("Filter publications based on the publication status."),
        choices=PublicationStatusOptions.choices,
    )
    registratiedatum_vanaf = filters.DateTimeFilter(
        help_text=_(
            "Filter publications that were registered after or on the given value."
        ),
        field_name="registratiedatum",
        lookup_expr="gte",
    )
    registratiedatum_tot = filters.DateTimeFilter(
        help_text=_("Filter publications that were registered before the given value."),
        field_name="registratiedatum",
        lookup_expr="lt",
    )
    informatie_categorieen = filters.ModelMultipleChoiceFilter(
        help_text=_(
            "Filter publications that belong to a particular information category. "
            "When you specify multiple categories, publications belonging to any "
            "category are returned.\n\n"
            "Filter values should be the UUID of the categories."
        ),
        field_name="informatie_categorieen__uuid",
        to_field_name="uuid",
        queryset=InformationCategory.objects.all(),
        widget=CSVWidget(),
    )

    sorteer = filters.OrderingFilter(
        help_text=_("Order on."),
        fields=(
            "registratiedatum",
            "officiele_titel",
            "verkorte_titel",
        ),
    )

    class Meta:
        model = Publication
        fields = (
            "search",
            "eigenaar",
            "publicatiestatus",
            "informatie_categorieen",
            "registratiedatum_vanaf",
            "registratiedatum_tot",
            "sorteer",
        )

    def search_official_and_short_title(self, queryset, name: str, value: str):
        return queryset.filter(
            Q(officiele_titel__icontains=value) | Q(verkorte_titel__icontains=value)
        )
