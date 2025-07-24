import requests
import traceback

def query_smallworld(smiles: str):
    url = "https://sw.docking.org/search/view"
    params = {
        "smi": smiles,
        "db": "REAL-Database-22Q1",
        "start": 0,
        "length": 20,
        "dist": "1-3",
        "async": "true",
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        sw_results = []
        for entry in data.get("data", []):
            if not isinstance(entry, list) or len(entry) < 3:
                continue
            mol = entry[0]
            similarity = entry[2]
            sw_results.append({
                "similar_molecules":
                    {"smiles": mol.get("hitSmiles", ""),
                     "zinc_id": mol.get("id", ""),
                     "similarity": similarity}
            })
            sw_results.sort(key=lambda x: x["similar_molecules"]["similarity"], reverse=True)
        sw_result_dict = {
            item["similar_molecules"]["smiles"]: item["similar_molecules"]["similarity"]
            for item in sw_results[:5]
        }
        print(sw_result_dict, "swdict")
        return sw_result_dict

    except Exception as e:
        print(f"error SmallWorld /view API error")
        return {"error": f"SmallWorld /view API error: {e}\n{traceback.format_exc()}"}
        # similar molecules to CC(=O)OC1=CC=CC=C1C(=O)O
