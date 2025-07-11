"""Create human summary from AAS Environment."""
def summarize_environment(env: dict) -> str:
    parts = []
    for sm in env.get("submodels", []):
        parts.append(f"Submodel: {sm.get('idShort','?')}")
        for el in sm.get("submodelElements", []):
            parts.append(f"  • {el.get('idShort','?')} ({el.get('modelType','?')})")
    return "\n".join(parts) if parts else "(No submodels)"