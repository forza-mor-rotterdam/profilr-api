# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2020 - 2022 Vereniging van Nederlandse Gemeenten, Gemeente Amsterdam
import importlib
import os
import zipfile
from urllib.parse import urlsplit

import requests
from apps.dataset.base import AreaLoader
from apps.locations.models import AreaType
from django.contrib.gis.gdal import DataSource, OGRGeomType
from django.contrib.gis.geos import MultiPolygon
from django.db import transaction


class ShapeBoundariesLoader(AreaLoader):
    DATASET_INFO = {"GENERIC": {}}

    PROVIDES = DATASET_INFO.keys()

    def __init__(self, **options):
        type_string = options["type_string"]
        directory = options["dir"]
        assert type_string in self.PROVIDES

        self.area_type, _ = AreaType.objects.get_or_create(
            code=options["type"],
            defaults={
                "name": options["type"],
                "description": f"{options['type']} data",
            },
        )
        self.directory = directory  # Data downloaded / processed here. Caller is responsible to clean-up directory.
        self.DATASET_URL = options["url"]
        self.data_file = options["shp"]
        self.code_field = options["code"]
        self.name_field = options["name"]

    def _download(self, zip_fullpath):
        """
        Download relevant data file.
        """
        if os.path.exists(zip_fullpath):
            return  # Datafile already downloaded.

        with requests.get(self.DATASET_URL, stream=True, verify=False) as r:
            r.raise_for_status()
            with open(zip_fullpath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    def _unzip(self, zip_fullpath):
        """
        Extract ZIP file to temp_dir.
        """
        with zipfile.ZipFile(zip_fullpath, "r") as zf:
            zf.extractall(path=self.directory)

    def _load_shape_data(self, dataset_info_item, area_type):
        """
        Load shape area as specified area type from the CBS (or compatible format) shapefiles.
        """
        data_fullpath = os.path.join(self.directory, dataset_info_item.get("shp_file"))
        code_field = dataset_info_item.get("code_field")
        name_field = dataset_info_item.get("name_field")

        cls = dataset_info_item.get("cls")
        related_cls = dataset_info_item.get("related_cls")
        related_code_field = dataset_info_item.get("related_code_field")
        related_field = dataset_info_item.get("related_field")
        related_rerea_type_code = dataset_info_item.get("related_rerea_type_code")
        has_related = (
            True if related_cls and related_code_field and related_field else False
        )
        module_name, class_name = cls.rsplit(".", 1)

        area_module = importlib.import_module(module_name)
        area_cls = getattr(area_module, class_name)

        ds = DataSource(data_fullpath)
        geom_by_code = {}

        polygon_type = OGRGeomType("Polygon")
        multipolygon_type = OGRGeomType("MultiPolygon")

        # Collect possible separate geometries representing the area of a single
        # municipality.
        for feature in ds[0]:
            code = feature.get(code_field)
            name = feature.get(name_field)
            geom_by_code[code] = {}
            related_code = None
            if has_related:
                related_code = feature.get(related_code_field)
            geom_by_code[code][related_code_field] = related_code
            geom_by_code[code]["name"] = name if name else code

            # Transform to WGS84 and merge if needed.
            transformed = feature.geom.transform("WGS84", clone=True)
            if geom_by_code[code].get("geometry"):
                geom_by_code[code]["geometry"] = geom_by_code[code]["geometry"].union(
                    transformed
                )
            else:
                geom_by_code[code]["geometry"] = transformed

        # Remove previously imported data, save our merged and transformed boundaries to the DB.
        with transaction.atomic():
            area_cls.objects.filter(_type=area_type).delete()

            for code, data in geom_by_code.items():
                geometry = data.get("geometry")
                if geometry.geom_type == polygon_type:
                    geos_polygon = geometry.geos
                    geos_geometry = MultiPolygon(geos_polygon)
                elif geometry.geom_type == multipolygon_type:
                    geos_geometry = geometry.geos
                else:
                    raise Exception("Expected either polygon or multipolygon.")

                area_module_data = {
                    "name": data["name"],
                    "code": code,
                    "_type": area_type,
                    "geometry": geos_geometry,
                }
                if has_related:
                    related_module_name, related_class_name = related_cls.rsplit(".", 1)
                    related_area_module = importlib.import_module(related_module_name)
                    related_area_cls = getattr(related_area_module, related_class_name)
                    related_instance = related_area_cls.objects.filter(
                        code=data[related_code_field],
                        _type__code=related_rerea_type_code,
                    ).first()
                    if not related_instance:
                        raise Exception(
                            f"An related instance of type {related_cls}, has not been found. code: {data[related_code_field]}, type_code: {related_rerea_type_code}"
                        )

                    area_module_data.update(
                        {
                            related_field: related_instance,
                        }
                    )

                area_cls.objects.create(**area_module_data)

    def load(self):
        split_url = urlsplit(self.DATASET_URL)
        zip_name = os.path.split(split_url.path)[-1]

        zip_fullpath = os.path.join(self.directory, zip_name)

        self._download(zip_fullpath)
        self._unzip(zip_fullpath)
