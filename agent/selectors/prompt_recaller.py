import openai
import time
from agent.utils.utils import get_identifier_and_properties
from agent.selectors.recall_path import get_potential_knowledge
from agent.utils.data_spec import DATA_SPECS
from agent.utils.filter import filter_valid_fields

inputs, outputs = get_identifier_and_properties()
knowledge = list(set(inputs + outputs))


def recall_knowledge(history: str, chemical: str, chemical_id: str, api_key: str) -> dict:
    openai.api_key = api_key
    potential_knowledge = get_potential_knowledge(chemical_id)

    # -------- STEP 1: Extract known fields from history --------
    extract_prompt = f"""
    You are a precision-focused chemistry assistant. Your sole task is to extract ONLY information explicitly stated in the conversation history about the molecule "{chemical}".

    **Context**: The user may refer to the molecule by name, SMILES, or PDB ID. Your extraction must be limited to these explicit mentions.

    **Target Fields**: Extract values only for the following fields, if they appear verbatim in {history}:
    {potential_knowledge}

    **Value Format Guidance**: Refer to {DATA_SPECS} to ensure extracted values match the expected type/pattern (e.g., SMILES as a string, logP as a float). If a value’s format does not match, omit the field.

    **Output**: A Python dictionary with keys from the target fields above. Use this structure:
    {{
        "chemical_name": "exact string from history",  # Only if explicitly mentioned
        "smiles": "exact string from history",         # Only if explicitly mentioned
        ...  # Other fields as applicable
    }}

    **Non-Negotiable Rules**:
    1. **NO INVENTION**: If a field is not explicitly stated in {history}, omit it. "Not sure" = omit.
    2. **NO FABRICATION**: Do not paraphrase, infer, or expand on information in {history}. Use exact values.
    3. **NO extras**: No explanations, markdown, or code block markers (e.g., ```). The output must be directly parseable with eval().
    """

    known_fields = _query_openai_once(extract_prompt)

    # -------- STEP 2: Correct Hallucinations --------
    reason_prompt = f"""
    You are a validation assistant. Your task is to purify the extracted data by removing any hallucinated or non-verified fields.

    **Inputs**:
    - Conversation history: {history}
    - Extracted fields: {known_fields} (a dictionary of field-value pairs)

    **Task**: For every key-value pair in {known_fields}, verify that the value is explicitly present in {history}. If a value is not found in {history}, DELETE that key-value pair.

    **Output**: The purified dictionary with only verified key-value pairs. 

    **Rules**:
    1. Do not add new fields or values. Only remove invalid pairs.
    2. Do not modify valid values (keep them exactly as in {known_fields} if verified).
    3. Output must be a raw Python dictionary with no code blocks and parseable with eval().
    """

    known_fields = _query_openai_once(reason_prompt)
    final = filter_valid_fields(known_fields, chemical, chemical_id)

    return final

def _query_openai_once(prompt: str, model: str = "gpt-4o", max_attempts: int = 5):
    for attempt in range(max_attempts):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "system", "content": prompt}],
                temperature=0
            )
            content = response["choices"][0]["message"]["content"]
            print(content, "\n-----Raw OpenAI Output-----")
            return eval(content)
        except openai.error.RateLimitError as e:
            print("Rate limit hit:", e)
            time.sleep(2 ** attempt)
        except Exception as e:
            print("Error during OpenAI call:", e)
            time.sleep(2)
    raise RuntimeError("OpenAI API failed after multiple attempts.")
