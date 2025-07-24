import re
import streamlit as st
import time

def type_text(text, speed=0.01):
    placeholder = st.empty()
    placeholder.markdown(f"**Assistant:**")
    typed_text = ""
    for char in text:
        typed_text += char
        placeholder.markdown(f"{typed_text}")
        time.sleep(speed)
    return placeholder

def typing(markdown_text):
    image_pattern = r'!\[.*?\]\((.*?)\)'
    parts = re.split(image_pattern, markdown_text)

    for i, part in enumerate(parts):
        if i % 2 == 0:
            if part.strip():
                type_text(part.strip())
        else:
            st.image(part.strip(), caption="Molecular Structure")

from agent.planner.tool_spec import TOOL_SPECS
def get_identifier_and_properties(tool_spec = TOOL_SPECS):
    unique_inputs = set()
    for tool in TOOL_SPECS:
        unique_inputs.update(tool["input"])
    inputs = list(unique_inputs)

    unique_outputs = set()
    for tool in TOOL_SPECS:
        unique_outputs.update(tool["output"])
    outputs = list(unique_outputs)
    return inputs, outputs

def clean_final_answer(answer: str) -> str:
    answer = re.sub(r"(?i)(^|\n)assistant\s*:\s*", "\n", answer)
    return answer.strip()