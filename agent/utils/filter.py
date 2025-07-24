import re

def is_valid_url(url: str) -> bool:
    return isinstance(url, str) and re.match(r'^https?://\S+$', url) is not None

def is_formula(s: str) -> bool:
    return isinstance(s, str) and re.match(r'^[A-Z][a-z]?[0-9₀-₉]*', s) is not None

def is_resolution(s: str) -> bool:
    return isinstance(s, str) and re.match(r'^[0-9.]+ ?Å$', s) is not None

def is_valid_smiles(smiles: str) -> bool:
    if not isinstance(smiles, str):
        return False
    smiles = smiles.strip()
    if not (3 <= len(smiles) <= 200):
        return False
    if any(bad in smiles.lower() for bad in ["http", "unknown", "none", "smiles", "structure"]):
        return False
    pattern = re.compile(r'^[A-Za-z0-9@+\-#=/\\\[\]\(\)%\.]+$')
    return bool(pattern.fullmatch(smiles))

def is_valid_pdb_id(pdb_id: str) -> bool:
    if not isinstance(pdb_id, str):
        return False
    return bool(re.fullmatch(r'^[0-9][A-Za-z0-9]{3}$', pdb_id.strip()))

def is_valid_chemical_name(name: str) -> bool:
    if not isinstance(name, str):
        return False
    name = name.strip().lower()
    if len(name) < 2:
        return False
    if any(bad in name for bad in ["structure", "smiles", "unknown", "n/a", "name:", "compound"]):
        return False
    return True

def is_valid_similar_molecule(entry: dict) -> bool:
    return (
        isinstance(entry, dict) and
        isinstance(entry.get("smiles"), str) and
        isinstance(entry.get("name"), str) and
        isinstance(entry.get("similarity"), (float, int))
    )

def filter_valid_fields(data: dict, chemical, chemical_id) -> dict:
    valid = {}

    for key, value in data.items():
        if key == "chemical_name":
            if is_valid_chemical_name(value):
                valid[key] = value

        elif key == "pdb_id":
            if is_valid_pdb_id(value):
                valid[key] = value.upper()  # optional: force uppercase

        elif key == "smiles":
            if is_valid_smiles(value):
                valid[key] = value

        elif key in {"expression_system", "source_organism", "provenance_details"}:
            if isinstance(value, str) and value.strip():
                valid[key] = value

        elif key == "formula":
            if is_formula(value):
                valid[key] = value

        elif key in {"logP", "logS", "MW", "TPSA"}:
            if isinstance(value, (float, int)):
                valid[key] = float(value)

        elif key == "2d_structure":
            if is_valid_url(value):
                valid[key] = value

        elif key == "resolution":
            if is_resolution(value):
                valid[key] = value

        elif key == "similar_molecules":
            if isinstance(value, list):
                filtered = [entry for entry in value if is_valid_similar_molecule(entry)]
                if filtered:
                    valid[key] = filtered

    valid_ = {chemical: {chemical_id: chemical}}
    valid_[chemical].update(valid)
    return valid_