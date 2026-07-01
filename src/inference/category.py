from src.models.registry import registry

def get_category(aqi: float) -> str:

    for item in registry.category_mapping:
        if aqi <= item["max"]:
            return item["category"]

    return registry.category_mapping[-1]["category"]