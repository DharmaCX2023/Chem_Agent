# import openai
# import time
# from agent.utils.utils import get_identifier_and_properties
#
# inputs, outputs = get_identifier_and_properties()
# knowledge = list(set(inputs + outputs))
#
# def recall_knowledge(history: str, chemical: str, chemical_id: str, api_key: str) -> dict:
#     openai.api_key = api_key
#
#     recaller_prompt = f"""
#     You are a chemistry assistant that reads conversation history and extracts all currently known or derivable information about a target molecule: "{chemical}".
#
#     The user may refer to chemicals using chemical names, SMILES, or PDB IDs.
#
#     ---
#
#     STEP 1 — Determine what chemical the user refers to. This may involve matching identifiers like smiles, pdb_id, or chemical name.
#
#     STEP 2 — Using the available information, identify which fields are already known. Known data may include:
#     {knowledge}
#
#     STEP 3 — Using tool capabilities below, reason about what other fields can be derived (but not yet known):
#
#     Tool Capabilities:
#     - If you have `chemical_name`, you can get: smiles, formula, 2D structure.
#     - If you have `smiles`, you can get: logP, TPSA, MW, logS, similar molecules, similarity scores.
#     - If you have `pdb_id`, you can get: source_organism, expression_system, resolution, provenance_details.
#     ---
#
#     DO NOT fabricate any values.
#     Only include values if:
#     - They are explicitly present in the conversation history:
#     {history}
#
#
#     If a value is *not* yet known, you MUST NOT include it in the output.
#     If a field is derivable (e.g. logP from SMILES), you may infer the value.
#     If you make up or hallucinate ang fields, the output will be discarded.
#     ---
#
#     Your Task:
#     - Step by step, reason out what information is already known.
#     - Based on the known fields, determine what other information can be inferred.
#     - Then return a valid Python dictionary like below:
#
#     Output Format by using keys lists in {knowledge}:
#     {{
#       "{chemical}": {{
#         "chemical_name": "...",   # already known
#         "smiles": "...",          # inferred or known
#         "logP": "...",            # inferred if possible
#         ...
#       }}
#     }}
#
#     Check the dict values one by one. If the values are not correct, remove the pair from dict.
#     for example: 2d structure has to be a dict of image url; logP has to contain a float.
#
#     - Only include fields that are known or inferable based on the tool capability list.
#     - Discard invalid pairs with values such as "..." in the dict.
#     - Do NOT include markdown, explanation, or commentary.
#     - Just return the dictionary without code block markers that can be directly processed with eval().
#     """
#
#     messages = [
#         {"role": "system", "content": recaller_prompt},
#     ]
#
#     for attempt in range(5):
#         try:
#             response = openai.ChatCompletion.create(
#                 model="gpt-4o",
#                 messages=messages,
#                 temperature=0
#             )
#             content = response["choices"][0]["message"]["content"]
#             print(content, "recall debug")
#             return eval(content)
#
#         except openai.error.RateLimitError as e:
#             print("OpenAI Rate Limit:", e)
#             time.sleep(2**attempt)
#         except Exception as e:
#             print("Knowledge recall failed:", e)
#             time.sleep(2)
#     raise RuntimeError("Knowledge recall failed: aborting...")

# f"""
#     You are a chemistry assistant that reads the full conversation history.
#     Your task is to extract what we already know about the mentioned chemical: {chemical} from the user history: {history}, even if only the name (e.g. "aspirin") is mentioned.
#     If a chemical name is stated but other fields like SMILES or formula are missing, include only `"chemical_name"` in the output.
#     Do not skip any chemical mentions.
#
#     Recogonise any of the following chemical identifiers or properties in dialogue:
#     {knowledge}
#
#     NOTE that chemical name, SMILES and PDB_ids do not necessarily appear in previous dialogues. But one of the identifier must be
#
#     Output format is:
#     {{
#       "aspirin": {{
#         "chemical_name": "aspirin",
#         "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
#         "formula": "C9H8O4",
#         "pdb_id": "3LVP",
#         "logP": [float],
#         "logS": [float],
#         "prevenance details": [string]
#       }},
#       "paracetamol": {{
#         "chemical_name": "paracetamol",
#         "smiles": "CC(=O)NC1=CC=C(O)C=C1"
#       }}
#     }}
#
#     Return a valid Python dict without code block markers that can be directly processed with eval().
#     """

# recaller_prompt = f"""You are a chemistry assistant that reads the full conversation history and extracts what is already known about each mentioned chemical.
#
# The user may refer to chemicals using chemical names, SMILES, or PDB IDs.
#
# Below is a list of tools available to you and the fields they can infer:
#
# Tool Capabilities:
# - If you have `chemical_name`, you can get: smiles, formula, 2D structure.
# - If you have `smiles`, you can get: logP, TPSA, MW, logS, similar molecules, similarity scores.
# - If you have `pdb_id`, you can get: source_organism, expression_system, resolution, provenance_details.
#
# Use these relationships to infer what can be derived from the given chemical_identifier: {chemical_id}.
#
# Return a dictionary where the key is a molecule identifier (usually chemical name or pdb_id or smiles),
# and value is a dict of all known or inferable fields for that molecule.
#
# If a field is not yet known and cannot be derived, do not include it.
#
# Use only valid Python dictionary. No markdown, no explanation.
#
# History:
# {history}
#
# Queried Identifier is:
# {chemical_id}
#
# Create an output dict start with the chemical and relevant information in following format:
#     {{
#       "{chemical}": {{
#         {chemical_id}: "{chemical}",
#         "other_knowledge, it can be logP, TPSA, MW, logS, similar molecules, similarity scores": "values of the knowledge"
#       }},
#     }}
#
# Include the chemical identifier itself in the output dict.
# Only include those properties and identifiers if you can find a value in the chat history.
# Only return recalled knowledge that is related to the the queried chemical identifier.
# Return a valid Python dict without code block markers that can be directly processed with eval().
# """

#     extract_prompt = f"""
# You are a chemistry assistant. Your only task is to extract known information from the conversation history about the molecule "{chemical}".
# The user may refer to it by name, SMILES, or PDB ID.
#
# Known fields to extract (if explicitly mentioned in the history):
# {potential_knowledge}
#
# Learn a sample data specification, try to understand what are the proper value to  add into the dict: {DATA_SPECS}
# YOu should only put in data of similar type or pattern into the dict according to the data specification.
#
# Output a Python dict using this format:
# {{
#     "chemical_name": "string",   # Only if explicitly mentioned
#     "smiles": "string",          # Only if explicitly mentioned
#     ...
#   }}
# }}
#
# Rules:
# - Do NOT invent any values.If you are not sure, ommit that field.
# - Do NOT fabricate anything that are not in {history}.
# - Do NOT include explanation or markdown.
# - Return the dictionary without code block markers that can be directly processed with eval().
# """

# reason_prompt = f"""
# You are a chemistry assistant. Your task is to check the hallucination in previous response.
#
# Rules:
# - Compare history: {history} and known fields: {known_fields}, remove any pairs that are in known field but not in chat history.
# - Return the dictionary without code block markers that can be directly processed with eval().
# """

# ## Developer Guidance
#
# ### Section1. System Overview
# The system is
# The system consists of an API planner to obtain requested chemical properties by using appropriate tool chains.
# To add new properties to the planner, simple modify the tool_specs.py.
#
# ### Section2. API handling
#
#
# ### Section3. Design Decisions
# Tool planner is used to design the shortest path to obtain queried properties from
#
# ### Section4. Knowledge Limitations
# 1. Cannot search more than one item at one time.
# 2. Number of patent and web search results are defined in the functions.
# Therefore, queries such as "help me find more relevant patents" are useful but not supported.
#
# ### Section5. Useful Tips for Developers
# To add new properties to the planner, simple modify the agent/planner/tool_specs.py.
# The new properties will be used by the APIs and tool chains and integrated into the assistant's response.

maps = [
  "ChemspaceBB_202408.smi.anon",
  "Enamine-SC-Stock-Mar2022.smi.anon",
  "MculeUltimate-20Q2.smi.anon",
  "REAL-Database-22Q1.smi.anon",
  "ZINC20-All-25Q2.smi.anon",
  "all-zinc.smi.anon",
  "in-stock-25Q2.smi.anon",
  "informer-set.smi.anon",
  "interesting.smi.anon",
  "mcule-v.smi.anon",
  "mcule.smi.anon",
  "mcule_full.smi.anon",
  "mcule_purchasable_virtual_230121.smi.anon",
  "old-in-stock.smi.anon",
  "wait-ok-25Q2.smi.anon",
  "wuxi_23Q1.smi.anon",
  "zinc20-forsale-25Q2.smi.anon"
]