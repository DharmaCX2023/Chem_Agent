from agent.planner.tool_spec import TOOL_SPECS


def plan_path(initial_inputs: list, target_output: str):
    from copy import deepcopy
    print(target_output, initial_inputs, "\n-----Initial and Target\n-----")
    best_plan = None
    shortest_len = float("inf")
    max_iterations = 5
    iteration_count = 0

    def dfs(available, plan):
        nonlocal best_plan, shortest_len, iteration_count

        iteration_count += 1
        if iteration_count > max_iterations:
            return

        if target_output in available:
            if len(plan) < shortest_len:
                best_plan = deepcopy(plan)
                shortest_len = len(plan)
            return

        for tool in TOOL_SPECS:
            name = tool["name"]
            inputs = set(tool["input"])
            outputs = set(tool["output"])

            if any(req in available for req in inputs) and not outputs.issubset(available):
                new_available = available | outputs
                new_plan = plan + [{"use": name}]
                dfs(new_available, new_plan)

    dfs(set(initial_inputs), [])

    if best_plan is None:
        return (f"Error: not possible to find {target_output} from given inputs within {max_iterations} iterations.")
    return best_plan

