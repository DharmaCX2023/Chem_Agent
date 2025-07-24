import requests
import urllib.parse

def query_pubchem(query: str):
    query_enc = urllib.parse.quote(query.strip())

    url_smiles = (
        f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
        f"{query_enc}/property/CanonicalSMILES/TXT"
    )
    url_props = (
        f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
        f"{query_enc}/property/MolecularFormula,MolecularWeight/JSON"
    )
    url_img = (
        f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
        f"{query_enc}/record/PNG?image_size=large"
    )

    # url_pdb = (
    #     f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
    #     f"{query_enc}/xrefs/PDB/JSON"
    # )

    try:
        # SMILES
        res_smiles = requests.get(url_smiles, timeout=5)
        res_smiles.raise_for_status()
        smiles = res_smiles.text.strip()

        # Formula + Weight
        res_props = requests.get(url_props, timeout=5)
        res_props.raise_for_status()
        props = res_props.json()["PropertyTable"]["Properties"][0]
        formula = props["MolecularFormula"]

        # 2D
        # res_img = requests.get(url_img, timeout=5)
        # res_img.raise_for_status()
        # img_data = res_img.content

        # PDB id
        # res_pdb = requests.get(url_pdb, timeout=5)
        # pdb_json = res_pdb.json()
        # pdbids = pdb_json.get("InformationList", {}).get("Information", [{}])[0].get("PDB", [])

        res = {
            "smiles": smiles,
            "molecular formula": formula,
            "2d structure": {"image": str(url_img)},
            #I need 2d structure of aspirin
        }

        return res

    except Exception as e:
        return {"error": f"PubChem query failed for {query}: {e}"}