import openai
import time
from agent.utils.utils import get_identifier_and_properties

inputs, outputs = get_identifier_and_properties()

def define_problem(user_query: str, api_key: str) -> dict:
    openai.api_key = api_key
    system_prompt = f"""
You are a chemistry assistant tool selector.

Your job is to analyze the user's question or dialogue history, and output a structured Json object indicating:
1. Which chemical or molecule identifier is mentioned. Only choose one. (by chemical name, SMILES, or pdb_id).
2. Recognize the type of the chemical identifier. It can be one of them: {inputs}. 
2. What chemical properties or information are being requested (e.g., smiles, organism source, logP, molecular weight (MW), patents, etc.). 
3. Recognize any known available names or available properties of the mentioned chemical, put the properties into `chemical_known`.
4. Whether web search or patent search is needed and extract search keywords from user query.

Available names:
{inputs}
Available properties: 
{outputs}

Requirements: 
1. Put the chemical name in a list, and put the requested properties in a list as well.  
2. When recognizing names and properties, try to correct misspellings.
3. If there is only key and no value, do not include it in the dict. 
Output Python dict format:
{{   
  "chemical":list [string],
  "chemical_identifier_type":list [string],
  "properties": list[string],
  "needs_web_search": True/False,
  "needs_patent": True/False
  "web_search_keywords": [string]
  "patent_search_keywords": [string]"
}}

Return a valid Python dict without code block markers that can be directly processed with eval(). 
Only if there is no chemicals or properties are found, return an empty dict.
If more than one chemical is found in the query, return an empty dict.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]

    for attempt in range(3):
        try:
            print("trying")
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=messages,
                temperature=0,
            )
            reply = response["choices"][0]["message"]["content"]
            print(reply, "reply")
            return eval(reply)

        except openai.error.RateLimitError as e:
            print("OpenAI Rate Limit:", e)
            time.sleep(2**attempt)
        except Exception as e:
            print("Tool selection failed:", e)
            time.sleep(2)
            return {"error": f"Failed to Find a Chemical Problem."}
