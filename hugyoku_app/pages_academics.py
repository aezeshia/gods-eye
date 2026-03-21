from __future__ import annotations

from .core import *


def render_source_lab_tab(ai_ready: bool, workspace: dict[str, object], source_bundle: str) -> None:
    src_left, src_right = st.columns(2, gap="large")
    with src_left:
        with st.container(border=True):
            render_card_header(
                "Multi-File Source Lab",
                "Add more source files directly from this page or review the current active source bundle before asking grounded questions.",
                "Sources",
            )
            inline_files = st.file_uploader(
                "Add more files to the active workspace",
                type=["docx", "pdf", "txt", "md"],
                accept_multiple_files=True,
                key="source_lab_inline_upload",
            )
            if st.button("Add Files To Active Workspace", key="source_lab_add_files", use_container_width=True):
                if inline_files:
                    added, failures = add_source_files_to_active_workspace(inline_files)
                    if added:
                        st.success(f"Added {added} file(s) to {active_workspace_name()}.")
                    for failure in failures:
                        st.warning(failure)
                    st.rerun()
                else:
                    st.warning("Upload at least one file first.")
            with st.expander("Review merged source preview", expanded=False):
                if source_bundle.strip():
                    st.text_area("Merged source preview", value=source_bundle, height=280, disabled=True)
                else:
                    render_route_block(
                        "No source bundle yet",
                        "Add files, notes, or screenshots to the active workspace first, then the merged source preview will appear here.",
                    )

    with src_right:
        with st.container(border=True):
            render_preview_panel(
                "Source-Grounded Answers",
                "Generate a grounded analysis with explicit file citations based on the active workspace sources.",
                "Grounded analysis output",
                st.session_state.source_lab_analysis,
                height=310,
                empty_title="No grounded analysis yet",
                empty_body="Run the grounded analysis action after adding workspace material. This preview will stay compact until there is a real result to review.",
                anchor="GA",
                tier="secondary",
            )
            if st.button(
                "Generate Grounded Analysis",
                key="source_lab_analyze",
                use_container_width=True,
                type="primary",
                disabled=not ai_ready,
            ):
                if not source_bundle:
                    st.warning("Add source files or notes to the active workspace first.")
                else:
                    prompt = (
                        "Analyze the provided sources and keep the response grounded in them.\n\n"
                        f"Sources:\n{trim_prompt_source(source_bundle)}\n\n"
                        "Return these plain-text sections in this exact order:\n"
                        "Summary:\n"
                        "Important Details:\n"
                        "Source Citations:\n\n"
                        "In Source Citations, cite files using the form [Source: filename]."
                    )
                    result = run_generation(prompt, "grounded analysis")
                    if result:
                        st.session_state.source_lab_analysis = result
                        remember_output("Grounded Analysis", f"{workspace['name']} Grounded Analysis", result, "academics", "grounded_answer")
                        st.success("Grounded analysis ready.")
            if st.session_state.source_lab_analysis.strip():
                render_download_button(
                    f"{workspace['name']} Grounded Analysis",
                    st.session_state.source_lab_analysis,
                    sanitize_filename(f"{workspace['name']}_grounded_analysis".lower().replace(" ", "_")),
                    "grounded_answer",
                    "clear_source_lab_workspace",
                )

    qa_left, qa_right = st.columns(2, gap="large")
    with qa_left:
        with st.container(border=True):
            render_card_header(
                "Document Q&A Mode",
                "Ask questions directly against the active workspace and require file-based citations in the answer.",
                "Q&A",
            )
            st.text_area("Question", key="source_lab_question_input", height=140)
            if st.button(
                "Answer With Citations",
                key="source_lab_answer_question",
                use_container_width=True,
                type="primary",
                disabled=not ai_ready,
            ):
                question = st.session_state.source_lab_question_input.strip()
                if not question:
                    st.warning("Enter a question first.")
                elif not source_bundle:
                    st.warning("Add source material to the active workspace first.")
                else:
                    prompt = (
                        "Answer the user's question using only the provided sources.\n"
                        "If the answer is not supported by the sources, say so clearly.\n\n"
                        f"Question: {question}\n\n"
                        f"Sources:\n{trim_prompt_source(source_bundle)}\n\n"
                        "Return these plain-text sections in this exact order:\n"
                        "Answer:\n"
                        "Cited Sources:\n"
                        "Confidence:\n\n"
                        "Use the form [Source: filename] in Cited Sources."
                    )
                    result = run_generation(prompt, "document Q&A answer")
                    if result:
                        st.session_state.source_lab_answer = result
                        remember_output("Document Q&A", f"{workspace['name']} Q&A", result, "academics", "documentqa")
                        st.success("Document Q&A answer ready.")
            if st.session_state.source_lab_answer.strip():
                st.text_area("Q&A answer", value=st.session_state.source_lab_answer, height=250, disabled=True)
            else:
                render_route_block(
                    "No answer yet",
                    "Enter a source-grounded question first. The answer preview will only expand once there is a result.",
                )
            if st.session_state.source_lab_answer.strip():
                render_download_button(
                    f"{workspace['name']} Document Answer",
                    st.session_state.source_lab_answer,
                    sanitize_filename(f"{workspace['name']}_document_answer".lower().replace(" ", "_")),
                    "documentqa",
                    "clear_source_lab_workspace",
                )

    with qa_right:
        with st.container(border=True):
            render_card_header(
                "Screenshot Input",
                "Screenshots stay attached to the active workspace. Use workspace notes to supply manual OCR text or important context.",
                "Image Input",
            )
            if workspace.get("images"):
                st.image([item.get("bytes") for item in workspace.get("images", [])[:4]], width=180)
                st.caption("Attached screenshots are stored with the active workspace.")
            else:
                st.caption("No screenshots attached yet. Add them from Workspaces.")
            if st.button("Open Workspaces", key="source_lab_open_workspaces", use_container_width=True):
                go("workspaces")


def render_study_tools_tab(ai_ready: bool, workspace: dict[str, object], source_bundle: str) -> None:
    reviewer_tab, flashcard_tab, test_tab, checker_tab = st.tabs(
        ["Reviewer Generator", "Flashcard Generator", "Practice Test", "Answer Checker"]
    )

    with reviewer_tab:
        left, right = st.columns(2, gap="large")
        with left:
            with st.container(border=True):
                render_card_header(
                    "Reviewer Generator",
                    "Turn the active workspace or a custom request into structured review notes.",
                    "Study Tool",
                )
                st.text_area("Reviewer focus or instructions", key="reviewer_request_input", height=170)
                if st.button("Generate Reviewer", key="generate_reviewer", use_container_width=True, type="primary", disabled=not ai_ready):
                    prompt = (
                        "Create reviewer notes for the provided study materials.\n\n"
                        f"Reviewer request: {st.session_state.reviewer_request_input.strip() or 'Use the active workspace as-is.'}\n\n"
                        f"Sources:\n{trim_prompt_source(source_bundle or workspace.get('notes', ''))}\n\n"
                        "Return these plain-text sections in this exact order:\n"
                        "Summary:\n"
                        "Key Terms:\n"
                        "Important Details:\n"
                        "Quick Recall Questions:\n"
                    )
                    result = run_generation(prompt, "reviewer notes")
                    if result:
                        st.session_state.reviewer_response = result
                        remember_output("Reviewer Notes", f"{workspace['name']} Reviewer", result, "academics", "reviewer")
                        st.success("Reviewer notes ready.")
        with right:
            with st.container(border=True):
                render_preview_panel(
                    "Reviewer Preview",
                    "Review the notes before exporting.",
                    "Reviewer output",
                    st.session_state.reviewer_response,
                    height=340,
                    empty_title="No reviewer notes yet",
                    empty_body="Generate reviewer notes from the left panel. The preview appears only once there is content worth reviewing.",
                    anchor="RV",
                    tier="secondary",
                )
                if st.session_state.reviewer_response.strip():
                    render_download_button(
                        f"{workspace['name']} Reviewer Notes",
                        st.session_state.reviewer_response,
                        sanitize_filename(f"{workspace['name']}_reviewer_notes".lower().replace(" ", "_")),
                        "reviewer",
                        "clear_reviewer_workspace",
                    )

    with flashcard_tab:
        left, right = st.columns(2, gap="large")
        with left:
            with st.container(border=True):
                render_card_header(
                    "Flashcard Generator",
                    "Generate concise question-and-answer cards from the active workspace or a custom request.",
                    "Study Tool",
                )
                st.text_area("Flashcard focus or instructions", key="flashcard_request_input", height=170)
                if st.button("Generate Flashcards", key="generate_flashcards", use_container_width=True, type="primary", disabled=not ai_ready):
                    prompt = (
                        "Create flashcards from the provided study materials.\n\n"
                        f"Flashcard request: {st.session_state.flashcard_request_input.strip() or 'Use the active workspace as-is.'}\n\n"
                        f"Sources:\n{trim_prompt_source(source_bundle or workspace.get('notes', ''))}\n\n"
                        "Return a numbered list of flashcards in this pattern:\n"
                        "Q:\n"
                        "A:\n\n"
                        "Keep each answer short and review-friendly."
                    )
                    result = run_generation(prompt, "flashcards")
                    if result:
                        st.session_state.flashcard_response = result
                        remember_output("Flashcards", f"{workspace['name']} Flashcards", result, "academics", "flashcards")
                        st.success("Flashcards ready.")
        with right:
            with st.container(border=True):
                render_preview_panel(
                    "Flashcard Preview",
                    "Review the generated cards before export.",
                    "Flashcard output",
                    st.session_state.flashcard_response,
                    height=340,
                    empty_title="No flashcards yet",
                    empty_body="Generate flashcards from the left panel. The preview will appear here once the deck is ready.",
                    anchor="FC",
                    tier="secondary",
                )
                if st.session_state.flashcard_response.strip():
                    render_download_button(
                        f"{workspace['name']} Flashcards",
                        st.session_state.flashcard_response,
                        sanitize_filename(f"{workspace['name']}_flashcards".lower().replace(" ", "_")),
                        "flashcards",
                        "clear_flashcard_workspace",
                    )

    with test_tab:
        left, right = st.columns(2, gap="large")
        with left:
            with st.container(border=True):
                render_card_header(
                    "Practice Test Generator",
                    "Generate multiple-choice, true/false, and short-answer practice items from the active workspace.",
                    "Study Tool",
                )
                st.text_area("Practice test focus or instructions", key="practice_test_request_input", height=170)
                if st.button("Generate Practice Test", key="generate_practice_test", use_container_width=True, type="primary", disabled=not ai_ready):
                    prompt = (
                        "Create a study practice test using the provided materials.\n\n"
                        f"Practice test request: {st.session_state.practice_test_request_input.strip() or 'Use the active workspace as-is.'}\n\n"
                        f"Sources:\n{trim_prompt_source(source_bundle or workspace.get('notes', ''))}\n\n"
                        "Return these plain-text sections in this exact order:\n"
                        "Multiple Choice:\n"
                        "True or False:\n"
                        "Short Answer:\n"
                        "Answer Key:\n"
                    )
                    result = run_generation(prompt, "practice test")
                    if result:
                        st.session_state.practice_test_response = result
                        remember_output("Practice Test", f"{workspace['name']} Practice Test", result, "academics", "practice_test")
                        st.success("Practice test ready.")
        with right:
            with st.container(border=True):
                render_preview_panel(
                    "Practice Test Preview",
                    "Review the generated practice test before export.",
                    "Practice test output",
                    st.session_state.practice_test_response,
                    height=340,
                    empty_title="No practice test yet",
                    empty_body="Generate the practice test first. The output preview and export controls will appear here after that.",
                    anchor="PT",
                    tier="secondary",
                )
                if st.session_state.practice_test_response.strip():
                    render_download_button(
                        f"{workspace['name']} Practice Test",
                        st.session_state.practice_test_response,
                        sanitize_filename(f"{workspace['name']}_practice_test".lower().replace(" ", "_")),
                        "practice_test",
                        "clear_practice_test_workspace",
                    )

    with checker_tab:
        left, right = st.columns(2, gap="large")
        with left:
            with st.container(border=True):
                render_card_header(
                    "Answer Checker",
                    "Compare a student answer against the question, optional reference notes, and the active workspace sources.",
                    "Study Tool",
                )
                st.text_area("Question", key="answer_checker_question_input", height=110)
                st.text_area("Reference notes (optional)", key="answer_checker_reference_input", height=110)
                st.text_area("Your answer", key="answer_checker_user_answer_input", height=140)
                if st.button("Check Answer", key="check_answer_button", use_container_width=True, type="primary", disabled=not ai_ready):
                    question = st.session_state.answer_checker_question_input.strip()
                    user_answer = st.session_state.answer_checker_user_answer_input.strip()
                    if not question or not user_answer:
                        st.warning("Enter both the question and your answer first.")
                    else:
                        prompt = (
                            "Evaluate the student's answer using the provided references and source material.\n\n"
                            f"Question:\n{question}\n\n"
                            f"Reference notes:\n{st.session_state.answer_checker_reference_input.strip() or 'No separate reference notes provided.'}\n\n"
                            f"Active workspace sources:\n{trim_prompt_source(source_bundle or workspace.get('notes', ''))}\n\n"
                            f"Student answer:\n{user_answer}\n\n"
                            "Return these plain-text sections in this exact order:\n"
                            "Score:\n"
                            "What Works:\n"
                            "Missing or Weak Parts:\n"
                            "Improved Answer:\n"
                        )
                        result = run_generation(prompt, "answer check")
                        if result:
                            st.session_state.answer_checker_response = result
                            remember_output("Answer Check", f"{workspace['name']} Answer Check", result, "academics", "answer_checker")
                            st.success("Answer review ready.")
        with right:
            with st.container(border=True):
                render_preview_panel(
                    "Answer Checker Preview",
                    "Review the score, gaps, and improved answer.",
                    "Answer checker output",
                    st.session_state.answer_checker_response,
                    height=390,
                    empty_title="No answer review yet",
                    empty_body="Submit a question and a student answer first. The review panel stays lightweight until there is a scored response.",
                    anchor="AN",
                    tier="secondary",
                )
                if st.session_state.answer_checker_response.strip():
                    render_download_button(
                        f"{workspace['name']} Answer Check",
                        st.session_state.answer_checker_response,
                        sanitize_filename(f"{workspace['name']}_answer_check".lower().replace(" ", "_")),
                        "answer_checker",
                        "clear_answer_checker_workspace",
                    )


def render_writing_studio_tab(ai_ready: bool, workspace: dict[str, object], source_bundle: str) -> None:
    rubric_tab, batch_tab, legacy_tab = st.tabs(["Rubric Mode", "Batch Output Generator", "Legacy Builders"])

    with rubric_tab:
        left, right = st.columns(2, gap="large")
        with left:
            with st.container(border=True):
                render_card_header(
                    "Rubric Mode",
                    "Generate writing aligned to selected rubric criteria while still using the active workspace as reference.",
                    "Writing Studio",
                )
                st.text_input("Writing title", key="rubric_title_input")
                st.text_area("Writing request", key="rubric_prompt_input", height=170)
                st.multiselect(
                    "Rubric focus",
                    options=["Clarity", "Structure", "Depth", "Grammar", "Critical Thinking", "Evidence"],
                    key="rubric_focus_input",
                )
                if st.button("Generate Rubric-Aligned Draft", key="generate_rubric_draft", use_container_width=True, type="primary", disabled=not ai_ready):
                    title = st.session_state.rubric_title_input.strip()
                    request = st.session_state.rubric_prompt_input.strip()
                    focus = ", ".join(st.session_state.rubric_focus_input) or "Clarity, Structure, Depth"
                    if not title or not request:
                        st.warning("Enter both the title and writing request first.")
                    else:
                        prompt = (
                            "Write a structured academic draft aligned to the selected rubric.\n\n"
                            f"Title: {title}\n"
                            f"Rubric focus: {focus}\n"
                            f"Request: {request}\n\n"
                            f"Source material:\n{trim_prompt_source(source_bundle or workspace.get('notes', ''))}\n\n"
                            "Return these plain-text sections in this exact order:\n"
                            "Title Suggestion:\n"
                            "Draft:\n"
                            "Rubric Alignment Notes:\n"
                        )
                        result = run_generation(prompt, "rubric-aligned draft")
                        if result:
                            st.session_state.rubric_response = result
                            remember_output("Rubric Draft", f"{title} Rubric Draft", result, "academics", "rubric")
                            st.success("Rubric-aligned draft ready.")
        with right:
            with st.container(border=True):
                render_preview_panel(
                    "Rubric Draft Preview",
                    "Review the aligned draft and rubric notes before export.",
                    "Rubric mode output",
                    st.session_state.rubric_response,
                    height=390,
                    empty_title="No rubric draft yet",
                    empty_body="Generate a rubric-aligned draft from the left panel. The review and export controls will appear here once the draft is ready.",
                    anchor="RB",
                    tier="secondary",
                )
                if st.session_state.rubric_response.strip():
                    render_download_button(
                        st.session_state.rubric_title_input.strip() or f"{workspace['name']} Rubric Draft",
                        st.session_state.rubric_response,
                        sanitize_filename((st.session_state.rubric_title_input.strip() or f"{workspace['name']}_rubric_draft").lower().replace(" ", "_")),
                        "rubric",
                        "clear_rubric_workspace",
                    )

    with batch_tab:
        left, right = st.columns(2, gap="large")
        with left:
            with st.container(border=True):
                render_card_header(
                    "Batch Output Generator",
                    "Generate multiple deliverables from one topic or one workspace source bundle in a single run.",
                    "Writing Studio",
                )
                st.text_input("Batch topic", key="batch_topic_input")
                st.text_area("Batch instructions", key="batch_request_input", height=170)
                if st.button("Generate Batch Outputs", key="generate_batch_outputs", use_container_width=True, type="primary", disabled=not ai_ready):
                    topic = st.session_state.batch_topic_input.strip() or str(workspace.get("name", "Workspace"))
                    request = st.session_state.batch_request_input.strip() or "Generate a study summary, reviewer, flashcards, and essay outline."
                    prompt = (
                        "Create multiple study outputs from the same source material.\n\n"
                        f"Topic: {topic}\n"
                        f"Request: {request}\n\n"
                        f"Source material:\n{trim_prompt_source(source_bundle or workspace.get('notes', ''))}\n\n"
                        "Return these plain-text sections in this exact order:\n"
                        "Summary:\n"
                        "Reviewer Notes:\n"
                        "Flashcards:\n"
                        "Essay Outline:\n"
                    )
                    result = run_generation(prompt, "batch output package")
                    if result:
                        st.session_state.batch_response = result
                        remember_output("Batch Output", f"{topic} Batch Output", result, "academics", "batch")
                        st.success("Batch output ready.")
        with right:
            with st.container(border=True):
                render_preview_panel(
                    "Batch Output Preview",
                    "Review the combined output package before export.",
                    "Batch output",
                    st.session_state.batch_response,
                    height=390,
                    empty_title="No batch output yet",
                    empty_body="Generate the batch package from the left panel. The preview stays compact until the combined output is ready.",
                    anchor="BT",
                    tier="secondary",
                )
                if st.session_state.batch_response.strip():
                    render_download_button(
                        st.session_state.batch_topic_input.strip() or f"{workspace['name']} Batch Output",
                        st.session_state.batch_response,
                        sanitize_filename((st.session_state.batch_topic_input.strip() or f"{workspace['name']}_batch_output").lower().replace(" ", "_")),
                        "batch",
                        "clear_batch_workspace",
                    )

    with legacy_tab:
        with st.container(border=True):
            render_card_header(
                "Legacy Builders",
                "The older dedicated pages still exist for users who prefer the original single-tool workflows.",
                "Compatibility",
            )
            row_a = st.columns(3, gap="small")
            if row_a[0].button("Open Quiz Solver", key="legacy_quiz_open", use_container_width=True):
                go("quiz")
            if row_a[1].button("Open Assignment Solver", key="legacy_assignment_open", use_container_width=True):
                go("assignment")
            if row_a[2].button("Open Essay Builder", key="legacy_essay_open", use_container_width=True):
                go("essay")
            row_b = st.columns(2, gap="small")
            if row_b[0].button("Open Activity Builder", key="legacy_activity_open", use_container_width=True):
                go("activity")
            if row_b[1].button("Open Document Builder", key="legacy_document_open", use_container_width=True):
                go("document")


def render_export_center_tab() -> None:
    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            render_card_header(
                "Professional Export Templates",
                "Choose the document style used by all Word exports generated in this session.",
                "Export Center",
            )
            st.radio(
                "Export template",
                options=list(EXPORT_TEMPLATES.keys()),
                key="export_template",
                horizontal=False,
            )
            template = EXPORT_TEMPLATES[st.session_state.export_template]
            render_meta_grid(
                [
                    ("Font", str(template["font"])),
                    ("Body size", str(template["body_size"])),
                    ("Title size", str(template["title_size"])),
                    ("Line spacing", str(template["line_spacing"])),
                ]
            )
    with right:
        with st.container(border=True):
            render_card_header(
                "Export Routes",
                "Local saves and browser downloads both use the same current export template.",
                "Routing",
            )
            paths = folder_path_lines()
            with st.expander("Open route list", expanded=False):
                render_route_block("Reviewer", paths["reviewer"])
                render_route_block("Flashcards", paths["flashcards"])
                render_route_block("Practice Test", paths["practice_test"])
                render_route_block("Rubric Draft", paths["rubric"])
                render_route_block("Batch Output", paths["batch"])


def render_academics_hub(ai_ready: bool) -> None:
    workspace = active_workspace()
    source_bundle = workspace_source_bundle(workspace)
    with st.container(border=True):
        render_card_header(
            PAGE_DETAILS["academics"]["title"],
            "Use the active workspace as the source of truth, then branch into one focused study flow at a time.",
            "Academics Suite",
            anchor="AC",
            tier="primary",
        )
        render_kpi_row(
            [
                ("Workspace", str(workspace.get("name", "General Workspace"))),
                ("Source files", str(len(workspace.get("files", [])))),
                ("Images", str(len(workspace.get("images", [])))),
                ("Template", str(st.session_state.get("export_template", "Academic Classic"))),
            ]
        )
        with st.expander("Workspace context", expanded=False):
            render_route_block(
                "Current source bundle",
                f"{len(source_bundle)} characters ready for prompting" if source_bundle else "No files or notes have been attached to this workspace yet.",
            )

    source_tab, study_tab, writing_tab, export_tab = st.tabs(
        ["Source Lab", "Study Tools", "Writing Studio", "Export Center"]
    )

    with source_tab:
        render_source_lab_tab(ai_ready, workspace, source_bundle)
    with study_tab:
        render_study_tools_tab(ai_ready, workspace, source_bundle)
    with writing_tab:
        render_writing_studio_tab(ai_ready, workspace, source_bundle)
    with export_tab:
        render_export_center_tab()
