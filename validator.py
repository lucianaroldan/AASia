from __future__ import annotations
import json, pathlib, requests
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_URL = "https://raw.githubusercontent.com/admin-shell-io/aas-specs/master/schemas/json/aas.json"
CACHE = pathlib.Path.home()/".cache/aas_schema/aas.json"
def _schema():
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True,exist_ok=True)
        data = requests.get(SCHEMA_URL,timeout=30).content
        CACHE.write_bytes(data)
    return json.load(CACHE.open("rb"))

def validate_environment(env: dict):
    Draft202012Validator(_schema(), format_checker=FormatChecker()).validate(env)

    