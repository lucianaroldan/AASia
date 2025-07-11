import unicodedata
import re
import itertools

_invalid_re = re.compile(r"[^A-Za-z0-9_]")
_start_re  = re.compile(r"^[A-Za-z]")

def _ascii(s: str) -> str:
    """Remove accents and map ñ → n (via NFD → ASCII)."""
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode()

def sanitize_id_short(id_short: str, prepend: str = "A") -> str:
    """
    • Converts to ASCII
    • Replaces hyphens by underscores
    • Removes remaining invalid chars
    • Ensures it starts with a letter (prepend prefix if needed)
    """
    s = _ascii(id_short).replace("-", "_")
    s = _invalid_re.sub("_", s)
    if not _start_re.match(s):
        s = f"{prepend}_{s}"
    return s

def sanitize_aas_json(aas: dict) -> dict:
    """
    Recursively sanitises every 'idShort' field in:
      • assetAdministrationShells
      • submodels
      • submodelElements (and deeper)
    Keeps a map old→new to catch duplicates.
    """
    renames = {}

    # 1. walk & rename
    def _walk(obj):
        if isinstance(obj, dict):
            if "idShort" in obj:
                orig = obj["idShort"]
                new  = sanitize_id_short(orig)
                # avoid duplicate idShorts after sanitizing
                if new in renames.values() and renames.get(orig, new) != new:
                    # append running counter if clash
                    n = 1
                    base = new
                    while f"{base}_{n}" in renames.values():
                        n += 1
                    new = f"{base}_{n}"
                renames[orig] = new
                obj["idShort"] = new
            for v in obj.values():
                _walk(v)
        elif isinstance(obj, list):
            for item in obj:
                _walk(item)
    _walk(aas)

    return aas



def normalize_booleans(aas: dict) -> dict:
    """Convert Sí/Yes/No/etc. to true/false for xs:boolean properties."""
    TRUE_SET  = {"si", "sí", "yes", "true", "verdadero", "1"}
    FALSE_SET = {"no", "false", "falso", "0"}

    def _walk(obj):
        if isinstance(obj, dict):
            if obj.get("modelType") == "Property" and obj.get("valueType") == "xs:boolean":
                raw = str(obj.get("value", "")).strip().lower()
                if raw in TRUE_SET:
                    obj["value"] = "true"
                elif raw in FALSE_SET:
                    obj["value"] = "false"
            for v in obj.values():
                _walk(v)
        elif isinstance(obj, list):
            for item in obj:
                _walk(item)

    _walk(aas)
    return aas



