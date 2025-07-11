
from typing import List, Dict
"""
Few-shot examples for both LLM tasks.

"""

###############################################################################
# 1)  JSON-GENERATION EXAMPLES  
###############################################################################

EXAMPLES = [
    {
        "user": (
            "- AAS Name: Demo_Asset_001\n"
            "- AAS Description: Demo asset for testing\n"
            "- Submodel Nameplate:\n"
            "  - Manufacturer: ManufacturerX\n"
            "  - Model: ModelY\n"
            "  - SerialNumber: 000000\n"
            "- Submodel OperatingData:\n"
            "  - ExampleMeasurement: 99.9 unitX\n"
            "  - IsRunning: true\n"
        ),
        "json": """{
  "assetAdministrationShells": [
    {
      "idShort": "Demo_Asset_001",
      "id": "urn:asset:demo:001",
      "modelType": "AssetAdministrationShell",
      "description": [{ "language": "en", "text": "Demo asset for testing" }],
      "assetInformation": {
        "assetKind": "Instance",
        "globalAssetId": "urn:asset:demo:001"
      },
      "submodels": [
        {
          "type": "ModelReference",
          "keys": [{ "type": "Submodel", "value": "urn:sm:nameplate" }]
        },
        {
          "type": "ModelReference",
          "keys": [{ "type": "Submodel", "value": "urn:sm:operatingdata" }]
        }
      ]
    }
  ],
  "submodels": [
    {
      "idShort": "Nameplate",
      "id": "urn:sm:nameplate",
      "modelType": "Submodel",
      "submodelElements": [
        {
          "modelType": "Property",
          "idShort": "Manufacturer",
          "valueType": "xs:string",
          "value": "ManufacturerX"
        },
        {
          "modelType": "Property",
          "idShort": "Model",
          "valueType": "xs:string",
          "value": "ModelY"
        },
        {
          "modelType": "Property",
          "idShort": "SerialNumber",
          "valueType": "xs:string",
          "value": "000000"
        }
      ]
    },
    {
      "idShort": "OperatingData",
      "id": "urn:sm:operatingdata",
      "modelType": "Submodel",
      "submodelElements": [
        {
          "modelType": "Property",
          "idShort": "ExampleMeasurement",
          "valueType": "xs:decimal",
          "value": "99.9",
          "qualifiers": [
            {
              "type": "UNIT",
              "valueType": "xs:string",
              "value": "unitX"
            }
          ]
        },
        {
          "modelType": "Property",
          "idShort": "IsRunning",
          "valueType": "xs:boolean",
          "value": "true"
        }
      ]
    }
  ]
}"""
    }
]

EXAMPLES_NOGENERICOS = [

# ---------- Example 1 ----------
    {
    "user": (
        "- AAS Name: Example Asset X1000\n"
        "- AAS Description: Industrial asset ExampleCorp model X1000\n"
        "- Submodel Nameplate:\n"
        "  - ManufacturerName: ExampleCorp\n"
        "  - Model: X1000\n"
        "  - SerialNumber: SN12345678\n"
        "- Submodel OperatingData:\n"
        "  - Temperature: 75 °C\n"
        "  - Load: 1200 kg\n"
        "- Submodel TechnicalData:\n"
        "  - FirmwareVersion: v2.3.4\n"
        "- Submodel AdditionalData:\n"
        "  - Comments: Installed in 2024\n"
        "- Submodel CarbonFootprint:\n"
        "  - CO2Emissions: 5.4 kgCO2/h\n"
        "  - EnergySource: Electric"
    ),
    "json": """{
  "assetAdministrationShells": [
    {
      "idShort": "ExampleAsset_X1000",
      "id": "urn:asset:example:X1000",
      "modelType": "AssetAdministrationShell",
      "administration": { "version": "1", "revision": "0" },
      "description": [ { "language": "en", "text": "Example industrial asset" } ],
      "displayName": [ { "language": "en", "text": "Example Asset X1000" } ],
      "assetInformation": {
        "assetKind": "Instance",
        "globalAssetId": "urn:global:asset:example:X1000",
        "specificAssetIds": [
          { "name": "SerialNumber", "value": "SN12345678" }
        ]
      },
      "submodels": [
        { "type": "ModelReference", "keys": [ { "type": "Submodel", "value": "urn:sm:nameplate" } ] },
        { "type": "ModelReference", "keys": [ { "type": "Submodel", "value": "urn:sm:operating" } ] },
        { "type": "ModelReference", "keys": [ { "type": "Submodel", "value": "urn:sm:technical" } ] },
        { "type": "ModelReference", "keys": [ { "type": "Submodel", "value": "urn:sm:additional" } ] },
        { "type": "ModelReference", "keys": [ { "type": "Submodel", "value": "urn:sm:carbon" } ] }
      ]
    }
  ],
  "submodels": [
    {
      "idShort": "Nameplate",
      "id": "urn:sm:nameplate",
      "modelType": "Submodel",
      "submodelElements": [
        { "modelType": "Property", "idShort": "ManufacturerName", "valueType": "xs:string", "value": "ExampleCorp" },
        { "modelType": "Property", "idShort": "Model",            "valueType": "xs:string", "value": "X1000" },
        { "modelType": "Property", "idShort": "SerialNumber",     "valueType": "xs:string", "value": "SN12345678" }
      ]
    },
    {
      "idShort": "OperatingData",
      "id": "urn:sm:operating",
      "modelType": "Submodel",
      "submodelElements": [
        { "modelType": "Property", "idShort": "Temperature", "valueType": "xs:decimal", "value": "75",
          "qualifiers": [ { "type": "UNIT", "valueType": "xs:string", "value": "°C" } ] },
        { "modelType": "Property", "idShort": "Load",        "valueType": "xs:decimal", "value": "1200",
          "qualifiers": [ { "type": "UNIT", "valueType": "xs:string", "value": "kg" } ] }
      ]
    },
    {
      "idShort": "TechnicalData",
      "id": "urn:sm:technical",
      "modelType": "Submodel",
      "submodelElements": [
        { "modelType": "Property", "idShort": "FirmwareVersion", "valueType": "xs:string", "value": "v2.3.4" }
      ]
    },
    {
      "idShort": "AdditionalData",
      "id": "urn:sm:additional",
      "modelType": "Submodel",
      "submodelElements": [
        { "modelType": "Property", "idShort": "Comments", "valueType": "xs:string", "value": "Installed in 2024" }
      ]
    },
    {
      "idShort": "CarbonFootprint",
      "id": "urn:sm:carbon",
      "modelType": "Submodel",
      "submodelElements": [
        { "modelType": "Property", "idShort": "CO2Emissions", "valueType": "xs:decimal", "value": "5.4",
          "qualifiers": [ { "type": "UNIT", "valueType": "xs:string", "value": "kgCO2/h" } ] },
        { "modelType": "Property", "idShort": "EnergySource", "valueType": "xs:string",  "value": "Electric" }
      ]
    }
  ]
}
"""
    },

    # ---------- Example 2 ----------
    {
    "user": (
        "- AAS Name: Grundfos_CR10_3_872134\n"
        "- AAS Description: Grundfos CR10-3 centrifugal pump\n"
        "- Submodel Nameplate:\n"
        "  - ManufacturerName: Grundfos\n"
        "  - Model: CR10-3\n"
        "  - SerialNumber: 872134\n"
        "- Submodel OperatingData:\n"
        "  - CurrentTemperature: 45 °C\n"
        "- Submodel Maintenance:\n"
        "  - LastStartDateTime: 2025-05-12T14:30:00"
    ),
    "json": """{
  "assetAdministrationShells": [
    {
      "idShort": "Grundfos_CR10_3_872134",
      "id": "urn:asset:grundfos:CR10_3:872134",
      "modelType": "AssetAdministrationShell",
      "administration": { "version": "1", "revision": "0" },
      "description": [ { "language": "en", "text": "Grundfos CR10-3 centrifugal pump" } ],
      "assetInformation": { "assetKind": "Instance", "globalAssetId": "urn:global:asset:grundfos:CR10-3" },
      "submodels": [
        { "type": "ModelReference", "keys": [ { "type": "Submodel", "value": "urn:sm:nameplate" } ] },
        { "type": "ModelReference", "keys": [ { "type": "Submodel", "value": "urn:sm:operating" } ] },
        { "type": "ModelReference", "keys": [ { "type": "Submodel", "value": "urn:sm:maintenance" } ] }
      ]
    }
  ],
  "submodels": [
    {
      "idShort": "Nameplate",
      "id": "urn:sm:nameplate",
      "modelType": "Submodel",
      "submodelElements": [
        { "modelType": "Property", "idShort": "ManufacturerName", "valueType": "xs:string", "value": "Grundfos" },
        { "modelType": "Property", "idShort": "Model",            "valueType": "xs:string", "value": "CR10-3" },
        { "modelType": "Property", "idShort": "SerialNumber",     "valueType": "xs:string", "value": "872134" }
      ]
    },
    {
      "idShort": "OperatingData",
      "id": "urn:sm:operating",
      "modelType": "Submodel",
      "submodelElements": [
        { "modelType": "Property", "idShort": "CurrentTemperature", "valueType": "xs:double", "value": "45",
          "qualifiers": [ { "type": "UNIT", "valueType": "xs:string", "value": "°C" } ] }
      ]
    },
    {
      "idShort": "Maintenance",
      "id": "urn:sm:maintenance",
      "modelType": "Submodel",
      "submodelElements": [
        { "modelType": "Property", "idShort": "LastStartDateTime", "valueType": "xs:dateTime", "value": "2025-05-122025-05-12T14:30:00" }
      ]
    }
  ]
}"""
    },
    # ---------- Example 3 ----------
    {
    "user": (
        "- AAS Name: SKF_CMSS2100\n"
        "- AAS Description: SKF CMSS 2100 vibration sensor\n"
        "- Submodel Nameplate:\n"
        "  - ManufacturerName: SKF\n"
        "  - Model: CMSS 2100\n"
        "- Submodel AdditionalData:\n"
        "  - VibrationRMS: 4.1 mm/s"
    ),
    "json": """{
  "assetAdministrationShells": [
    {
      "idShort": "SKF_CMSS2100",
      "id": "urn:asset:skf:CMSS2100",
      "modelType": "AssetAdministrationShell",
      "assetInformation": { "assetKind": "Instance", "globalAssetId": "urn:global:asset:skf:CMSS2100" },
      "submodels": [
        { "type": "ModelReference", "keys": [ { "type": "Submodel", "value": "urn:sm:nameplate" } ] },
        { "type": "ModelReference", "keys": [ { "type": "Submodel", "value": "urn:sm:additional" } ] }
      ]
    }
  ],
  "submodels": [
    {
      "idShort": "Nameplate",
      "id": "urn:sm:nameplate",
      "modelType": "Submodel",
      "submodelElements": [
        { "modelType": "Property", "idShort": "ManufacturerName", "valueType": "xs:string", "value": "SKF" },
        { "modelType": "Property", "idShort": "Model",            "valueType": "xs:string", "value": "CMSS 2100" }
      ]
    },
    {
      "idShort": "AdditionalData",
      "id": "urn:sm:additional",
      "modelType": "Submodel",
      "submodelElements": [
        { "modelType": "Property", "idShort": "VibrationRMS", "valueType": "xs:double", "value": "4.1",
          "qualifiers": [ { "type": "UNIT", "valueType": "xs:string", "value": "mm/s" } ] }
      ]
    }
  ]
}"""
    }
]

###############################################################################
# 2)  INTERPRETATION EXAMPLES  (bullet-list few-shots in Spanish)
###############################################################################

EXAMPLES_INTERPRET: List[Dict[str, str]] = [

{
    "user": (
        "Texto de entrada:\n"
        "“Robot ABB IRB 6700 con carga 150 kg y alcance 2650 mm. "
        "Controlador IRC5. Sistema de seguridad SICK. "
        "Potencia 8 kW, factor de carga 0.85. "
        "Observación: instalado en 2024.”"
    ),
    "assistant": (
        "AAS Name: ABB_IRB6700\n"
        "AAS Description: Robot industrial ABB IRB 6700\n"
        "• Nameplate\n"
        "    - manufacturer: ABB\n"
        "    - model: IRB_6700\n"
        "• TechnicalData\n"
        "    - payload_capacity: 150 kg\n"
        "    - reach: 2650 mm\n"
        "    - rated_power: 8 kW\n"
        "    - load_factor: 0.85\n"
        "• ControlSystem\n"
        "    - controller_model: IRC5\n"
        "    - safety_device: SICK\n"
        "• Maintenance\n"
        "    - installation_year: 2024"
    )
},
  {
        'user': '''Texto de entrada:
“Tanque de enfriamiento de leche marca Sertec, modelo TEF-5000, número de serie ST-2023-0456. Instalado en febrero de 2024, capacidad nominal 5.000 litros. Temperatura actual: 3.8 °C, rango operativo: 3.5 °C – 4.0 °C. Compresor Frascold FX-40, 10 HP, refrigerante R404A. Presiones: baja 12 bar, alta 18 bar. Última limpieza: 31/05/2025. Próximo mantenimiento: 15/08/2025.”''',
        'assistant': '''AAS Name: Sertec_TEF5000
AAS Description: Tanque de enfriamiento de leche Sertec modelo TEF-5000
• Nameplate
    - manufacturer: Sertec
    - model: TEF_5000
    - serial_number: ST_2023_0456
• TechnicalData
    - nominal_capacity: 5000 litros
• OperatingData
    - current_temperature: 3.8 °C
    - operating_temperature_min: 3.5 °C
    - operating_temperature_max: 4.0 °C
• CoolingSystem
    - compressor_model: Frascold FX-40
    - compressor_power: 10 HP
    - refrigerant_type: R404A
    - pressure_low: 12 bar
    - pressure_high: 18 bar
• Maintenance
    - last_cleaning_date: 2025-05-31
    - next_maintenance_date: 2025-08-15'''
    },
    {
        'user': '''Texto de entrada:
“Sensor de vibración SKF modelo CMSS 2100. Valor RMS: 4.1 mm/s. Incluye módulo de monitoreo continuo serie 3000 instalado en mayo 2025.”''',
        'assistant': '''AAS Name: SKF_CMSS2100
AAS Description: Sensor de vibración SKF CMSS 2100 con monitoreo continuo
• Nameplate
    - manufacturer: SKF
    - model: CMSS_2100
• OperatingData
    - vibration_rms: 4.1 mm/s
• ControlSystem
    - monitoring_module_series: 3000
• Maintenance
    - installation_month: 2025-05'''
    },
    {
        'user': '''Texto de entrada:
“Motor eléctrico WEG modelo X100, 15 HP, velocidad nominal 1470 RPM. Velocidad actual 1425 RPM, temperatura actual 65 °C. Última revisión 15/03/2024.”''',
        'assistant': '''AAS Name: WEG_X100
AAS Description: Motor eléctrico WEG modelo X100 de 15 HP
• Nameplate
    - manufacturer: WEG
    - model: X100
• TechnicalData
    - rated_power: 15 HP
    - rated_speed: 1470 RPM
• OperatingData
    - current_speed: 1425 RPM
    - current_temperature: 65 °C
• Maintenance
    - last_maintenance_date: 2024-03-15'''
    },
]



 


EXAMPLES_INTERPRET_old: List[Dict[str, str]] = [
    # ---------- Few-shot 1 ----------
    {
        "user": (
            "Texto de entrada:\n"
            "“Bomba centrífuga Grundfos CR10-3, fabricante Grundfos, modelo CR10-3, "
            "número de serie 872134. Temperatura actual 45 °C. "
            "Mantenimiento: última puesta en marcha 12/05/2025.”"
        ),
        "assistant": (
            "AAS Name: Grundfos_CR10_3_872134\n"
            "AAS Description: Grundfos CR10-3 centrifugal pump\n"
            "- Nameplate\n"
            "    - ManufacturerName: Grundfos\n"
            "    - Model: CR10_3\n"
            "    - SerialNumber: 872134\n"
            "- OperatingData\n"
            "    - CurrentTemperature: 45 °C\n"
            "- Maintenance\n"
            "    - LastStartDate: 2025-05-12"
        ),
    },
    # ---------- Few-shot 2 ----------
    {
        "user": (
            "Texto de entrada:\n"
            "“Robot ABB IRB 6700 con carga 150 kg y alcance 2650 mm. "
            "Controlador IRC5. Sistema de seguridad SICK. "
            "Submodel: EnergyData — potencia 8 kW, factor de carga 0.85. "
            "Observación: instalado en 2024.”"
        ),
        "assistant": (
            "AAS Name:Robot ABB\n"
            "AAS Description: Robot ABB IRB 6700\n"
            "-  Nameplate\n"
            "    - ManufacturerName: ABB\n"
            "    - Model: IRB_6700\n"
            "- OperatingData\n"
            "    - PayloadCapacity: 150 kg\n"
            "    - ReachMax: 2650 mm\n"
            "- EnergyData\n"
            "    - Power: 8 kW\n"
            "    - LoadFactor: 0.85\n"
            "- SafetySystem\n"
            "    - ScannerType: SICK\n"
            "- AdditionalData\n"
            "    - Comments: Installed in 2024"
        ),
    },
]

