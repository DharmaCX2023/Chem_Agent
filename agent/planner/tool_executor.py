from agent.tools.pubchem import query_pubchem
from agent.tools.rdkit import compute_properties
from agent.tools.pdb import query_pdb
from agent.tools.smallworld import query_smallworld
from agent.planner.tool_spec import TOOL_SPECS

TOOL_IMPLS = {
    "query_pubchem": lambda inputs: query_pubchem(inputs["chemical_name"]),
    "compute_properties": lambda inputs: compute_properties(
        smiles=inputs.get("smiles")
    ),
    "query_pdb": lambda inputs: query_pdb(inputs["pdb_id"]),
    "query_smallworld": lambda inputs: query_smallworld(inputs["smiles"])
}

def execute_plan(plan, initial_inputs, chemical_id, tool_specs = TOOL_SPECS):
    context = dict(initial_inputs)
    known = list(context[chemical_id].keys())
    print(plan, "\n-----Planning...\n-----")

    for step in plan:
        tool = step["use"]
        input_keys = [k for k in next(spec["input"] for spec in tool_specs if spec["name"] == tool) if k in known][:1] #[k for k in candidate_inputs if k in context]
        input_key = input_keys[0]
        input_kwargs = {input_key: context[chemical_id][input_key]}
        result = TOOL_IMPLS[tool](input_kwargs)
        known.extend(result)
        context[chemical_id].update(result)
    return context