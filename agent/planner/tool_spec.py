TOOL_SPECS = [
    {
        "name": "query_pubchem",
        "input": ["chemical_name"],
        "output": ["smiles", "formula", "2d_structure"]
    },
    {
        "name": "compute_properties",
        "input": ["smiles"],
        "output": ["logP", "TPSA", "MW", "logS"]
    },
    {
        "name": "query_pdb",
        "input": ["pdb_id"],
        "output": ["source_organism", "expression_system", "resolution", "provenance_details"]
    },
    {
        "name": "query_smallworld",
        "input": ["smiles"],
        "output": ["similar_molecules"]
    }
]