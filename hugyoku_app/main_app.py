from __future__ import annotations

from .core import *
from .pages_general import (
    render_admin_page,
    render_dashboard,
    render_header,
    render_hugyoku_page,
    render_login_gate,
    render_sidebar,
    render_workspaces_page,
)
from .pages_academics import render_academics_hub
from .pages_developer import render_developer_hub
from .pages_system import render_history_page, render_settings_page


def main() -> None:
    # Wide layout plus auto sidebar collapse gives better behavior on narrow screens.
    st.set_page_config(page_title="Hugyoku | Premium Academics Suite", layout="wide", initial_sidebar_state="auto")
    st.markdown(THEME_CSS, unsafe_allow_html=True)
    initialize_auth_storage()
    ensure_state()
    apply_pending_state_actions()
    render_flash_message()

    if not st.session_state.is_authenticated:
        render_login_gate()
        return

    ensure_workspace_bootstrap()

    if not can_access_page(st.session_state.active_page):
        fallback_page = "dashboard"
        for candidate in ["hugyoku", "dashboard", "workspaces", "academics", "developer", "history", "settings"]:
            if can_access_page(candidate):
                fallback_page = candidate
                break
        st.session_state.active_page = fallback_page
        st.session_state.flash_message = "That page is not allowed for your account."
        st.session_state.flash_level = "warning"
        st.rerun()

    _client, model, error = load_client()
    ai_ready = error is None
    model_label = model or "No model configured"
    ai_message = "AI ready for academics" if ai_ready else error

    render_sidebar(ai_ready, model_label, ai_message)
    render_header(ai_ready, model_label, ai_message)
    render_flash_message()

    page = st.session_state.active_page
    if page == "hugyoku":
        render_hugyoku_page(ai_ready)
    elif page == "dashboard":
        render_dashboard()
    elif page == "workspaces":
        render_workspaces_page(ai_ready)
    elif page == "academics":
        render_academics_hub(ai_ready)
    elif page == "developer":
        render_developer_hub(ai_ready)
    elif page == "history":
        render_history_page()
    elif page == "settings":
        render_settings_page(ai_ready)
    elif page == "admin":
        render_admin_page()
    elif page == "quiz":
        render_quiz_page(ai_ready)
    elif page == "assignment":
        render_assignment_page(ai_ready)
    elif page == "essay":
        render_essay_page(ai_ready)
    elif page == "activity":
        render_activity_page(ai_ready)
    elif page == "document":
        render_document_page(ai_ready)
    elif page == "codefix":
        render_codefix_page(ai_ready)
    else:
        go("dashboard")
