from __future__ import annotations

from .core import *


def render_developer_hub(ai_ready: bool) -> None:
    stack_profile = developer_stack_profile()
    with st.container(border=True):
        render_card_header(
            PAGE_DETAILS["developer"]["title"],
            "Keep code generation and debugging separate from the academic tools, with one focused workflow visible at a time.",
            "Developer Suite",
            anchor="DV",
            tier="primary",
        )
        render_kpi_row(
            [
                ("Active model", current_model_name() or "No active model"),
                ("Stack profile", str(stack_profile["profile_name"])),
                ("Code focus", "High" if stack_profile["is_coder_model"] else "Moderate"),
            ]
        )
        with st.expander("Capability context", expanded=False):
            st.caption(stack_profile["note"])

    fix_tab, generator_tab, stack_tab, selftest_tab, compare_tab, diff_tab, notes_tab = st.tabs(
        ["Code Fixer", "Code Generator", "Stack Guide", "Self-Test", "Model Compare", "Code Diff View", "Debug Notes"]
    )

    with fix_tab:
        selected_fix_stack, selected_fix_level = resolve_stack_choice(
            st.session_state.codefix_stack_profile,
            st.session_state.codefix_custom_stack,
        )
        left, right = st.columns([1.02, 0.98], gap="large")
        with left:
            with st.container(border=True):
                render_card_header(
                    "Code Fix Builder",
                    "Paste the failing code, choose the target stack, and add the error or symptom. The stack list is filtered for what the current model is more likely to handle well.",
                    "Compose",
                )
                st.text_input("Issue title (optional)", key="codefix_title")
                st.selectbox(
                    "Tech stack",
                    options=stack_profile["ordered_options"],
                    key="codefix_stack_profile",
                )
                if st.session_state.codefix_stack_profile == "Custom":
                    st.text_input("Custom stack", key="codefix_custom_stack")
                render_route_block("Stack fit", f"{selected_fix_stack}\n{stack_confidence_message(selected_fix_level)}")
                st.text_area("Error message or symptoms", key="codefix_error", height=120)
                st.text_area("Code snippet", key="codefix_source", height=220)
                st.text_area("Expected behavior (optional)", key="codefix_expectation", height=95)
                action_a, action_b = st.columns(2, gap="small")
                if action_a.button("Generate Code Fix", key="developer_codefix_generate", use_container_width=True, type="primary", disabled=not ai_ready):
                    title = st.session_state.codefix_title.strip()
                    language = selected_fix_stack or "Code"
                    error_text = st.session_state.codefix_error.strip()
                    source = st.session_state.codefix_source.strip()
                    expectation = st.session_state.codefix_expectation.strip()
                    st.session_state.codefix_language = language
                    if not source:
                        st.warning("Paste the code snippet before generating a fix.")
                    elif not error_text:
                        st.warning("Add the error message or symptoms before generating a fix.")
                    else:
                        prompt = (
                            "Fix the following code issue for study and debugging support.\n\n"
                            f"Language or stack: {language}\n"
                            f"Stack confidence level: {selected_fix_level}\n"
                            f"Issue title: {title or 'No title provided'}\n"
                            f"Error message or symptoms:\n{error_text}\n\n"
                            f"Code snippet:\n{source}\n\n"
                            f"Expected behavior:\n{expectation or 'Not provided'}\n\n"
                            "Return these plain-text sections in this exact order:\n"
                            "Issue Summary:\n"
                            "Root Cause:\n"
                            "Fixed Version:\n"
                            "Why It Works:\n"
                            "Next Checks:\n"
                        )
                        result = run_generation(prompt, "code fix")
                        if result:
                            st.session_state.codefix_response = result
                            remember_output("Code Fix", title or f"{language} Code Fix", result, "developer", "codefix")
                            st.success("Code fix ready.")
                if action_b.button("Clear Code Fixer", key="developer_codefix_clear", use_container_width=True):
                    queue_reset("clear_codefix_workspace", "Code fixer workspace cleared.")
                    st.rerun()
        with right:
            with st.container(border=True):
                render_preview_panel(
                    "Code Fix Preview",
                    "The fix, explanation, and next checks appear here.",
                    "Fixed result",
                    st.session_state.codefix_response,
                    height=430,
                    empty_title="No code fix yet",
                    empty_body="Generate the fix from the left panel first. The preview and export controls will appear only when there is a real debugging result to inspect.",
                    anchor="FX",
                    tier="secondary",
                )
                if st.session_state.codefix_response.strip():
                    export_title = st.session_state.codefix_title.strip() or f"{selected_fix_stack or 'Code'} Code Fix"
                    render_download_button(
                        export_title,
                        st.session_state.codefix_response,
                        sanitize_filename(export_title.lower().replace(" ", "_")),
                        "codefix",
                        "clear_codefix_workspace",
                    )

    with generator_tab:
        selected_codegen_stack, selected_codegen_level = resolve_stack_choice(
            st.session_state.codegen_stack_profile,
            st.session_state.codegen_custom_stack,
        )
        left, right = st.columns([1.02, 0.98], gap="large")
        with left:
            with st.container(border=True):
                render_card_header(
                    "Code Generator",
                    "Describe what you want built, or upload reference documents and notes so the model can infer the target without a long manual description.",
                    "Compose",
                )
                st.text_input("Project or file title", key="codegen_title")
                st.selectbox(
                    "Target stack",
                    options=stack_profile["ordered_options"],
                    key="codegen_stack_profile",
                )
                if st.session_state.codegen_stack_profile == "Custom":
                    st.text_input("Custom target stack", key="codegen_custom_stack")
                render_route_block("Stack fit", f"{selected_codegen_stack}\n{stack_confidence_message(selected_codegen_level)}")
                st.text_area("Build description (optional if references already explain the task)", key="codegen_description", height=130)
                st.text_area("Expected output or constraints", key="codegen_expectation", height=100)
                st.file_uploader(
                    "Reference documents",
                    type=["docx", "pdf", "txt", "md"],
                    accept_multiple_files=True,
                    key="codegen_reference_docs",
                )
                st.file_uploader(
                    "Reference images",
                    type=["png", "jpg", "jpeg", "webp"],
                    accept_multiple_files=True,
                    key="codegen_reference_images",
                )
                st.text_area(
                    "Attachment note (use this if the images need extra explanation)",
                    key="codegen_attachment_note",
                    height=88,
                )
                action_a, action_b = st.columns(2, gap="small")
                if action_a.button("Generate Code", key="developer_codegen_generate", use_container_width=True, type="primary", disabled=not ai_ready):
                    title = st.session_state.codegen_title.strip() or f"{selected_codegen_stack} Generator"
                    description = st.session_state.codegen_description.strip()
                    expectation = st.session_state.codegen_expectation.strip()
                    doc_files = st.session_state.get("codegen_reference_docs") or []
                    image_files = st.session_state.get("codegen_reference_images") or []
                    reference_bundle, issues = read_codegen_reference_bundle(
                        doc_files,
                        image_files,
                        st.session_state.codegen_attachment_note,
                    )
                    for issue in issues:
                        st.warning(issue)
                    if not description and not reference_bundle:
                        st.warning("Add a build description or upload at least one reference file.")
                    else:
                        prompt = (
                            "Generate code or project scaffolding for the user's request.\n\n"
                            f"Target stack: {selected_codegen_stack}\n"
                            f"Stack confidence level: {selected_codegen_level}\n"
                            f"Project title: {title}\n"
                            f"Build description:\n{description or 'Infer the goal from the attached references.'}\n\n"
                            f"Expected output or constraints:\n{expectation or 'No extra constraints provided.'}\n\n"
                            f"Reference material:\n{trim_prompt_source(reference_bundle) if reference_bundle else 'No attachments provided.'}\n\n"
                            "Return these plain-text sections in this exact order:\n"
                            "Solution Summary:\n"
                            "Generated Code:\n"
                            "Setup Notes:\n"
                            "Next Steps:\n"
                        )
                        result = run_generation(prompt, "code generator output")
                        if result:
                            st.session_state.codegen_response = result
                            remember_output("Code Generator", title, result, "developer", "codegen")
                            st.success("Code output ready.")
                if action_b.button("Clear Code Generator", key="developer_codegen_clear", use_container_width=True):
                    queue_reset("clear_codegen_workspace", "Code generator cleared.")
                    st.rerun()
        with right:
            with st.container(border=True):
                render_preview_panel(
                    "Generated Code Preview",
                    "Review the generated code and notes before exporting or re-prompting.",
                    "Generated code output",
                    st.session_state.codegen_response,
                    height=430,
                    empty_title="No generated code yet",
                    empty_body="Describe the build or attach reference material first. The preview area expands when there is generated code to review.",
                    anchor="CG",
                    tier="secondary",
                )
                if st.session_state.codegen_response.strip():
                    export_title = st.session_state.codegen_title.strip() or f"{selected_codegen_stack} Code Output"
                    render_download_button(
                        export_title,
                        st.session_state.codegen_response,
                        sanitize_filename(export_title.lower().replace(" ", "_")),
                        "codegen",
                        "clear_codegen_workspace",
                    )

    with stack_tab:
        with st.container(border=True):
            render_card_header(
                "Stack Fit Guide",
                "This guide keeps the developer tools honest about what the current model is more likely to handle well.",
                "Capability Profile",
            )
            render_meta_grid(
                [
                    ("Active model", current_model_name() or "No active model"),
                    ("Profile", stack_profile["profile_name"]),
                    ("Code focus", "High" if stack_profile["is_coder_model"] else "Moderate"),
                ]
            )
            st.caption(stack_profile["note"])
            render_route_block("Best fit", "\n".join(stack_profile["best_fit"]))
            render_route_block("Good with review", "\n".join(stack_profile["good_fit"]))
            render_route_block("Manual review strongly advised", "\n".join(stack_profile["low_fit"]))
            st.caption("Reference files are parsed for text documents. Image attachments are kept as references, but this current setup does not perform OCR.")

    with selftest_tab:
        selected_selftest_stack, _selftest_level = resolve_stack_choice(
            st.session_state.selftest_stack_profile,
            st.session_state.selftest_custom_stack,
        )
        left, right = st.columns([1.02, 0.98], gap="large")
        with left:
            with st.container(border=True):
                render_card_header(
                    "Developer Self-Test",
                    "Run a standard coding prompt against the active model for the selected stack so we can check whether the model behaves well before trusting it on a real task.",
                    "Verification",
                )
                st.selectbox("Self-test stack", options=stack_profile["ordered_options"], key="selftest_stack_profile")
                if st.session_state.selftest_stack_profile == "Custom":
                    st.text_input("Custom self-test stack", key="selftest_custom_stack")
                render_route_block("Current test target", f"{selected_selftest_stack}\nModel: {current_model_name() or 'No active model'}")
                if st.button("Run Self-Test", key="run_developer_selftest", use_container_width=True, type="primary", disabled=not ai_ready):
                    prompt = developer_selftest_prompt(selected_selftest_stack)
                    result, used_model = run_generation_with_details(prompt, f"{selected_selftest_stack} self-test")
                    if result:
                        st.session_state.selftest_response = result
                        st.session_state.selftest_last_model = used_model or current_model_name()
                        remember_output("Developer Self-Test", f"{selected_selftest_stack} Self-Test", result, "developer", "codefix")
                        st.success("Self-test completed.")
                if st.button("Clear Self-Test", key="clear_developer_selftest", use_container_width=True):
                    queue_reset("clear_selftest_workspace", "Developer self-test cleared.")
                    st.rerun()
        with right:
            with st.container(border=True):
                render_preview_panel(
                    "Self-Test Result",
                    "This shows the latest self-test output and the exact requested model id used for that run.",
                    "Self-test output",
                    st.session_state.selftest_response,
                    height=300,
                    empty_title="No self-test yet",
                    empty_body="Run the self-test from the left panel first. The result area remains compact until there is an actual benchmark response.",
                    anchor="ST",
                    tier="secondary",
                )
                render_meta_grid(
                    [
                        ("Last self-test model", st.session_state.selftest_last_model or "No self-test run yet"),
                        ("Last generation model", st.session_state.last_generation_model or "No generation yet"),
                        ("Last generation label", st.session_state.last_generation_label or "None"),
                    ]
                )

    with compare_tab:
        left, right = st.columns([1.02, 0.98], gap="large")
        with left:
            with st.container(border=True):
                render_card_header(
                    "Compare Two Models",
                    "Run the same coding prompt against two requested model ids and inspect the outputs side by side.",
                    "Comparison",
                )
                compare_a, compare_b = st.columns(2, gap="small")
                compare_a.selectbox("Model A", options=MODEL_SELECTION_OPTIONS, key="compare_model_a")
                compare_b.selectbox("Model B", options=MODEL_SELECTION_OPTIONS, key="compare_model_b")
                if st.session_state.compare_model_a == "Custom":
                    st.text_input("Custom Model A", key="compare_custom_model_a")
                if st.session_state.compare_model_b == "Custom":
                    st.text_input("Custom Model B", key="compare_custom_model_b")
                st.text_area(
                    "Comparison prompt",
                    key="compare_prompt",
                    height=160,
                    placeholder="Example: Build a FastAPI CRUD endpoint with validation and explain the route structure.",
                )
                action_a, action_b = st.columns(2, gap="small")
                if action_a.button("Run Model Comparison", key="run_model_compare", use_container_width=True, type="primary", disabled=not ai_ready):
                    compare_prompt = st.session_state.compare_prompt.strip()
                    model_a = resolve_model_selection(st.session_state.compare_model_a, st.session_state.compare_custom_model_a)
                    model_b = resolve_model_selection(st.session_state.compare_model_b, st.session_state.compare_custom_model_b)
                    if not compare_prompt:
                        st.warning("Enter a comparison prompt first.")
                    elif not model_a or not model_b:
                        st.warning("Both model slots need a valid model id.")
                    else:
                        result_a, used_a = run_generation_with_details(compare_prompt, "model compare A", requested_model=model_a, track_global=False)
                        result_b, used_b = run_generation_with_details(compare_prompt, "model compare B", requested_model=model_b, track_global=False)
                        if result_a:
                            st.session_state.compare_output_a = result_a
                            st.session_state.compare_used_model_a = used_a or model_a
                        if result_b:
                            st.session_state.compare_output_b = result_b
                            st.session_state.compare_used_model_b = used_b or model_b
                        if result_a or result_b:
                            st.session_state.last_generation_label = "model comparison"
                            st.session_state.last_generation_model = st.session_state.compare_used_model_b or st.session_state.compare_used_model_a
                            st.session_state.last_generation_status = "success"
                            st.session_state.last_generation_time = workspace_timestamp()
                            st.session_state.last_generation_note = "Side-by-side model comparison completed."
                            st.success("Model comparison completed.")
                if action_b.button("Clear Comparison", key="clear_model_compare", use_container_width=True):
                    queue_reset("clear_compare_workspace", "Model comparison cleared.")
                    st.rerun()
        with right:
            model_col_a, model_col_b = st.columns(2, gap="small")
            with model_col_a:
                with st.container(border=True):
                    render_preview_panel(
                        "Model A Output",
                        st.session_state.compare_used_model_a or "No comparison run yet.",
                        "Compare output A",
                        st.session_state.compare_output_a,
                        height=300,
                        empty_title="No Model A output yet",
                        empty_body="Run the model comparison first. This side stays compact until the first output arrives.",
                        anchor="A",
                        tier="secondary",
                    )
            with model_col_b:
                with st.container(border=True):
                    render_preview_panel(
                        "Model B Output",
                        st.session_state.compare_used_model_b or "No comparison run yet.",
                        "Compare output B",
                        st.session_state.compare_output_b,
                        height=300,
                        empty_title="No Model B output yet",
                        empty_body="Run the model comparison first. This side stays compact until the second output arrives.",
                        anchor="B",
                        tier="secondary",
                    )

    with diff_tab:
        fixed_version = extract_section_value(st.session_state.codefix_response, ["Fixed Version"])
        diff_text = build_code_diff(st.session_state.codefix_source, fixed_version)
        left, right = st.columns(2, gap="large")
        with left:
            with st.container(border=True):
                render_card_header(
                    "Before / After Diff",
                    "The diff is built from the original snippet and the Fixed Version section returned by the AI.",
                    "Diff",
                )
                if diff_text:
                    st.code(diff_text, language="diff")
                else:
                    st.caption("Generate a code fix first to build a diff view.")
        with right:
            with st.container(border=True):
                render_card_header(
                    "Parsed Fix Sections",
                    "Useful when you want the root cause and next checks separated from the raw output.",
                    "Sections",
                )
                st.text_area("Root cause", value=extract_section_value(st.session_state.codefix_response, ["Root Cause"]), height=120, disabled=True)
                st.text_area("Why it works", value=extract_section_value(st.session_state.codefix_response, ["Why It Works"]), height=120, disabled=True)
                st.text_area("Next checks", value=extract_section_value(st.session_state.codefix_response, ["Next Checks"]), height=120, disabled=True)

    with notes_tab:
        with st.container(border=True):
            render_card_header(
                "Debug Notes",
                "Recent debugging outputs, last-used model details, and comparison context remain visible here for continuity.",
                "Developer Notes",
            )
            render_meta_grid(
                [
                    ("Last generation model", st.session_state.last_generation_model or "No generation yet"),
                    ("Last generation label", st.session_state.last_generation_label or "None"),
                    ("Last generation time", st.session_state.last_generation_time or "None"),
                ]
            )
            render_history_snippets(limit=8, page_filter="developer")
            row = st.columns(2, gap="small")
            if row[0].button("Open Standalone Code Fixer", key="open_standalone_codefix", use_container_width=True):
                go("codefix")
            if row[1].button("Clear Developer History", key="clear_dev_history_hint", use_container_width=True):
                go("history")
