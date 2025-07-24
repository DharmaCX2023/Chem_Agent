from agent.planner.tool_spec import TOOL_SPECS

def get_potential_knowledge(initial, tools= TOOL_SPECS):
    known = []
    known.append(initial)
    for _ in range(3):
        for tool in tools:
            if any(req in known for req in tool["input"]):
                known.extend(tool["output"])
    return list(set(known))