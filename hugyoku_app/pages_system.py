from __future__ import annotations

from .core import *


def render_history_page() -> None:
    entries = list(st.session_state.get("history_entries", []))
    with st.container(border=True):
        render_card_header(
            PAGE_DETAILS["history"]["title"],
            PAGE_DETAILS["history"]["subtitle"],
            "History",
            anchor="HS",
            tier="primary",
        )
        render_tag_row(["Uploads", "Generations", "Exports", "Workspace Events"])

    filter_left, filter_right = st.columns(2, gap="large")
    with filter_left:
        kind_filter = st.selectbox(
            "Filter by kind",
            options=["All"] + sorted({str(entry.get("kind", "")) for entry in entries if entry.get("kind")}),
            key="history_kind_filter",
        )
    with filter_right:
        page_filter = st.selectbox(
            "Filter by page",
            options=["All"] + sorted({str(entry.get("page", "")) for entry in entries if entry.get("page")}),
            key="history_page_filter",
        )

    filtered_entries = entries
    if kind_filter != "All":
        filtered_entries = [entry for entry in filtered_entries if entry.get("kind") == kind_filter]
    if page_filter != "All":
        filtered_entries = [entry for entry in filtered_entries if entry.get("page") == page_filter]

    top_left, top_right = st.columns([1.05, 0.95], gap="large")
    with top_left:
        with st.container(border=True):
            render_card_header(
                "Recent Session Timeline",
                "The most recent events appear first so it is easy to reconstruct what happened in the session.",
                "Timeline",
            )
            if filtered_entries:
                for entry in filtered_entries[:20]:
                    render_route_block(
                        f"{entry.get('timestamp', '')} • {entry.get('title', '')}",
                        f"{entry.get('details', '')}\nPage: {entry.get('page', '-')}\nWorkspace: {entry.get('workspace', '-')}",
                    )
            else:
                st.caption("No history entries match the current filters.")
    with top_right:
        with st.container(border=True):
            render_card_header(
                "Workspace Output Archive",
                "Saved outputs are grouped under the current workspace and remain reusable during this session.",
                "Archive",
            )
            render_workspace_outputs(limit=10)
            if st.button("Clear History", key="clear_history_button", use_container_width=True):
                queue_reset("clear_history_entries", "History cleared.", "info")
                st.rerun()


def render_settings_page(ai_ready: bool) -> None:
    secret_model = read_secret("HF_MODEL") or "No secret model configured"
    sync_model_selector_state()

    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            render_card_header(
                "Model Switcher",
                "Override the model coming from secrets for this Streamlit session.",
                "Settings",
                anchor="MD",
                tier="primary",
            )
            st.selectbox(
                "Model source",
                options=[item for item in MODEL_SELECTION_OPTIONS if item != "Active Session Model"],
                key="model_choice_input",
            )
            if st.session_state.model_choice_input == "Custom":
                st.text_input("Custom model id", key="model_custom_input")
            render_meta_grid(
                [
                    ("Secret default", secret_model),
                    ("Current override", st.session_state.model_override or "None"),
                    ("AI status", "Ready" if ai_ready else "Not ready"),
                ]
            )
            save_model_col, reset_model_col = st.columns(2, gap="small")
            if save_model_col.button("Apply Model Choice", key="apply_model_choice", use_container_width=True, type="primary"):
                choice = st.session_state.model_choice_input
                if choice == "HF Secret Default":
                    st.session_state.model_override = ""
                elif choice == "Custom":
                    st.session_state.model_override = st.session_state.model_custom_input.strip()
                else:
                    st.session_state.model_override = choice
                append_history_entry("settings", "Updated model selection", st.session_state.model_override or "Using HF secret default model.", "settings", active_workspace_name(), "model")
                st.session_state.flash_message = "Model selection updated."
                st.session_state.flash_level = "success"
                st.rerun()
            if reset_model_col.button("Reset To Secret Model", key="reset_model_choice", use_container_width=True):
                queue_reset("clear_model_selection", "Model override cleared.")
                st.rerun()

    with right:
        with st.container(border=True):
            render_card_header(
                "Session Controls",
                "Adjust session-level export defaults and history retention.",
                "Settings",
                anchor="SC",
                tier="secondary",
            )
            st.radio("Default export template", options=list(EXPORT_TEMPLATES.keys()), key="export_template", horizontal=False)
            st.number_input("History entry limit", min_value=20, max_value=300, step=10, key="settings_history_limit")
            render_route_block("Current package root", current_package_root_name())
            if st.button("Open History", key="settings_open_history", use_container_width=True):
                go("history")

    verify_left, verify_right = st.columns(2, gap="large")
    with verify_left:
        with st.container(border=True):
            render_card_header(
                "Real Model Verification Panel",
                "This runs a live probe against the currently active requested model id. It verifies the app request path and the provider response, not the hidden physical backend identity behind the provider.",
                "Verification",
            )
            render_meta_grid(
                [
                    ("Requested active model", current_model_name() or "No active model"),
                    ("Last verified model", st.session_state.verification_last_model or "No probe yet"),
                    ("Last verify status", st.session_state.verification_last_status or "Not run"),
                ]
            )
            if st.button("Run Live Verification Probe", key="run_live_model_probe", use_container_width=True, type="primary", disabled=not ai_ready):
                target_model = current_model_name()
                if not target_model:
                    st.warning("No active model is configured.")
                else:
                    ok, _probe = run_model_verification_probe(target_model)
                    if ok:
                        st.success("Live model probe completed.")
                    else:
                        st.error("Live model probe failed.")
            render_route_block(
                "Verification note",
                st.session_state.verification_last_note or "No verification probe has been run yet.",
            )

    with verify_right:
        with st.container(border=True):
            render_card_header(
                "Last Generation Used Model",
                "This records the exact requested model id used by the last generation call handled by the app.",
                "Generation Trace",
            )
            render_meta_grid(
                [
                    ("Model", st.session_state.last_generation_model or "No generation yet"),
                    ("Label", st.session_state.last_generation_label or "None"),
                    ("Status", st.session_state.last_generation_status or "None"),
                    ("Time", st.session_state.last_generation_time or "None"),
                ]
            )
            render_route_block(
                "Last generation note",
                st.session_state.last_generation_note or "No generation has been recorded yet.",
            )
