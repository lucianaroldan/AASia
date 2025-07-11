import io
from pathlib import Path
from basyx.aas.adapter import json as aas_json, aasx
from basyx.aas import model


def export_aasx_from_json(json_text: str, out_path: Path) -> Path:
    """
    Convierte un texto JSON AAS (IDTA v3.0.x) en un paquete AASX usando BaSyx SDK.
    Devuelve la ruta al archivo .aasx generado.
    """
    # Deserializar JSON al ObjectStore
    store = aas_json.read_aas_json_file(io.StringIO(json_text))
    # Recopilar IDs de los AAS en el entorno
    aas_ids = [obj.id for obj in store if isinstance(obj, model.AssetAdministrationShell)]
    # Contenedor de archivos suplementarios vacío
    file_store = aasx.DictSupplementaryFileContainer()
    # Escribir el paquete AASX
    with aasx.AASXWriter(out_path) as writer:
        for aas_id in aas_ids:
            writer.write_aas(aas_id, store, file_store)
    return out_path