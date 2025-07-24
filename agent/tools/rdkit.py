from rdkit import Chem
from rdkit.Chem import Descriptors

def compute_properties(smiles: str):
    try:
        mol = Chem.MolFromSmiles(smiles)
        return {
            "MW": round(Descriptors.MolWt(mol), 2),
            "TPSA": round(Descriptors.TPSA(mol), 2),
            "logP": round(Descriptors.MolLogP(mol), 2),
            "logS": round(Descriptors.MolLogP(mol) - 0.5 * Descriptors.MolWt(mol) / 100, 2)
        }
    except Exception as e:
        return {"error": f"RDKit error: {e}"}