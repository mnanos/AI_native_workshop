"""Streamlit UI for the AI-native workshop demo."""

from __future__ import annotations

import streamlit as st

from utils.llm import LLMClientError
from workflow import WorkflowCoordinator


st.set_page_config(page_title="AI-Native Workshop Demo", layout="centered")

st.title("AI-Native Workshop Demo")
st.caption("A small AI Lab Assistant that shows a prompt, a workflow, and role-based agents.")

st.write(
    "Paste a short technical assignment, then run the deterministic workflow: "
    "Planner -> Builder -> Reviewer."
)

assignment = st.text_area(
    "Assignment",
    height=180,
    placeholder="Example: Build a Python program that reads sensor measurements from a CSV file...",
)

if st.button("Run Workflow", type="primary"):
    try:
        result = WorkflowCoordinator().run(assignment)
    except ValueError as exc:
        st.warning(str(exc))
    except LLMClientError as exc:
        st.error(str(exc))
    else:
        st.subheader("Assignment")
        st.write(result.assignment)

        st.subheader("Requirements")
        st.markdown(result.requirements)

        st.subheader("Plan")
        st.markdown(result.plan)

        st.subheader("Starter Code")
        st.code(result.starter_code, language="python")

        st.subheader("Review")
        st.markdown(result.review)

        st.subheader("Final Next Steps")
        st.markdown(result.next_steps)
