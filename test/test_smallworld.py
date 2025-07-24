import requests
import traceback

def query_smallworld(smiles: str):
    url = "https://sw.docking.org/search/view"
    params = {
        "smi": smiles,
        "db": "REAL-Database-22Q1",
        "start": 0,
        "length": 5,
        "dist": "1-3",
        "async": "true",
    }

    try:
        res = requests.get(url, params=params, timeout=30)  # 增加超时时间到30秒
        res.raise_for_status()
        data = res.json()
        print(data)
        sw_results = []
        for entry in data.get("data", []):
            if not isinstance(entry, list) or len(entry) < 3:
                continue
            mol = entry[0]
            similarity = entry[2]
            sw_results.append({
                "similar_molecules": {
                    "smiles": mol.get("hitSmiles", ""),
                    "zinc_id": mol.get("id", ""),
                    "similarity": similarity
                }
            })
        sw_results.sort(key=lambda x: x["similar_molecules"]["similarity"], reverse=True)

        return sw_results

    except Exception as e:
        print(f"Error querying SmallWorld API: {e}")
        return {"error": f"SmallWorld API error: {e}\n{traceback.format_exc()}"}

if __name__ == "__main__":
    sample_smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"
    results = query_smallworld(sample_smiles)

    if isinstance(results, list) and results:
        print(f"找到 {len(results)} 个相似分子:")
        for i, result in enumerate(results[:5], 1):
            mol = result["similar_molecules"]
            print(f"{i}. SMILES: {mol['smiles']}")
            print(f"   ZINC ID: {mol['zinc_id']}")
            print(f"   相似度: {mol['similarity']}")
            print("-" * 40)
    else:
        print("未找到相似分子或发生错误:", results)
