"""Streamlit UI for the AI-native workshop demo."""

from __future__ import annotations

import streamlit as st

from utils.formatting import extract_section
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
    assignment_placeholder = st.container()
    requirements_placeholder = st.container()
    plan_placeholder = st.container()
    code_placeholder = st.container()
    review_placeholder = st.container()
    next_steps_placeholder = st.container()
    status = st.status("Running workflow...", expanded=True)

    try:
        coordinator = WorkflowCoordinator()
        for step in coordinator.run_incremental(assignment):
            if step.name == "assignment":
                with assignment_placeholder:
                    st.subheader("Assignment")
                    st.write(step.content)
                status.write("Assignment accepted.")
            elif step.name == "planner":
                with requirements_placeholder:
                    st.subheader("Requirements")
                    st.markdown(extract_section(step.content, "Requirements"))
                with plan_placeholder:
                    st.subheader("Plan")
                    st.markdown(extract_section(step.content, "Implementation Steps"))
                status.write("Planner completed.")
            elif step.name == "builder":
                with code_placeholder:
                    st.subheader("Starter Code")
                    st.code(step.content, language="python")
                status.write("Builder completed.")
            elif step.name == "reviewer":
                with review_placeholder:
                    st.subheader("Review")
                    st.markdown(step.content)
                status.write("Reviewer completed.")
            elif step.name == "next_steps":
                with next_steps_placeholder:
                    st.subheader("Final Next Steps")
                    st.markdown(step.content)
                status.write("Next steps prepared.")
    except ValueError as exc:
        status.update(label="Workflow failed", state="error", expanded=True)
        st.warning(str(exc))
    except LLMClientError as exc:
        status.update(label="Workflow failed", state="error", expanded=True)
        st.error(str(exc))
    else:
        status.update(label="Workflow complete", state="complete", expanded=False)
