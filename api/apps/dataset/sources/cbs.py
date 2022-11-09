from apps.dataset.sources.shape import ShapeBoundariesLoader
from apps.locations.models import AreaType


class CBSBoundariesLoader(ShapeBoundariesLoader):
    """
    Load municipal (and neigbhorhood) boundaries as SIA Area instances.
    """

    DATASET_URL = "https://www.cbs.nl/-/media/cbs/dossiers/nederland-regionaal/wijk-en-buurtstatistieken/wijkbuurtkaart_2022_v1.zip"  # noqa
    # Unfortunately, these filenames are not uniformly named over the years,
    # so a hard-coded mapping is provided for the most recent data file (as of
    # this writing early 2022).

    CBS_GEMEENTE_2022 = "cbs-gemeente-2022"
    CBS_WIJK_2022 = "cbs-wijk-2022"
    CBS_BUURT_2022 = "cbs-buurt-2022"

    DATASET_INFO = [
        {
            "area_type_code": CBS_GEMEENTE_2022,
            "shp_file": "WijkBuurtkaart_2022_v1/gemeente_2022_v1.shp",
            "code_field": "GM_CODE",
            "name_field": "GM_NAAM",
            "cls": "apps.locations.models.Gemeente",
        },
        {
            "area_type_code": CBS_WIJK_2022,
            "shp_file": "WijkBuurtkaart_2022_v1/wijk_2022_v1.shp",
            "code_field": "WK_CODE",
            "name_field": "WK_NAAM",
            "cls": "apps.locations.models.Wijk",
            "related_code_field": "GM_CODE",
            "related_field": "gemeente",
            "related_cls": "apps.locations.models.Gemeente",
            "related_rerea_type_code": CBS_GEMEENTE_2022,
        },
        {
            "area_type_code": CBS_BUURT_2022,
            "shp_file": "WijkBuurtkaart_2022_v1/buurt_2022_v1.shp",
            "code_field": "BU_CODE",
            "name_field": "BU_NAAM",
            "cls": "apps.locations.models.Buurt",
            "related_code_field": "WK_CODE",
            "related_field": "wijk",
            "related_cls": "apps.locations.models.Wijk",
            "related_rerea_type_code": CBS_WIJK_2022,
        },
    ]

    def __init__(self, **options):
        # Data downloaded / processed here. Caller is responsible to clean-up directory.
        self.directory = options["dir"]

    def load(self):
        super().load()

        for di in self.DATASET_INFO:
            type_string = di.get("area_type_code")
            area_type, _ = AreaType.objects.get_or_create(
                code=type_string,
                defaults={
                    "name": type_string,
                    "description": f'{type_string} from CBS "Wijk- en buurtkaart" data.',
                },
            )
            self._load_shape_data(di, area_type)
