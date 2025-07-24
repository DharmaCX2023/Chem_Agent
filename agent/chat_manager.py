from agent.selectors.prompt_selector import define_problem
from agent.selectors.prompt_recaller import recall_knowledge
from agent.tools import patent_search, web_search
import openai
from agent.memory import Memory
from agent.planner.tool_executor import execute_plan
from agent.planner.tool_planner import plan_path
import json
from agent.utils.utils import get_identifier_and_properties

inputs, outputs = get_identifier_and_properties()

class ChatManager:
    def __init__(self, api_key, memory: Memory, serpapi_key=None):
        self.memory = memory
        self.serpapi_key = serpapi_key
        self.openai_key = api_key
        self.full_results = []
    def get_response(self, user_query: str):
        self.memory.add_user_message(user_query)
        history = self.memory.get_context(5)
        full_query = f"{history}\nuser:{user_query}"

        print(full_query, "\n-----Chat History-----\n")
        tool_selection = define_problem(full_query, self.openai_key)
        print(tool_selection, "\n-----Keyword Selection-----\n")

        recalled = recall_knowledge(full_query,
                                    tool_selection["chemical"][0],
                                    tool_selection["chemical_identifier_type"][0],
                                    self.openai_key)

        print(recalled, "\n-----Recalled Knowledge\n-----")

        results = []
        for request in tool_selection["properties"]:
            if request in outputs:
                plan = plan_path(recalled[tool_selection["chemical"][0]].keys(), request)
                if isinstance(plan, list):
                    results.append(execute_plan(plan, recalled, tool_selection["chemical"][0]))

        if tool_selection["needs_patent"]:
            results.append(
                patent_search.search_google_patents(tool_selection["patent_search_keywords"][0], self.serpapi_key))
        if tool_selection["needs_web_search"]:
            results.append(web_search.simple_web_search(tool_selection["web_search_keywords"][0], self.openai_key))

        print(results, "\n-----API results\n-----")

        final_answer = self.format_response(tool_selection["properties"],
                                            tool_selection["needs_patent"],
                                            tool_selection["needs_web_search"],
                                            results,
                                            user_query,
                                            self.openai_key)

        self.full_results.append(results)
        self.memory.add_assistant_message(results)
        self.memory.add_assistant_message(final_answer)
        return final_answer

    def format_response(self, properties: list, patent_bool, web_bool, results: list, user_query: str, api_key: str) -> str: #
        openai.api_key = api_key
        system_prompt = (
            "You are a helpful chemistry assistant. Based on the following user query and extracted information, "
            "generate a clean, friendly, and informative answer.\n"
            "Use natural language and clear structure.\n\n"
            "You MUST only include content in the field of chemistry research. \n"

            f"Requirements: "
            f"Here are the retrieved tool results:\n{json.dumps(results)}. \n"
            f"1. You MUST filter the information in retrieved tool results, and only use queried chemical properties: {properties}, "
            f"2. If web search used is true: {web_bool}, show summarise web information and integrate to tyour answer.\n"
            f"3. If the response is similar molecules, give me the SMILES, similarity score and some other knowledge you have about the chemicals. \n"
            f"4. Organize your language in a user friendly format. \n"
            f"5. You MUST not show str(Assistant:) in your answer.\n"
            f"6. If patent search used is true: {patent_bool}, keep the patent titles, inventors and only tell user the status in US, EP and CN. \n"
            f"7. ONLY if {bool('2d_structure' in properties)} is True, use the image url to generate image in your response and merge it into the answer. Otherwise, do not show image at all. \n"
            f"Satisfy all the 1-7 requirements in you answer. \n"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User asked: {user_query}"},
        ]

        try:
            res = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.5,
            )
            return res["choices"][0]["message"]["content"]
        except Exception as e:
            return f" AI formatting failed: {str(e)}"  # tell me aspirin smiles