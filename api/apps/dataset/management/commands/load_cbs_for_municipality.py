# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2022 Vereniging van Nederlandse Gemeenten, Gemeente Amsterdam
"""
Extract neighborhood data for a given municipality from CBS data.

Note:
- Centraal Bureau voor de Statistiek (CBS) neighborhood and municipal map data
  must be present in the Signalen database.
- The Signalen instance that we run this script for must serve one municipality.
- AreaTypes will be added that have names `<municipal_code>-wijk` and
  `<municipal_code>-buurt`.
- The Dutch "buurt" and "wijk" both translate to neighborhood, but in the
  Netherlands "wijk" areas are larger and consist of "buurt" areas. We use the
  Dutch terms below - the use of CBS data makes this code specific to the
  Netherlands.
"""
from apps.dataset.sources.cbs import CBSBoundariesLoader
from django.core.management import BaseCommand

REQUIRED_DATASETS = {
    # Dataset names must match those defined in apps.dataset.sources.cbs
    "CBS_MUNICIPAL_BORDERS_DATASET": "cbs-gemeente-2022",
    "CBS_WIJK_DATASET": "cbs-wijk-2022",
    "CBS_BUURT_DATASET": "cbs-buurt-2022",
}


class Command(BaseCommand):
    def _cbs_data_present(self):
        """
        We need the CBS data municipal borders and neighborhood borders
        """

    def handle(self, *args, **options):
        """
        Find neighborhoods in requested municipality store them as a dataset.

        Note: storing as a dataset in this context means that a we derive
        area type names for the neighborhoods in the municipality under
        consideration. We store a copy of all relevant neighborhoods (both the
        Dutch "wijk" and "buurt" types of neighborhood) associated with the
        newly created AreaTypes.
        """
        loader = CBSBoundariesLoader(dir="/tmp/")

        loader.load()
