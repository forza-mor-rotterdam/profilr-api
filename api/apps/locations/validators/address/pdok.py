from apps.locations.validators.address.base import (
    AddressValidationUnavailableException,
    BaseAddressValidation,
)
from django.conf import settings
from django.http import QueryDict
from requests import get
from requests.exceptions import RequestException


class PDOKAddressValidation(BaseAddressValidation):
    address_validation_url = f"{settings.PDOK_API_URL}/locatieserver/v3/suggest"

    def _search_result_to_address(self, result):
        mapping = {
            # PDOK_key: sia_key,
            "straatnaam": "straatnaam",
            "postcode": "postcode",
            "huisnummer": "huisnummer",
            "huisletter": "huisletter",
            "huisnummertoevoeging": "huisnummertoevoeging",
            "woonplaatsnaam": "woonplaatsnaam",
        }

        sia_address_dict = {}
        for PDOK_key, sia_key in mapping.items():
            sia_address_dict[sia_key] = result[PDOK_key] if PDOK_key in result else ""
        sia_address_dict["geometrie"] = result["centroide_ll"]
        sia_address_dict["buurt_code"] = result["buurtcode"]
        # sia_address_dict["wijk_code"] = result["wijkcode"]
        return sia_address_dict

    def _pdok_request_query_params(self, address, lon=None, lat=None):
        query_dict = QueryDict(mutable=True)
        query_dict.update({"fl": "*"})
        query_dict.update({"rows": "5"})
        query_dict.update({"fq": "bron:BAG"})
        query_dict.update({"fq": "type:adres"})

        if "woonplaats" in address and address["woonplaats"].strip():
            query_dict.update({"fq": f'woonplaatsnaam:{address["woonplaats"].strip()}'})
        if "postcode" in address and address["postcode"].strip():
            query_dict.update({"fq": f'postcode:{address["postcode"].strip()}'})

        # remove '', ' ' strings before formatting
        cleaned_pdok_list = filter(
            lambda item: item, map(str.strip, settings.DEFAULT_PDOK_MUNICIPALITIES)
        )
        query_dict.update(
            {"fq": f"""gemeentenaam:("{'" "'.join(cleaned_pdok_list)}")"""}
        )

        straatnaam = address["openbare_ruimte"].strip()
        huisnummer = str(address["huisnummer"]).strip()
        huisletter = (
            address["huisletter"].strip()
            if "huisletter" in address and address["huisletter"]
            else ""
        )
        toevoeging = (
            f'-{address["huisnummer_toevoeging"].strip()}'
            if "huisnummer_toevoeging" in address and address["huisnummer_toevoeging"]
            else ""
        )  # noqa

        if lon and lat:
            query_dict.update({"lon": lon, "lat": lat})

        query_dict.update({"q": f"{straatnaam} {huisnummer}{huisletter}{toevoeging}"})

        return query_dict

    def _search(self, address, lon=None, lat=None, *args, **kwargs):
        try:
            query_params = self._pdok_request_query_params(
                address=address, lon=lon, lat=lat
            )
            response = get(f"{self.address_validation_url}?{query_params.urlencode()}")
            print(response.json().get("response", {}).get("docs", [])[0])
            response.raise_for_status()
        except RequestException as e:
            raise AddressValidationUnavailableException(e)
        return response.json()["response"]["docs"]
