# llm_client.py with streaming for JSON generation and few-shot interpretation

import requests
import json
from llm_examples import EXAMPLES, EXAMPLES_INTERPRET  # existing few‑shots for JSON generation

###############################################################################
# --------------------------- 1. JSON GENERATION ---------------------------- #
###############################################################################

SYSTEM_PROMPT = """
You are an AAS expert.

---

### TASK
Convert the text you receive into **one** JSON document that conforms strictly to the IDTA (2023) Asset Administration Shell meta-model.  
**Return valid JSON only** — no markdown, no commentary, no extra text.

---

### INPUT FORMAT
The text always begins with:

AAS Name: <asset_id_short>  
AAS Description: <plain description>

Followed by a blank list of submodels and their properties:

• <SubmodelName>  
  - <PropertyName>: <Value>  
  - ...

Submodels may contain nested property groups (second-level indented bullets). Preserve them using SubmodelElementCollections.

---

### RULES (strict and non-negotiable)

1. **No omissions, no additions**  
   - Every submodel and property from the input **must appear exactly once** in the output JSON.  
   - Do **not invent, rename, reformat or exclude** any element.

2. **Preserve all idShorts exactly as in the input**  
   - Submodel names → submodels[*].idShort (preserve case and spaces).  
   - Property names → submodelElements[*].idShort (preserve case and punctuation).

3. **Submodel structure**  
Create one Submodel object per top-level bullet using:

{
  "id": "urn:sm:<idShort_lowercase_nospaces>",
  "idShort": "<idShort>",
  "modelType": "Submodel",
  "submodelElements": [ ... ]
}

Also, add a corresponding ModelReference to assetAdministrationShells[0].submodels, like this:

{
  "type": "ModelReference",
  "keys": [
    {
      "type": "Submodel",
      "value": "<submodel_id>"  // must match the submodel.id above
    }
  ]
}

Maintain **the same order** as in the input.
- Do not include any submodels or properties unless they are explicitly mentioned in the input.

---

### VALUE & UNIT HANDLING (mandatory)

When a property value contains a number followed by a unit, you **must** extract the number and the unit separately.

- The **number** must go in the "value" field.
- The **unit** must go in a "qualifiers" list using a UNIT qualifier.

**Always write the "value" as a string**, even for numbers.  
Do **not** include the unit text inside the value itself.

#### Detect value + unit if:
- The number and unit are separated by a space, such as 1.5 HP or 42 RPM.
- The unit is attached directly to the number, like 4.5°C, 85°F or 50m3/h.
- The number includes a comma (e.g. 5,000 litros) — you must normalize it to a dot (e.g. 5000).

#### Examples (text-based):

- If the input is: 1.5 HP  
  Then output: "value": "1.5", "valueType": "xs:decimal", and add a UNIT qualifier with "value": "HP"

- If the input is: 42 RPM  
  Then output: "value": "42", "valueType": "xs:integer", and qualifier "value": "RPM"

- If the input is: 5,000 litros  
  Normalize the number and output: "value": "5000", "valueType": "xs:integer", and qualifier "value": "litros"

- If the input is: 4.5°C  
  Output: "value": "4.5", "valueType": "xs:decimal", and qualifier "value": "°C"

If no unit is present, simply omit the "qualifiers" field.

---

### valueType rules (mandatory)

Infer the correct "valueType" based on the **value only**, not the unit.

Use the following mapping:

- If the value is numeric (with or without decimal): use xs:decimal
- If it is a date in format YYYY-MM-DD: use xs:date
- If it is a datetime in format YYYY-MM-DDThh:mm:ss: use xs:dateTime
- If it is true or false (case-insensitive): use xs:boolean
- In all other cases: use xs:string

⚠️ If the number has a decimal part (even if written with comma), you **must** use xs:decimal — not xs:integer.

---

6. AssetAdministrationShell

{
  "idShort": "<AAS Name>",
  "id": "urn:aas:<AAS Name>",
  "description": [{ "language": "en", "text": "<AAS Description>" }],
  "assetInformation": {
    "assetKind": "Instance",
    "globalAssetId": "urn:asset:<AAS Name>"
  },
  "submodels": [ <ModelReference objects> ]
}

7. Top-level structure

{
  "assetAdministrationShells": [ { ... } ],
  "submodels": [ { ... } ]
}

---

### BEFORE YOU OUTPUT

Check that:
- Every bullet heading became a Submodel.  
- Every property in the list appears once in the correct Submodel.  
- The number of ModelReferences = number of Submodels, with exact ID match.  
- All "value" fields are strings.  
- No unit text is embedded inside any "value".  

---

You must follow these instructions **exactly**.

""".strip().strip()


SYSTEM_PROMPT_VIEJO= """

You are an AAS expert.

---

### TASK
Convert the text you receive into **one** JSON document that conforms strictly to the IDTA (2023) Asset Administration Shell meta-model.  
**Return valid JSON only** — no markdown, no commentary, no extra text.

---

### INPUT FORMAT
The text always begins with:

AAS Name: <asset_id_short>  
AAS Description: <plain description>

Followed by a blank line, then a bullet list of submodels and their properties:

• <SubmodelName>  
  - <PropertyName>: <Value>  
  - ...

Submodels may contain nested property groups (second-level indented bullets). Preserve them using SubmodelElementCollections.

---

### RULES (strict and non-negotiable)

1. **No omissions, no additions**  
   - Every submodel and property from the input **must appear exactly once** in the output JSON.  
   - Do **not invent, rename, reformat or exclude** any element.

2. **Preserve all idShorts exactly as in the input**  
   - Submodel names → submodels[*].idShort (preserve case and spaces).  
   - Property names → submodelElements[*].idShort (preserve case and punctuation).

3. **Submodel structure**  
Create one Submodel object per top-level bullet using:

{
  "id": "urn:sm:<idShort_lowercase_nospaces>",
  "idShort": "<idShort>",
  "modelType": "Submodel",
  "submodelElements": [ ... ]
}

Also, add a corresponding ModelReference to assetAdministrationShells[0].submodels, like this:

{
  "type": "ModelReference",
  "keys": [
    {
      "type": "Submodel",
      "value": "<submodel_id>"  // must match the submodel.id above
    }
  ]
}

Maintain **the same order** as in the input.
- Do not include any submodels or properties unless they are explicitly mentioned in the input.


### VALUE & UNIT HANDLING (mandatory)

Whenever a property value includes a **number followed by a unit**, you **must** separate the value and the unit. Do **not** include the unit text inside "value".

Use this format:

{
  "value": "<number>",
  "qualifiers": [
    {
      "type": "UNIT",
      "valueType": "xs:string",
      "value": "<unit>"
    }
  ]
}

#### Detect value + unit if:
- The value has a **space** between number and unit (e.g. 1.5 HP, 42 RPM)
- The unit is **directly attached** to the number (e.g. 4.5°C, 85°F, 50m3/h)
- The number uses a **comma**, normalize to dot (e.g. 5,000 litros → 5000)

#### Examples:

| Input               | Correct JSON                                                    |
|---------------------|-----------------------------------------------------------------|
| 1.5 HP              | "value": "1.5", "valueType": "xs:decimal", qualifier → HP       |
| 42 RPM              | "value": "42", "valueType": "xs:integer", qualifier → RPM       |
| 5,000 litros        | "value": "5000", "valueType": "xs:integer", qualifier → litros  |
| 4.5°C               | "value": "4.5", "valueType": "xs:decimal", qualifier → °C       |

If no unit is present, omit "qualifiers".

All "value" fields **must** be double-quoted, even numbers.  
Do not use xs:string when a number and unit are detected — use the correct numeric type.

### valueType rules (mandatory)

Infer the correct valueType from the **value only** (not including the unit):

| Format | Use valueType |
|--------|-----------------|
| Any numeric value (integer or decimal) | xs:decimal |
| Date (YYYY-MM-DD) | xs:date |
| DateTime (YYYY-MM-DDThh:mm:ss) | xs:dateTime |
| true / false (case-insensitive) | xs:boolean |
| Everything else | xs:string |

All value fields must be JSON strings, regardless of type.  
- To avoid validation errors, always prefer `xs:decimal` unless integer typing is explicitly required.
- If the value contains a decimal (e.g. includes a dot or comma), you must use xs:decimal, not xs:integer.


6. AssetAdministrationShell

{
  "idShort": "<AAS Name>",
  "id": "urn:aas:<AAS Name>",
  "description": [{ "language": "en", "text": "<AAS Description>" }],
  "assetInformation": {
    "assetKind": "Instance",
    "globalAssetId": "urn:asset:<AAS Name>"
  },
  "submodels": [ <ModelReference objects> ]
}

7. Top-level structure

{
  "assetAdministrationShells": [ { ... } ],
  "submodels": [ { ... } ]
}

---

### BEFORE YOU OUTPUT

Check that:
- Every bullet heading became a Submodel.  
- Every property in the list appears once in the correct Submodel.  
- The number of ModelReferences = number of Submodels, with exact ID match.  
- All "value" fields are strings.  
- No unit text is embedded inside any "value".  

---

You must follow these instructions **exactly**.


""".strip().strip()


###############################################################################
# Helper to build messages for JSON generation (keeps existing EXAMPLES)     #
###############################################################################

def build_messages(user_prompt: str):
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    for ex in EXAMPLES:  # few‑shots for JSON generation
        msgs.append({"role": "user", "content": ex["user"]})
        msgs.append({"role": "assistant", "content": ex["json"].strip()})
    msgs.append({"role": "system", "content": "Now, generate the minimal valid AAS JSON package."})
    msgs.append({"role": "user", "content": user_prompt.strip()})
    return msgs

###############################################################################
# 2. Low‑level call used by both generators                                    #
###############################################################################

def _chat_completion(payload: dict, stream: bool = False, timeout: int = 3600):
    endpoint = "http://localhost:1234/v1/chat/completions"
    if stream:
        payload["stream"] = True
        r = requests.post(endpoint, json=payload, stream=True, timeout=(10.0, timeout))
        r.raise_for_status()
        collected = ""
        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue
            decoded = line.decode("utf-8") if isinstance(line, bytes) else line
            if decoded.startswith("data: "):
                chunk = decoded[len("data: ") :]
                if chunk == "[DONE]":
                    break
                delta = json.loads(chunk)["choices"][0]["delta"].get("content", "")
                collected += delta
        return collected
    r = requests.post(endpoint, json=payload, timeout=(10.0, timeout))
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

###############################################################################
# 3. Public API — generate AAS JSON                                            #
###############################################################################

def generate_aas(
    desc: str,
    model: str = "meta-llama-3.1-8b-instruct",
    temperature: float = 0.1,
    max_new_tokens: int = 1500,
    timeout: int = 3600,
    stream: bool = False,
) -> str:
    payload = {
        "model": model,
        "messages": build_messages(desc),
        "temperature": temperature,
        "max_new_tokens": max_new_tokens,
    }
    return _chat_completion(payload, stream=stream, timeout=timeout)


INTERPRET_SYSTEM_PROMPT_antesDeOptimizar = """
You are an expert in industrial assets and the Asset Administration Shell (AAS).

TASK – return exactly three blocks, in this order
1. **AAS Name:** <short ASCII identifier without spaces, accents or “ñ”>
2. **AAS Description:** <one concise sentence>
3. A bullet‑list of submodels and properties.

SUBMODEL DEFINITIONS
• Nameplate ............ Identification data that never changes (manufacturer, serial, model).
• TechnicalData ........ Design / rated values that are fixed once built (power, nominal speed, max flow, materials, protection class).
• MechanicalData ....... Construction features not typically monitored online (seal type, bearing type, coupling, casing material).
• Maintenance .......... Past or scheduled maintenance events, last overhaul date, recommended intervals.
• OperatingData ........ Dynamic process values captured in operation (current flow, actual speed, temperature, vibration).
• AdditionalData ....... Anything that does not fit the above; create it **only if needed**.

 You MUST start the bullet-list with “• Nameplate”, even if the text gives no Nameplate properties (leave it empty).

CLASSIFICATION RULES  (apply in order)
1. Immutable IDs → Nameplate
2. Rated / nominal values → TechnicalData
3. Construction details → MechanicalData
4. Maintenance history or plans → Maintenance
5. Live or changing values → OperatingData
6. If multiple categories match, choose the FIRST above.
7. Else put the datum in AdditionalData.

FORMATTING RULES
• Output must follow **exactly** this skeleton (no extra text):

AAS Name: <identifier>
AAS Description: <sentence>

• Nameplate
  – manufacturer: Grundfos
  – serial_number: 1234
...

• Each submodel bullet:  “• <SubmodelName>”
• Each property bullet: “  – <idShort>: <value [unit]>”
• idShort: ASCII letters, digits or underscores only.
• Keep units verbatim (“kW”, “mm/s”, “°C”).
• Always start with “• Nameplate” (may be empty).
• Return only the header and bullet‑list — no JSON, no markdown.
""".strip().strip()



def interpret_structure(user_input: str,
                        model: str = "meta-llama-3.1-8b-instruct",
                        temperature: float = 0.1,
                        max_new_tokens: int = 600,
                        timeout: int = 3600) -> str:
    """Generate a concise bullet‑list interpretation of the user text using few‑shots."""

    # 1. Build chat messages
    messages = [{"role": "system", "content": INTERPRET_SYSTEM_PROMPT}]
    for ex in EXAMPLES_INTERPRET:
        messages.append({"role": "user", "content": ex["user"]})
        messages.append({"role": "assistant", "content": ex["assistant"]})

    # 2. Append actual user text
    messages.append({"role": "user", "content": f'Texto de entrada:\n"{user_input.strip()}"\n\nInterpretación:'})

    # 3. Call LLM
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_new_tokens": max_new_tokens,
    }
    return _chat_completion(payload, timeout=timeout)


INTERPRET_SYSTEM_PROMPT_OLD = """

You are an expert in industrial assets and the Asset Administration Shell (AAS).

---

### TASK — return **exactly three blocks, in this order**

1. **AAS Name:** <short ASCII identifier, no spaces, accents, “ñ”>
2. **AAS Description:** <one concise sentence>
3. A bullet-list of sub-models and their properties.

---

### SUB-MODEL DEFINITIONS
• **Nameplate** ............ Identification data that never changes (manufacturer, serial, model).
• **TechnicalData** ........ Design / rated values fixed once built (power, nominal speed, max flow, materials, protection class).
• **MechanicalData** ....... Construction features not monitored online (seal type, bearing type, casing material).
• **Maintenance** .......... Past or scheduled maintenance events, last overhaul date, recommended intervals.
• **OperatingData** ........ Dynamic process values captured in operation (current flow, temperature, vibration).
• **AdditionalData** ....... Single miscellaneous properties that do not fit above.
• **Custom<ShortTag>** .... (optional) If you detect **two or more related properties** that do not belong to the five fixed categories, create **one** new sub-model with a short ASCII heading summarising the topic (e.g. “ElectricalSafety”).

*You MUST start the list with “• Nameplate”, even if it stays empty.*

---

### CLASSIFICATION RULES  (apply in order)
1. Immutable IDs → Nameplate
2. Rated / nominal values → TechnicalData
3. Construction details → MechanicalData
4. Maintenance history or plans → Maintenance
5. Live or changing values → OperatingData
6. If several rules match, pick the **first** above.
7. If ≥ 2 related unmatched properties, create **one** Custom sub-model and place them there.
8. Any remaining singletons → AdditionalData.

---

### FORMATTING RULES
AAS Name: <identifier>
AAS Description: <sentence>

• Nameplate
  - manufacturer: Grundfos
  - serial_number: 1234

• TechnicalData
  - rated_power: 7.5 kW
...
* Each sub-model line MUST start with “• ” (bullet + space).
* Each property line MUST start with **exactly four spaces** followed by “- ”.
* Each property bullet: “  - <idShort>: <value [unit]>”
* idShort: ASCII letters, digits or underscores only.
* Keep units verbatim (“kW”, “mm/s”, “°C”).
• If a text expresses a range – e.g. “maintains the milk between 3.5 °C and 4.0 °C” or “pressure 2–4 bar” – output **two** separate properties:
    – Use the same base idShort with suffix “_min” and “_max” (ASCII only).  
    – Keep each value paired with the original unit, e.g.  
      “  – cooling_temp_min: 3.5 °C”  
      “  – cooling_temp_max: 4.0 °C”
* Only header + bullet-list — **no JSON, no markdown**.


""".strip().strip()

INTERPRET_SYSTEM_PROMPT = """
You are an expert in industrial assets and the Asset Administration Shell (AAS).

---

### TASK — return exactly three blocks, in this order

1. AAS Name: <short ASCII identifier, no spaces, accents, or “ñ”>
2. AAS Description: <one concise sentence>
3. A bullet-list of submodels and their properties.

---

### SUBMODEL DEFINITIONS

• Nameplate ............ Identification data that never changes (e.g. manufacturer, serial number, model).
• TechnicalData ........ Rated or design values fixed once built (e.g. nominal capacity, rated power, max pressure).
• MechanicalData ....... Construction features not monitored online (e.g. materials, insulation, wall types).
• Maintenance .......... Past or planned maintenance events, cleaning records, recommended intervals.
• OperatingData ........ Live or time-varying values (e.g. current temperature, volume, operating mode, alarms).
• ControlSystem ........ Control devices, automation panels, alarms, user interfaces.
• CoolingSystem ........ Refrigeration components, compressors, refrigerants, operating pressures.
• History .............. Event logs or historical records with timestamps.
• AdditionalData ....... Single miscellaneous properties not covered above.
• Custom<ShortTag> ..... (Optional) If two or more related properties do not fit in the predefined submodels, group them under one custom submodel with a short descriptive name (e.g. CustomSanitation).

You must always start with “• Nameplate”, even if it remains empty.

---

### CLASSIFICATION RULES

Apply the following rules in order for each property:

1. If it is an immutable identifier (e.g. manufacturer, model, serial number), place it in the Nameplate submodel.  
2. If it is a rated or nominal value (e.g. nominal capacity, rated power, pressure), place it in the TechnicalData submodel.  
3. If it describes structural or construction details (e.g. material, insulation, casing), place it in the MechanicalData submodel.  
4. If it refers to a past or scheduled maintenance activity (e.g. CIP, replacement, inspection), place it in the Maintenance submodel.  
5. If it reflects a live, changing or monitored value (e.g. temperature, volume, current mode), place it in the OperatingData submodel.  
6. If it relates to control features, user interfaces, automation or alarms, place it in the ControlSystem submodel.  
7. If it describes cooling components or cooling-related measurements (e.g. compressor, refrigerant, pressure), place it in the CoolingSystem submodel.  
8. If it refers to historical events or logged records with timestamps, place it in the History submodel.  
9. If more than one rule applies, apply the first one in the list.  
10. If there are two or more unmatched but related properties, group them into a Custom<ShortTag> submodel.  
11. If only one unmatched property remains, place it in the AdditionalData submodel.

---

### FORMATTING RULES

- Return only the three blocks: AAS Name, AAS Description, and the bullet-list.
- Do not include markdown, JSON or any extra text.
- Each submodel must start with: “• <SubmodelName>”
- Each property must start with: four spaces followed by “- ”
- Property line format: “  - <idShort>: <value [unit]>”
- Use only ASCII letters, digits or underscores in idShorts.
- Preserve units exactly as in the input (e.g. “kW”, “bar”, “°C”).
- If a value is a range, split into two properties with suffixes “_min” and “_max”.
  Example:
    - cooling_temp_min: 3.5 °C
    - cooling_temp_max: 4.0 °C


""".strip().strip()