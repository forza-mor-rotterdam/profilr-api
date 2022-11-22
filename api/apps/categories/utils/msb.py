from apps.categories.models import Category
from deepdiff import DeepDiff
from django.utils.text import slugify


def sync_categories(onderwerpgroepen):
    existing_main = {
        main.get("external_id"): {
            "external_id": main.get("external_id"),
            "name": main.get("name"),
        }
        for main in Category.objects.filter(
            is_active=True, parent__isnull=True
        ).values()
    }

    new_main = {
        main.get("code"): {
            "external_id": main.get("code"),
            "name": main.get("omschrijving"),
        }
        for main in onderwerpgroepen
    }

    # print(list(existing_main.keys()))
    # print(list(new_main.keys()))

    ddiff_main = DeepDiff(existing_main, new_main, verbose_level=2, view="tree")
    for v in ddiff_main.get("dictionary_item_added", []):
        pl = v.path(output_format="list")
        o = new_main[pl[0]]
        Category.objects.create(**o)
    for v in ddiff_main.get("dictionary_item_removed", []):
        pl = v.path(output_format="list")
        Category.objects.get(external_id=pl[0], parent__isnull=True).delete()
    for v in ddiff_main.get("values_changed", []):
        pl = v.path(output_format="list")
        o = new_main[pl[0]]
        o["slug"] = slugify(o["name"])
        Category.objects.filter(external_id=pl[0], parent__isnull=True).update(**o)

    existing_sub = {
        main.get("external_id"): {
            "parent_id": main.get("parent_id"),
            "external_id": main.get("external_id"),
            "name": main.get("name"),
        }
        for main in Category.objects.filter(
            is_active=True, parent__isnull=False
        ).values()
    }
    new_sub = {
        sub.get("code"): {
            "parent_id": Category.objects.get(
                external_id=main.get("code"), parent__isnull=True
            ).id,
            "external_id": sub.get("code"),
            "name": sub.get("omschrijving"),
        }
        for main in onderwerpgroepen
        for sub in main.get("onderwerpen", [])
    }

    print(existing_sub)
    print(new_sub)

    ddiff_sub = DeepDiff(existing_sub, new_sub, verbose_level=2, view="tree")
    for v in ddiff_sub.get("dictionary_item_added", []):
        pl = v.path(output_format="list")
        o = new_sub[pl[0]]
        Category.objects.create(**o)
    for v in ddiff_sub.get("dictionary_item_removed", []):
        pl = v.path(output_format="list")
        Category.objects.get(external_id=pl[0], parent__isnull=False).delete()
    for v in ddiff_sub.get("values_changed", []):
        pl = v.path(output_format="list")
        o = new_sub[pl[0]]
        o["slug"] = slugify(o["name"])
        Category.objects.filter(external_id=pl[0], parent__isnull=False).update(**o)
