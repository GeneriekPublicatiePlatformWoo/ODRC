import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from zgw_consumers.constants import APITypes

from woo_publications.logging.constants import Events
from woo_publications.logging.models import TimelineLogProxy
from woo_publications.logging.typing import ActingUser

# when the document isn't specified both the service and uuid needs to be unset
_DOCUMENT_NOT_SET = models.Q(document_service=None, document_uuid=None)
# when the document is specified both the service and uuid needs to be set
_DOCUMENT_SET = ~models.Q(document_service=None) & ~models.Q(document_uuid=None)


class Publication(models.Model):
    uuid = models.UUIDField(
        _("UUID"),
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    informatie_categorieen = models.ManyToManyField(
        "metadata.informationcategory",
        verbose_name=_("information categories"),
        help_text=_(
            "The information categories clarify the kind of information present in the publication."
        ),
    )
    publisher = models.ForeignKey(
        "metadata.organisation",
        verbose_name=_("publisher"),
        related_name="published_publications",
        help_text=_("The organisation which publishes the publication."),
        limit_choices_to={"is_actief": True},
        on_delete=models.CASCADE,
    )
    verantwoordelijke = models.ForeignKey(
        "metadata.organisation",
        verbose_name=_("liable organisation"),
        related_name="liable_for_publications",
        help_text=_(
            "The organisation which is liable for the publication and its contents."
        ),
        limit_choices_to={"is_actief": True},
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    opsteller = models.ForeignKey(
        "metadata.organisation",
        verbose_name=_("drafter"),
        related_name="drafted_publications",
        help_text=_("The organisation which drafted the publication and its content."),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    officiele_titel = models.CharField(
        _("official title"),
        max_length=255,
    )
    verkorte_titel = models.CharField(
        _("short title"),
        max_length=255,
        blank=True,
    )
    omschrijving = models.TextField(_("description"), blank=True)
    registratiedatum = models.DateTimeField(
        _("created on"),
        auto_now_add=True,
        editable=False,
        help_text=_(
            "System timestamp reflecting when the publication was registered in the "
            "database. Not to be confused with the creation date of the publication, "
            "which is usually *before* the registration date."
        ),
    )
    laatst_gewijzigd_datum = models.DateTimeField(
        _("last modified"),
        auto_now=True,
        editable=False,
        help_text=_(
            "System timestamp reflecting when the publication was last modified in the "
            "database."
        ),
    )

    class Meta:  # type: ignore
        verbose_name = _("publication")
        verbose_name_plural = _("publications")

    def get_owner(self) -> ActingUser | None:
        """
        Extract the owner from the audit trails.
        """
        qs = TimelineLogProxy.objects.for_object(self)  # type: ignore reportAttributeAccessIssue
        try:
            log = qs.get(extra_data__event=Events.create)
        except TimelineLogProxy.DoesNotExist:
            return None
        assert isinstance(log, TimelineLogProxy)
        return log.acting_user[0]

    def __str__(self):
        return self.officiele_titel


class Document(models.Model):
    uuid = models.UUIDField(
        _("UUID"),
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    publicatie = models.ForeignKey(
        Publication,
        verbose_name=_("publication"),
        help_text=_(
            "The publication that this document belongs to. A publication may have "
            "zero or more documents."
        ),
        on_delete=models.CASCADE,
    )
    identifier = models.CharField(
        _("identifier"),
        help_text=_("The (primary) unique identifier."),
        max_length=255,
    )
    officiele_titel = models.CharField(
        _("official title"),
        max_length=255,
    )
    verkorte_titel = models.CharField(
        _("short title"),
        max_length=255,
        blank=True,
    )
    omschrijving = models.TextField(_("description"), blank=True)
    creatiedatum = models.DateField(
        _("creation date"),
        help_text=_(
            "Date when the (physical) document came into existence. Not to be confused "
            "with the registration timestamp of the document - the creation date is "
            "typically *before* the registration date."
        ),
    )
    bestandsformaat = models.CharField(
        _("file format"),
        max_length=255,
        help_text=_(
            "TODO - placeholder accepting anything, in the future this will be "
            "validated against a reference value list."
        ),
        default="unknown",  # TODO: remove this once the formats are set up properly
    )
    bestandsnaam = models.CharField(
        _("file name"),
        max_length=255,
        help_text=_("File name 'on disk' of the document, e.g. 'gelakt-verslag.pdf'."),
        default="unknown.bin",  # TODO: remove this once we can enforce the blank=False
    )
    bestandsomvang = models.PositiveIntegerField(
        _("file size"),
        default=0,
        help_text=_("Size of the file on disk, in bytes."),
    )
    registratiedatum = models.DateTimeField(
        _("created on"),
        auto_now_add=True,
        editable=False,
        help_text=_(
            "System timestamp reflecting when the document was registered in the "
            "database. Not to be confused with the creation date of the document, "
            "which is usually *before* the registration date."
        ),
    )
    laatst_gewijzigd_datum = models.DateTimeField(
        _("last modified"),
        auto_now=True,
        editable=False,
        help_text=_(
            "System timestamp reflecting when the document was last modified in the "
            "database."
        ),
    )

    # Documents API integration
    document_service = models.ForeignKey(
        "zgw_consumers.Service",
        verbose_name=_("Documents API Service"),
        on_delete=models.PROTECT,
        limit_choices_to={
            "api_type": APITypes.drc,
        },
        null=True,
        blank=True,
    )
    document_uuid = models.UUIDField(
        _("document UUID"),
        help_text=_("The UUID of the API resource recorded in the Documenten API."),
        unique=False,
        editable=True,
        null=True,
        blank=True,
    )
    lock = models.CharField(
        _("document lock"),
        max_length=255,
        blank=True,
        help_text=_(
            "The lock value to be able to update this document in the Documents API.",
        ),
    )

    class Meta:  # type: ignore
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        constraints = [
            models.CheckConstraint(
                check=(_DOCUMENT_NOT_SET | _DOCUMENT_SET),
                name="documents_api_reference",
                violation_error_message=_(
                    "You must specify both the Documents API service and document UUID to identify a "
                    "document.",
                ),
            )
        ]

    def __str__(self):
        return self.officiele_titel
