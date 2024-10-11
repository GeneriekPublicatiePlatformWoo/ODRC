from io import StringIO
from pathlib import Path

from django.core.management import call_command

import requests
from glom import Coalesce, PathAccessError, T, glom

from woo_publications.metadata.models import Theme

WAARDENLIJST_URL = "https://repository.officiele-overheidspublicaties.nl/waardelijsten/scw_toplijst/1/json/scw_toplijst_1.json"

SPEC = {
    "data": {
        "identifier": "@id",
        "naam": T["http://www.w3.org/2004/02/skos/core#prefLabel"][0]["@value"],
    },
    "parents": Coalesce(
        (T["http://www.w3.org/2004/02/skos/core#broader"], ["@id"]), default=[]
    ),
}


class ThemeWaardenlijstError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def update_theme(file_path: Path):
    try:
        response = requests.get(WAARDENLIJST_URL)
    except requests.RequestException as err:
        raise ThemeWaardenlijstError("Could not retrieve the value list data.") from err

    try:
        response.raise_for_status()
    except requests.RequestException as err:
        raise ThemeWaardenlijstError(
            f"Got an unexpected response status code when retrieving the value list data: {response.status_code}."
        ) from err

    data = response.json()
    if not data:
        raise ThemeWaardenlijstError("Received empty data from value list.")

    waardenlijst = [
        glom(theme, SPEC, skip_exc=PathAccessError)
        for theme in data
        if theme["@type"][0] == "http://www.w3.org/2004/02/skos/core#Concept"
    ]

    root_themes_data = [theme["data"] for theme in waardenlijst if not theme["parents"]]
    sub_themes = [theme for theme in waardenlijst if theme["parents"]]

    # create/update root themes
    for theme in root_themes_data:
        theme_object = Theme.objects.filter(identifier=theme["identifier"])
        if theme_object.exists():
            theme_object.update(**theme)
        else:
            Theme.add_root(**theme)

    # create/update sub themes
    for theme in sub_themes:
        theme_object = Theme.objects.filter(identifier=theme["data"]["identifier"])
        for parent in theme["parents"]:
            if theme_object.exists():
                theme_object.update(**theme["data"])
            else:
                parent = Theme.objects.get(identifier=parent)
                parent.add_child(**theme["data"])

    to_export = Theme.objects.all().values_list("pk", flat=True)

    call_command(
        "dumpdata",
        "metadata.theme",
        format="json",
        indent=4,
        natural_primary=True,
        pks=",".join([str(pk) for pk in to_export]),
        output=file_path,
        stdout=StringIO(),
    )
