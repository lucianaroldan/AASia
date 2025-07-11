from typing import Union

def fix_degree_symbols_in_json(data: Union[str, dict]) -> dict:
    """
    Corrige símbolos de grados mal codificados (como 'Â°C' o 'ÃC') dentro de qualifiers en un JSON AAS.
    Acepta un string JSON o un diccionario ya cargado, y devuelve un diccionario corregido.
    """
    if isinstance(data, str):
        data = json.loads(data)

    def fix_qualifier_value(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "qualifiers" and isinstance(value, list):
                    for qualifier in value:
                        if (
                            isinstance(qualifier, dict)
                            and qualifier.get("type") == "UNIT"
                            and isinstance(qualifier.get("value"), str)
                        ):
                            unit = qualifier["value"]
                            if "Â°C" in unit or "ÃC" in unit:
                                qualifier["value"] = unit.replace("Â°C", "°C").replace("ÃC", "°C")
                            if "Â°F" in unit or "ÃF" in unit:
                                qualifier["value"] = unit.replace("Â°F", "°F").replace("ÃF", "°F")
                else:
                    fix_qualifier_value(value)
        elif isinstance(obj, list):
            for item in obj:
                fix_qualifier_value(item)

    fix_qualifier_value(data)
    return data
