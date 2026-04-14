from __future__ import annotations

from .core import *


def render_login_gate() -> None:
    has_users = auth_user_count() > 0
    st.markdown('<div class="hugyoku-login-page"></div>', unsafe_allow_html=True)
    login_page_css = """
    <style>
    body:has(.hugyoku-login-page) .main .block-container,
    body:has(.hugyoku-login-page) [data-testid="block-container"] {
      max-width: 980px !important;
      padding-top: 0.55rem !important;
      padding-bottom: 1rem !important;
    }

    body:has(.hugyoku-login-page) [data-testid="stHorizontalBlock"] {
      gap: 0.85rem !important;
      align-items: stretch !important;
    }

    body:has(.hugyoku-login-page) [data-testid="stVerticalBlockBorderWrapper"] > div {
      padding: 0.92rem 0.95rem !important;
    }

    body:has(.hugyoku-login-page) .app-hero-title {
      font-size: clamp(1.9rem, 4.6vw, 2.7rem) !important;
      line-height: 1.04 !important;
      max-width: 14ch !important;
      margin-bottom: 0.32rem !important;
    }

    body:has(.hugyoku-login-page) .app-card-subtitle {
      max-width: 66ch !important;
      font-size: 0.93rem !important;
      line-height: 1.55 !important;
    }

    body:has(.hugyoku-login-page) .app-card-title {
      font-size: 1.2rem !important;
    }

    body:has(.hugyoku-login-page) .app-chip-row {
      gap: 0.42rem !important;
      margin-top: 0.78rem !important;
    }

    body:has(.hugyoku-login-page) .app-chip {
      padding: 0.32rem 0.62rem !important;
      font-size: 0.73rem !important;
    }

    body:has(.hugyoku-login-page) .app-meta-grid {
      margin-top: 0.75rem !important;
      gap: 0.5rem !important;
    }

    body:has(.hugyoku-login-page) .app-meta-item,
    body:has(.hugyoku-login-page) .app-route-block {
      padding: 0.72rem 0.78rem !important;
    }

    body:has(.hugyoku-login-page) [data-testid="stForm"] {
      margin-top: 0.2rem;
    }

    body:has(.hugyoku-login-page) [data-testid="stTextInput"] > label,
    body:has(.hugyoku-login-page) [data-testid="stPasswordInput"] > label {
      font-size: 0.85rem !important;
    }

    body:has(.hugyoku-login-page) [data-testid="stTextInput"] input,
    body:has(.hugyoku-login-page) [data-testid="stPasswordInput"] input {
      min-height: 2.85rem !important;
      font-size: 1rem !important;
    }

    body:has(.hugyoku-login-page) .stButton > button,
    body:has(.hugyoku-login-page) .stForm [data-testid="stFormSubmitButton"] > button {
      min-height: 2.9rem !important;
      font-size: 0.98rem !important;
    }

    @media (max-width: 700px) {
      body:has(.hugyoku-login-page) .main .block-container,
      body:has(.hugyoku-login-page) [data-testid="block-container"] {
        padding-left: 0.55rem !important;
        padding-right: 0.55rem !important;
        padding-top: 0.38rem !important;
        padding-bottom: 0.72rem !important;
      }

      body:has(.hugyoku-login-page) [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 0.7rem !important;
      }

      body:has(.hugyoku-login-page) [data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
      }

      body:has(.hugyoku-login-page) [data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 0.8rem 0.8rem !important;
        border-radius: 16px !important;
      }

      body:has(.hugyoku-login-page) .app-hero-title {
        font-size: 1.62rem !important;
        max-width: none !important;
      }

      body:has(.hugyoku-login-page) .app-card-subtitle,
      body:has(.hugyoku-login-page) .app-route-body,
      body:has(.hugyoku-login-page) .app-soft-note {
        font-size: 0.84rem !important;
        line-height: 1.45 !important;
      }

      body:has(.hugyoku-login-page) .app-chip:nth-child(n+4) {
        display: none !important;
      }

      body:has(.hugyoku-login-page) .app-meta-grid {
        grid-template-columns: 1fr 1fr !important;
      }

      body:has(.hugyoku-login-page) .app-meta-label {
        font-size: 0.62rem !important;
      }

      body:has(.hugyoku-login-page) .app-meta-value {
        font-size: 0.9rem !important;
      }
    }
    </style>
    """
    st.markdown(login_page_css, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            """
            <div class="app-kicker">Hugyoku Access Control</div>
            <div class="app-hero-title">Login Before Workspace Access</div>
            <div class="app-card-subtitle">
              Sign in first before opening Hugyoku. Keep the page simple on mobile:
              one main action, compact status, and secondary details below.
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_tag_row(["Login First", "Role-Based Access", "Local Storage"])
        render_meta_grid(
            [
                ("Users", str(auth_user_count())),
                ("Database", AUTH_DB_PATH.name),
                ("Mode", "Bootstrap required" if not has_users else "Login required"),
            ]
        )

    if not has_users:
        with st.container(border=True):
            render_card_header(
                "Create The First Admin",
                "Set up the first admin account on this machine. After setup, every user signs in before entering Hugyoku.",
                "Bootstrap",
                compact=True,
            )
            with st.form("bootstrap_form", clear_on_submit=False):
                st.text_input("Admin username", key="bootstrap_username_input")
                st.text_input("Display name", key="bootstrap_display_name_input")
                st.text_input("Password", key="bootstrap_password_input", type="password")
                st.text_input("Confirm password", key="bootstrap_confirm_password_input", type="password")
                bootstrap_submitted = st.form_submit_button(
                    "Create First Admin",
                    use_container_width=True,
                    type="primary",
                )
            if bootstrap_submitted:
                username = st.session_state.bootstrap_username_input.strip()
                display_name = st.session_state.bootstrap_display_name_input.strip()
                password = st.session_state.bootstrap_password_input
                confirm = st.session_state.bootstrap_confirm_password_input
                if not username or not password:
                    st.warning("Username and password are required.")
                elif password != confirm:
                    st.warning("Passwords do not match.")
                else:
                    ok, message = create_auth_user(username, display_name or username, password, role="super_admin")
                    if ok:
                        queue_reset("clear_bootstrap_form", "First admin account created. You can sign in now.")
                        st.rerun()
                    else:
                        st.error(message)

        with st.expander("Setup notes", expanded=False):
            render_route_block("Create once", "Bootstrap the first admin on the machine where Hugyoku runs.")
            render_route_block("Login after setup", "After bootstrap, every user must sign in before any workspace appears.")
            render_route_block("Admin powers", "Admins can create users, change roles, and limit page access.")
        return

    with st.container(border=True):
        render_card_header(
            "Sign In",
            "Use your Hugyoku account to open the workspace. The page stays focused on the login form first.",
            "Authentication",
            compact=True,
        )
        with st.form("login_form", clear_on_submit=False):
            st.text_input("Username", key="login_username_input")
            st.text_input("Password", key="login_password_input", type="password")
            login_submitted = st.form_submit_button("Login To Hugyoku", use_container_width=True, type="primary")
        if login_submitted:
            success, message = authenticate_user(st.session_state.login_username_input, st.session_state.login_password_input)
            if success:
                queue_reset(
                    "clear_login_form",
                    f"Welcome back, {st.session_state.auth_display_name or st.session_state.auth_username}.",
                )
                st.rerun()
            st.error(message)

    with st.expander("Access details", expanded=False):
        render_route_block("Access rules", "member -> core workspace tools\nadmin -> workspace tools + admin panel\ninactive user -> blocked")
        recent_logs = auth_log_rows(limit=4)
        if recent_logs:
            for log_row in recent_logs[:4]:
                render_route_block(
                    f"{log_row['created_at']} • {log_row['event_type']}",
                    f"{log_row['username']}\n{log_row['details']}",
                )
        else:
            st.caption("No recent auth activity yet.")


def render_admin_page() -> None:
    users = list_auth_users()
    role_filter = st.session_state.admin_filter_role
    filtered_users = users if role_filter == "All" else [user for user in users if user["role"] == role_filter]

    with st.container(border=True):
        render_card_header(
            PAGE_DETAILS["admin"]["title"],
            PAGE_DETAILS["admin"]["subtitle"],
            "Admin Control",
        )
        render_tag_row(["User Manager", "Role Permissions", "Auth Logs", "Account Status"])

    overview_tab, users_tab, logs_tab = st.tabs(["Overview", "Users", "Activity Logs"])

    with overview_tab:
        total_users = len(users)
        active_users = sum(1 for user in users if user["is_active"])
        admin_users = sum(1 for user in users if user["role"] in {"admin", "super_admin"})
        member_users = sum(1 for user in users if user["role"] == "member")
        viewer_users = sum(1 for user in users if user["role"] == "viewer")
        with st.container(border=True):
            render_card_header(
                "Access Overview",
                "Quick visibility into who can use the app and which accounts currently have elevated privileges.",
                "Overview",
            )
            render_meta_grid(
                [
                    ("Total users", str(total_users)),
                    ("Active users", str(active_users)),
                    ("Admins", str(admin_users)),
                    ("Current operator", st.session_state.auth_username or "-"),
                ]
            )
            render_meta_grid(
                [
                    ("Members", str(member_users)),
                    ("Viewers", str(viewer_users)),
                    ("Inactive", str(max(total_users - active_users, 0))),
                    ("Admin safeguard", "Enabled"),
                ]
            )
            render_route_block(
                "Role model",
                "super_admin/admin -> full access\nmember -> main app access\nviewer -> no developer access unless enabled manually",
            )

    with users_tab:
        create_col, manage_col = st.columns([0.95, 1.05], gap="large")
        with create_col:
            with st.container(border=True):
                render_card_header(
                    "Create User",
                    "Create a new local account and assign its base role in one step.",
                    "User Management",
                )
                with st.form("admin_create_user_form", clear_on_submit=False):
                    st.text_input("New username", key="admin_new_username")
                    st.text_input("Display name", key="admin_new_display_name")
                    st.text_input("Temporary password", key="admin_new_password", type="password")
                    st.selectbox("Role", options=["member", "viewer", "admin"], key="admin_new_role")
                    create_user_submitted = st.form_submit_button(
                        "Create User Account",
                        use_container_width=True,
                        type="primary",
                    )
                if create_user_submitted:
                    ok, message = create_auth_user(
                        st.session_state.admin_new_username,
                        st.session_state.admin_new_display_name or st.session_state.admin_new_username,
                        st.session_state.admin_new_password,
                        st.session_state.admin_new_role,
                    )
                    if ok:
                        queue_reset("clear_admin_create_user_form", message)
                        st.rerun()
                    else:
                        st.error(message)
                if filtered_users:
                    st.markdown("#### Current Directory")
                    for user in filtered_users[:6]:
                        status_note = "active" if user["is_active"] else "disabled"
                        render_route_block(
                            f"{user['username']} • {user['role']}",
                            f"{user['display_name']}\n{status_note}",
                        )

        with manage_col:
            with st.container(border=True):
                render_card_header(
                    "Manage Existing Users",
                    "Edit roles, status, and page-level privileges. Password resets are local and immediate.",
                    "Access Control",
                )
                filter_col, select_col = st.columns([0.45, 0.55], gap="small")
                filter_col.selectbox("Role filter", options=["All", "super_admin", "admin", "member", "viewer"], key="admin_filter_role")
                selected_options = filtered_users or users
                if not selected_options:
                    st.caption("No users available.")
                else:
                    selected_index = 0
                    existing_id = int(st.session_state.admin_selected_user_id or 0)
                    option_ids = [int(user["id"]) for user in selected_options]
                    if existing_id in option_ids:
                        selected_index = option_ids.index(existing_id)
                    selected_user_id = select_col.selectbox(
                        "Select user",
                        options=option_ids,
                        index=selected_index,
                        format_func=lambda value: next(
                            f"{user['username']} ({user['role']})" for user in selected_options if int(user["id"]) == int(value)
                        ),
                        key="admin_selected_user_id",
                    )
                    selected_user = get_user_by_id(int(selected_user_id))
                    if selected_user:
                        default_permissions = selected_user["permissions"]
                        is_super_admin_target = str(selected_user["role"]) == "super_admin"
                        current_is_super_admin = st.session_state.auth_role == "super_admin"
                        can_manage_target = current_is_super_admin or not is_super_admin_target
                        if not can_manage_target:
                            st.warning("Only a super admin can edit another super admin account.")
                        display_name = st.text_input("Display name", value=str(selected_user["display_name"]), key=f"admin_display_name_{selected_user_id}")
                        role_value = st.selectbox(
                            "Role",
                            options=["super_admin", "admin", "member", "viewer"],
                            index=["super_admin", "admin", "member", "viewer"].index(str(selected_user["role"])),
                            key=f"admin_role_{selected_user_id}",
                        )
                        active_value = st.checkbox("Account active", value=bool(selected_user["is_active"]), key=f"admin_active_{selected_user_id}")
                        st.markdown("#### Page Permissions")
                        perm_cols = st.columns(2, gap="small")
                        permissions_keys = ["hugyoku", "hugyoku_chat", "dashboard", "workspaces", "academics", "developer", "history", "settings", "admin"]
                        permission_values: dict[str, bool] = {}
                        for idx, permission_key in enumerate(permissions_keys):
                            target_col = perm_cols[idx % 2]
                            with target_col:
                                permission_values[permission_key] = st.checkbox(
                                    permission_key.replace("_", " ").title(),
                                    value=bool(default_permissions.get(permission_key, False)),
                                    key=f"perm_{selected_user_id}_{permission_key}",
                                )
                        action_row = st.columns(2, gap="small")
                        if action_row[0].button(
                            "Save User Changes",
                            key=f"save_user_{selected_user_id}",
                            use_container_width=True,
                            type="primary",
                            disabled=not can_manage_target,
                        ):
                            ok, message = update_auth_user(
                                int(selected_user_id),
                                display_name,
                                role_value,
                                active_value,
                                permission_values,
                            )
                            if ok:
                                if int(selected_user_id) == int(st.session_state.auth_user_id):
                                    refreshed = get_user_by_id(int(selected_user_id))
                                    if refreshed:
                                        apply_auth_session(refreshed)
                                st.session_state.flash_message = message
                                st.session_state.flash_level = "success"
                                st.rerun()
                            else:
                                st.error(message)
                        st.text_input("Reset password", key="admin_reset_password", type="password")
                        if action_row[1].button(
                            "Update Password",
                            key=f"reset_user_password_{selected_user_id}",
                            use_container_width=True,
                            disabled=not can_manage_target,
                        ):
                            ok, message = update_auth_password(int(selected_user_id), st.session_state.admin_reset_password)
                            if ok:
                                queue_reset("clear_admin_password_reset", message)
                                st.rerun()
                            else:
                                st.error(message)

    with logs_tab:
        with st.container(border=True):
            render_card_header(
                "Authentication Logs",
                "Recent account events for this local app instance.",
                "Audit Trail",
            )
            for row in auth_log_rows(limit=60):
                render_route_block(
                    f"{row['created_at']} • {row['event_type']}",
                    f"{row['username']}\n{row['details']}",
                )


def render_header(ai_ready: bool, model_label: str, ai_message: str) -> None:
    workspace = active_workspace()
    local_access = using_local_access_mode()
    title = f"{current_identity_name()}'s Premium Study Desk"
    subtitle = (
        "Unified dashboard for workspaces, source-grounded analysis, study generators, "
        "developer support, history, and export controls."
    )
    status_text = "AI ready for academics" if ai_ready else ai_message
    chip_class = "ready" if ai_ready else ("waiting" if "Add HF_TOKEN" in ai_message or "Streamlit secrets" in ai_message else "offline")
    current_page_title = PAGE_DETAILS.get(st.session_state.active_page, {}).get("title", "Dashboard")
    current_mode = "Local folder picker" if save_destination_mode() == "local" else "Browser download"
    current_template = str(st.session_state.get("export_template", "Academic Classic"))

    if st.session_state.active_page == "hugyoku_chat":
        return

    left, right = st.columns([1.72, 0.98], gap="large")
    with left:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="app-hero-shell">
                  <div class="app-card-topline">
                    <span class="app-anchor-badge">HQ</span>
                    <span class="app-tier-pill primary">Command Center</span>
                  </div>
                  <div class="app-hero-title">{html_text(title)}</div>
                  <div class="app-hero-lead">{html_text(subtitle)}</div>
                  <div class="app-hero-note">Focused workflows for research, drafting, review, and export.</div>
                  <div class="app-luxury-rule"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            render_kpi_row(
                [
                    ("Current page", current_page_title),
                    ("Export mode", current_mode),
                    ("Workspace", str(workspace.get("name", "General Workspace"))),
                ]
            )
            action_a, action_b, action_c, action_d = st.columns([1, 1, 1, 1], gap="small")
            if action_a.button("Open Hugyoku", key="hero_open_hugyoku", type="primary", use_container_width=True):
                go("hugyoku")
            if action_b.button("Open Hugyoku Chat", key="hero_open_hugyoku_chat", use_container_width=True):
                go("hugyoku_chat")
            if action_c.button("Open Academics", key="hero_open_academics", use_container_width=True):
                go("academics")
            if action_d.button("Open Developer", key="hero_open_developer", use_container_width=True):
                go("developer")
    with right:
        with st.container(border=True):
            render_card_header(
                "Live Control Panel",
                "Real-time session status, model awareness, and operator context stay visible in one compact panel.",
                "System Status",
                anchor="AI",
                tier="secondary",
                compact=True,
            )
            st.markdown(
                f"<div class='app-status-pill {chip_class}'>{html_text(status_text)}</div>",
                unsafe_allow_html=True,
            )
            render_meta_grid(
                [
                    ("Access mode", "Direct local access" if local_access else (st.session_state.auth_username or "No active user")),
                    ("Active model", model_label),
                ]
            )
            with st.expander("Session details", expanded=False):
                render_meta_grid(
                    [
                        ("Role", "Workspace unlocked" if local_access else (st.session_state.auth_role or "None")),
                        ("History entries", str(len(st.session_state.get("history_entries", [])))),
                        ("Template", current_template),
                    ]
                )
            if st.button("Refresh AI Status", key="refresh_ai_status", use_container_width=True):
                st.rerun()


def render_sidebar(ai_ready: bool, model_label: str, ai_message: str) -> None:
    local_access = using_local_access_mode()
    nav_items = [
        ("hugyoku", "01 Hugyoku"),
        ("hugyoku_chat", "02 Hugyoku Chat"),
        ("dashboard", "03 Dashboard"),
        ("workspaces", "04 Workspaces"),
        ("academics", "05 Academics"),
        ("developer", "06 Developer"),
        ("history", "07 History"),
        ("settings", "08 Settings"),
    ]
    if can_access_page("admin"):
        nav_items.append(("admin", "09 Admin"))

    with st.sidebar:
        st.markdown(
            """
            <div class="app-sidebar-brand-row">
              <span class="app-anchor-badge">HY</span>
              <div>
                <div class="app-sidebar-brand">Hugyoku</div>
                <div class="app-sidebar-copy">Private academic command desk for grounded research, drafting, exports, and developer support.</div>
                <div class="app-sidebar-quiet">Compact navigation rail with live session context.</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div class='app-nav-section'>Navigate</div>", unsafe_allow_html=True)

        academic_pages = {"academics", "quiz", "assignment", "essay", "activity", "document"}
        developer_pages = {"developer", "codefix"}
        for page, label in nav_items:
            if not can_access_page(page):
                continue
            active = (
                page == "academics" and st.session_state.active_page in academic_pages
            ) or (
                page == "developer" and st.session_state.active_page in developer_pages
            ) or st.session_state.active_page == page
            if st.button(
                label,
                key=f"nav_{page}",
                type="primary" if active else "secondary",
                use_container_width=True,
            ):
                go(page)

        ensure_workspace_bootstrap()
        workspace_ids = list(st.session_state.workspaces.keys())
        if st.session_state.active_page == "hugyoku_chat":
            with st.expander("Chat context", expanded=False):
                selected_workspace = st.selectbox(
                    "Active workspace",
                    options=workspace_ids,
                    index=workspace_ids.index(st.session_state.active_workspace_id),
                    format_func=workspace_option_label,
                    key="sidebar_workspace_selector_chat",
                )
                if selected_workspace != st.session_state.active_workspace_id:
                    st.session_state.active_workspace_id = selected_workspace
                    st.rerun()
                st.caption("Use the compact chat shell for the thread. Open other pages when you need full workspace controls.")
                if local_access:
                    st.caption("Login is disabled on this install, so direct access stays enabled.")
                elif st.button("Logout", key="sidebar_logout_button_chat", use_container_width=True):
                    logout_current_user()
                    st.session_state.flash_message = "You have been logged out."
                    st.session_state.flash_level = "info"
                    st.rerun()
            return

        with st.container(border=True):
            render_card_header(
                "Workspace Focus",
                "Switch context before generating, reviewing, or exporting anything.",
                "Control",
                anchor="WS",
                tier="secondary",
                compact=True,
            )
            selected_workspace = st.selectbox(
                "Active workspace",
                options=workspace_ids,
                index=workspace_ids.index(st.session_state.active_workspace_id),
                format_func=workspace_option_label,
                key="sidebar_workspace_selector",
            )
            if selected_workspace != st.session_state.active_workspace_id:
                st.session_state.active_workspace_id = selected_workspace
                st.rerun()
            workspace = active_workspace()
            render_kpi_row(
                [
                    ("Files", str(len(workspace.get("files", [])))),
                    ("Images", str(len(workspace.get("images", [])))),
                ]
            )
            st.caption("Your active workspace controls what gets grouped, cited, and exported.")

        with st.container(border=True):
            render_card_header(
                "Session Control",
                "Your identity, role, and model context are grouped here so the sidebar stays compact.",
                "Access",
                anchor="ID",
                tier="tertiary",
                compact=True,
            )
            render_meta_grid(
                [
                    ("User", st.session_state.auth_display_name or st.session_state.auth_username or "Unknown user"),
                    ("Role", "Direct local access" if local_access else (st.session_state.auth_role or "none")),
                ]
            )
            st.caption(
                "Login is disabled in this build, so the workspace opens directly."
                if local_access
                else "Use the app for studying, drafting, and understanding source material before submitting anything."
            )
            if not local_access and st.button("Logout", key="sidebar_logout_button", use_container_width=True):
                logout_current_user()
                st.session_state.flash_message = "You have been logged out."
                st.session_state.flash_level = "info"
                st.rerun()

        with st.expander("Session diagnostics", expanded=False):
            st.caption("AI status")
            st.write("Ready" if ai_ready else ai_message)
            st.caption(model_label)
            st.caption(f"Export mode: {'Local folder picker' if save_destination_mode() == 'local' else 'Browser download'}")


def render_hugyoku_page(ai_ready: bool) -> None:
    workspace = active_workspace()
    doc_files = list(st.session_state.get("hugyoku_reference_docs") or [])
    image_files = list(st.session_state.get("hugyoku_reference_images") or [])
    output_sections = list(st.session_state.get("hugyoku_output_sections", []))
    has_understanding = bool(st.session_state.hugyoku_understanding.strip())
    has_result = bool(output_sections)
    stage = int(st.session_state.get("hugyoku_stage", 1) or 1)
    if stage >= 3 and has_result:
        stage = max(stage, 3)
    elif has_understanding:
        stage = max(stage, 2)
    else:
        stage = 1
    st.session_state.hugyoku_stage = stage

    with st.container(border=True):
        render_card_header(
            PAGE_DETAILS["hugyoku"]["title"],
            PAGE_DETAILS["hugyoku"]["subtitle"],
            "Universal Flow",
            anchor="HY",
            tier="primary",
        )
        render_kpi_row(
            [
                ("Workspace", str(workspace.get("name", "General Workspace"))),
                ("Docs", str(len(doc_files))),
                ("Images", str(len(image_files))),
                ("Status", "Result ready" if stage >= 3 else ("Understanding ready" if stage >= 2 else "Awaiting task")),
            ]
        )
        st.caption("Flow: 1) Task intake -> 2) AI understanding and corrections -> 3) Final result, editing, and export.")

    def persist_hugyoku_result(result_text: str, export_format: str, generation_note: str) -> None:
        sections = build_hugyoku_sections(result_text)
        output_title = guess_hugyoku_title(st.session_state.hugyoku_task_input, st.session_state.hugyoku_understanding, sections)
        st.session_state.hugyoku_output_sections = sections
        prime_hugyoku_section_widgets(sections)
        st.session_state.hugyoku_output_raw = compile_hugyoku_sections(sections)
        st.session_state.hugyoku_output_title = output_title
        st.session_state.hugyoku_output_format = export_format
        st.session_state.hugyoku_generation_note = generation_note
        remember_output("Hugyoku", output_title, st.session_state.hugyoku_output_raw, "hugyoku", "hugyoku")

    def run_understanding_analysis() -> None:
        task_text = st.session_state.hugyoku_task_input.strip()
        reference_bundle, issues, ocr_status = read_hugyoku_reference_bundle(doc_files, image_files, st.session_state.hugyoku_attachment_note)
        for issue in issues:
            st.warning(issue)
        if not task_text and not reference_bundle:
            st.warning("Add a task, a document, or an image first so Hugyoku has something to analyze.")
            return
        result, used_model = run_generation_with_details(
            build_hugyoku_understanding_prompt(task_text, reference_bundle),
            "hugyoku task understanding",
        )
        if result:
            st.session_state.hugyoku_understanding = result
            st.session_state.hugyoku_last_bundle = reference_bundle
            st.session_state.hugyoku_last_ocr_status = ocr_status
            st.session_state.hugyoku_stage = 2
            st.session_state.hugyoku_refinement_round = 1
            st.session_state.hugyoku_output_sections = []
            st.session_state.hugyoku_output_raw = ""
            st.session_state.hugyoku_output_title = ""
            st.session_state.hugyoku_result_prompt = ""
            st.session_state.hugyoku_output_format = detect_requested_export_format(task_text, result)
            st.session_state.hugyoku_generation_note = f"Understanding prepared using {used_model or current_model_name() or 'the active model'}."
            append_history_entry(
                "analysis",
                "Hugyoku understanding ready",
                ocr_status or "Task understanding generated.",
                "hugyoku",
                active_workspace_name(),
                "hugyoku",
            )
            st.session_state.flash_message = "Step 1 complete. Review the AI understanding in Step 2."
            st.session_state.flash_level = "success"
            st.rerun()

    def run_understanding_revision() -> None:
        refinement_prompt = st.session_state.hugyoku_refinement_prompt.strip()
        if not refinement_prompt:
            st.warning("Add a correction prompt first, or skip this step if the understanding is already correct.")
            return
        task_text = st.session_state.hugyoku_task_input.strip()
        reference_bundle = st.session_state.hugyoku_last_bundle
        if not reference_bundle:
            reference_bundle, issues, ocr_status = read_hugyoku_reference_bundle(doc_files, image_files, st.session_state.hugyoku_attachment_note)
            for issue in issues:
                st.warning(issue)
            st.session_state.hugyoku_last_bundle = reference_bundle
            st.session_state.hugyoku_last_ocr_status = ocr_status
        result, used_model = run_generation_with_details(
            build_hugyoku_refinement_prompt(task_text, reference_bundle, st.session_state.hugyoku_understanding, refinement_prompt),
            "hugyoku understanding revision",
        )
        if result:
            st.session_state.hugyoku_understanding = result
            st.session_state.hugyoku_stage = 2
            st.session_state.hugyoku_refinement_round = max(int(st.session_state.hugyoku_refinement_round or 0), 0) + 1
            st.session_state.hugyoku_output_sections = []
            st.session_state.hugyoku_output_raw = ""
            st.session_state.hugyoku_output_title = ""
            st.session_state.hugyoku_result_prompt = ""
            st.session_state.hugyoku_output_format = detect_requested_export_format(f"{task_text}\n{refinement_prompt}", result)
            st.session_state.hugyoku_generation_note = f"Understanding refined using {used_model or current_model_name() or 'the active model'}."
            st.session_state.hugyoku_refinement_prompt = ""
            append_history_entry(
                "analysis",
                "Hugyoku understanding revised",
                "The task understanding loop ran again with user corrections.",
                "hugyoku",
                active_workspace_name(),
                "hugyoku",
            )
            st.session_state.flash_message = "Understanding updated. If it looks correct now, continue to the final result."
            st.session_state.flash_level = "success"
            st.rerun()

    def run_final_generation() -> None:
        task_text = st.session_state.hugyoku_task_input.strip()
        reference_bundle = st.session_state.hugyoku_last_bundle
        if not reference_bundle:
            reference_bundle, issues, ocr_status = read_hugyoku_reference_bundle(doc_files, image_files, st.session_state.hugyoku_attachment_note)
            for issue in issues:
                st.warning(issue)
            st.session_state.hugyoku_last_bundle = reference_bundle
            st.session_state.hugyoku_last_ocr_status = ocr_status
        export_format = detect_requested_export_format(
            f"{task_text}\n{st.session_state.hugyoku_refinement_prompt}",
            st.session_state.hugyoku_understanding,
        )
        result, used_model = run_generation_with_details(
            build_hugyoku_generation_prompt(
                task_text,
                reference_bundle,
                st.session_state.hugyoku_understanding,
                export_format,
                st.session_state.hugyoku_refinement_prompt.strip(),
            ),
            "hugyoku final output",
        )
        if result:
            persist_hugyoku_result(
                result,
                export_format,
                f"Final result generated using {used_model or current_model_name() or 'the active model'}.",
            )
            st.session_state.hugyoku_stage = 3
            st.session_state.flash_message = "Final result generated. Step 3 is now ready for editing and export."
            st.session_state.flash_level = "success"
            st.rerun()

    if has_result:
        sync_hugyoku_sections_from_widgets()
        compiled_output = st.session_state.hugyoku_output_raw.strip()
        result_left, result_right = st.columns([1.05, 0.95], gap="large")
        with result_left:
            with st.container(border=True):
                render_card_header(
                    "Final Result",
                    "This is now the main focus. Review the output here first, then export or refine it from the panel on the right.",
                    "Step 4",
                    anchor="RS",
                    tier="primary",
                )
                render_preview_panel(
                    "Output Preview",
                    "The generated result stays pinned here so it is easy to see and review.",
                    "Final output preview",
                    compiled_output,
                    height=500,
                    empty_title="No result generated yet",
                    empty_body="Generate the final result first. It will appear here once the draft is ready.",
                    anchor="OP",
                    tier="secondary",
                )
                if compiled_output:
                    render_hugyoku_export_button(
                        st.session_state.hugyoku_output_title or "Hugyoku Output",
                        compiled_output,
                        st.session_state.hugyoku_output_format,
                    )
        with result_right:
            with st.container(border=True):
                render_card_header(
                    "Edit And Refine",
                    "Adjust each section, change the format, or send one more prompt after you see the result.",
                    "Controls",
                    anchor="ED",
                    tier="secondary",
                )
                st.text_input("Output title", key="hugyoku_output_title")
                st.selectbox(
                    "Export format",
                    options=["docx", "pdf", "txt"],
                    format_func=lambda value: value.upper(),
                    key="hugyoku_output_format",
                )
                for index, section in enumerate(output_sections):
                    heading_key = f"hugyoku_section_heading_{index}"
                    content_key = f"hugyoku_section_content_{index}"
                    if heading_key not in st.session_state:
                        st.session_state[heading_key] = str(section.get("heading", "")).strip()
                    if content_key not in st.session_state:
                        st.session_state[content_key] = str(section.get("content", "")).strip()
                    with st.expander(st.session_state.get(heading_key) or f"Section {index + 1}", expanded=index == 0):
                        st.text_input("Section heading", key=heading_key)
                        st.text_area("Section content", key=content_key, height=150)
                row_a, row_b = st.columns(2, gap="small")
                if row_a.button("Apply Section Edits", key="hugyoku_apply_section_edits", use_container_width=True, type="primary"):
                    sync_hugyoku_sections_from_widgets()
                    st.success("Section edits applied to the result preview.")
                if row_b.button("Start New Hugyoku Task", key="hugyoku_reset_after_result", use_container_width=True):
                    queue_reset("clear_hugyoku_workspace", "Hugyoku workflow reset. You can start a new task now.")
                    st.rerun()
                st.text_area(
                    "Additional prompt after result",
                    key="hugyoku_result_prompt",
                    height=120,
                    placeholder="Example: Make it more formal, shorten the answer, or convert it into a reviewer format.",
                )
                refine_a, refine_b = st.columns(2, gap="small")
                if refine_a.button("Regenerate With Additional Prompt", key="hugyoku_regenerate_output", use_container_width=True, type="secondary", disabled=not ai_ready):
                    additional_prompt = st.session_state.hugyoku_result_prompt.strip()
                    if not additional_prompt:
                        st.warning("Add an additional prompt first so Hugyoku knows what to improve.")
                    else:
                        sync_hugyoku_sections_from_widgets()
                        current_body = st.session_state.hugyoku_output_raw
                        revision_prompt = f"{additional_prompt}\n\nCurrent editable draft:\n{current_body}"
                        result, used_model = run_generation_with_details(
                            build_hugyoku_generation_prompt(
                                st.session_state.hugyoku_task_input.strip(),
                                st.session_state.hugyoku_last_bundle,
                                st.session_state.hugyoku_understanding,
                                st.session_state.hugyoku_output_format,
                                revision_prompt,
                            ),
                            "hugyoku refined output",
                        )
                        if result:
                            persist_hugyoku_result(
                                result,
                                st.session_state.hugyoku_output_format,
                                f"Result refined using {used_model or current_model_name() or 'the active model'}.",
                            )
                            st.session_state.hugyoku_stage = 3
                            st.session_state.hugyoku_result_prompt = ""
                            st.session_state.flash_message = "The final result was refined and updated."
                            st.session_state.flash_level = "success"
                            st.rerun()
                if refine_b.button("Save Current Draft To Workspace", key="hugyoku_save_current_draft", use_container_width=True):
                    sync_hugyoku_sections_from_widgets()
                    remember_output(
                        "Hugyoku Draft",
                        st.session_state.hugyoku_output_title or "Hugyoku Draft",
                        st.session_state.hugyoku_output_raw,
                        "hugyoku",
                        "hugyoku",
                    )
                    st.success("Current Hugyoku draft saved into the active workspace history.")
                with st.expander("Result notes", expanded=False):
                    render_route_block(
                        "Detected export route",
                        f"{st.session_state.hugyoku_output_format.upper()} output ready for {'local save' if save_destination_mode() == 'local' else 'browser download'}.",
                    )
                    render_route_block(
                        "Why this draft exists",
                        st.session_state.hugyoku_generation_note or "No generation note yet.",
                    )

    with st.expander("1. Task intake", expanded=stage == 1):
        with st.container(border=True):
            render_card_header(
                "Task Intake",
                "Describe the task and attach anything the AI should read first. Keep this focused on the assignment itself.",
                "Step 1",
                anchor="IN",
                tier="secondary",
            )
            st.text_area(
                "Input task",
                key="hugyoku_task_input",
                height=160,
                placeholder="Example: Make me an essay about Aristotle's life and submit it as a Word file. Include introduction, key contributions, and conclusion.",
            )
            upload_left, upload_right = st.columns(2, gap="small")
            with upload_left:
                st.file_uploader(
                    "Insert reference files",
                    type=["docx", "pdf", "txt", "md"],
                    accept_multiple_files=True,
                    key="hugyoku_reference_docs",
                    help="Attach assignment sheets, rubrics, notes, or source documents.",
                )
            with upload_right:
                st.file_uploader(
                    "Insert image",
                    type=["png", "jpg", "jpeg", "webp"],
                    accept_multiple_files=True,
                    key="hugyoku_reference_images",
                    help="Attach screenshots, worksheet images, or photo references.",
                )
            st.text_area(
                "Attachment note (optional)",
                key="hugyoku_attachment_note",
                height=85,
                placeholder="Use this only if the attachments need extra context before analysis.",
            )
            action_a, action_b = st.columns(2, gap="small")
            if action_a.button("Analyze Task Understanding", key="hugyoku_analyze_task", use_container_width=True, type="primary", disabled=not ai_ready):
                run_understanding_analysis()
            if action_b.button("Reset Hugyoku Flow", key="hugyoku_clear_workspace", use_container_width=True):
                queue_reset("clear_hugyoku_workspace", "Hugyoku workflow cleared.")
                st.rerun()

    if stage >= 2 and has_understanding:
        with st.expander("2. Review AI understanding", expanded=stage == 2):
            top_left, top_right = st.columns([1.08, 0.92], gap="large")
            with top_left:
                with st.container(border=True):
                    render_preview_panel(
                        "AI Understanding",
                        "Read this first. If the AI got the task wrong, use the correction box below. If it got the task right, continue to the final result.",
                        "Understanding preview",
                        st.session_state.hugyoku_understanding,
                        height=300,
                        empty_title="No understanding yet",
                        empty_body="Start from task intake first.",
                        anchor="UA",
                        tier="secondary",
                    )
            with top_right:
                with st.container(border=True):
                    render_card_header(
                        "Quick Summary",
                        "Use this short summary to confirm whether the AI understood the request correctly.",
                        "Step 2",
                        anchor="CF",
                        tier="tertiary",
                    )
                    render_meta_grid(
                        [
                            ("Requested output", extract_section_value(st.session_state.hugyoku_understanding, ["Requested Output"]) or "Not analyzed yet"),
                            ("Requested format", (extract_section_value(st.session_state.hugyoku_understanding, ["Requested File Format"]) or st.session_state.hugyoku_output_format).upper()),
                        ]
                    )
                    render_route_block(
                        "Task summary",
                        extract_section_value(st.session_state.hugyoku_understanding, ["Task Summary"]) or "No task summary yet.",
                    )
                    with st.expander("More analysis notes", expanded=False):
                        render_route_block(
                            "Important requirements",
                            extract_section_value(st.session_state.hugyoku_understanding, ["Important Requirements"]) or "No requirements captured yet.",
                        )
                        render_route_block(
                            "Missing or uncertain parts",
                            extract_section_value(st.session_state.hugyoku_understanding, ["Missing or Uncertain Parts"]) or "No missing parts were flagged.",
                        )
                        render_route_block("OCR status", st.session_state.hugyoku_last_ocr_status or "No image analysis has been run yet.")

            with st.container(border=True):
                render_card_header(
                    "Correct Or Continue",
                    "If may mali, ilagay mo dito ang correction. Kung tama na, diretso ka na sa final result.",
                    "Next Action",
                    anchor="NX",
                    tier="secondary",
                )
                st.text_area(
                    "Correction or clarification prompt",
                    key="hugyoku_refinement_prompt",
                    height=120,
                    placeholder="Example: Focus only on the significance of the name, keep it concise, and submit it as DOCX.",
                )
                action_a, action_b = st.columns(2, gap="small")
                if action_a.button("Revise Understanding", key="hugyoku_revise_understanding", use_container_width=True, type="secondary", disabled=not ai_ready):
                    run_understanding_revision()
                if action_b.button("Generate Final Result", key="hugyoku_generate_result", use_container_width=True, type="primary", disabled=not ai_ready):
                    run_final_generation()


def render_hugyoku_chat_page(ai_ready: bool) -> None:
    st.markdown(HUGYOKU_CHAT_V2_CSS, unsafe_allow_html=True)

    messages = list(st.session_state.get("hugyoku_chat_messages", []))
    reasoning_mode = str(st.session_state.get("hugyoku_chat_reasoning_mode", "Balanced"))
    selected_model = resolve_hugyoku_chat_model() or current_model_name() or "No model selected"
    last_used_model = st.session_state.get("hugyoku_chat_last_used_model") or "No response yet"
    workspace_name = active_workspace_name()
    upload_nonce = int(st.session_state.get("hugyoku_chat_upload_nonce", 0) or 0)
    show_full_history = bool(st.session_state.get("hugyoku_chat_show_full_history", False))

    def split_chat_uploads(uploaded_files: list[object]) -> tuple[list[object], list[object]]:
        doc_files: list[object] = []
        image_files: list[object] = []
        for uploaded_file in uploaded_files:
            suffix = Path(str(getattr(uploaded_file, "name", "")).lower()).suffix
            if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
                image_files.append(uploaded_file)
            else:
                doc_files.append(uploaded_file)
        return doc_files, image_files

    def send_hugyoku_chat(
        user_prompt: str,
        doc_files: list[object],
        image_files: list[object],
        audio_upload: object | None = None,
        *,
        attachment_bundle_override: str | None = None,
        append_user_message: bool = True,
    ) -> None:
        user_prompt = (user_prompt or "").strip()
        attachment_note = str(st.session_state.get("hugyoku_chat_attachment_note", "")).strip()
        voice_transcript, voice_status = transcribe_chat_audio(audio_upload)
        bundle_note_parts = [attachment_note]
        if voice_transcript:
            bundle_note_parts.append(f"[Voice Transcript]\n{voice_transcript}")
        combined_attachment_note = "\n\n".join(part for part in bundle_note_parts if part.strip())

        if attachment_bundle_override is None:
            attachment_bundle, issues, ocr_status = read_hugyoku_reference_bundle(
                doc_files,
                image_files,
                combined_attachment_note,
            )
        else:
            attachment_bundle = attachment_bundle_override.strip()
            issues = []
            ocr_status = ""
        for issue in issues:
            st.warning(issue)
        message_text = user_prompt or voice_transcript.strip()
        if not message_text and not attachment_bundle:
            st.warning("Type a message, add files, or record your voice first.")
            return

        requested_model = resolve_hugyoku_chat_model()
        if not requested_model:
            st.warning("Choose a valid AI model first.")
            return

        attachment_names = summarize_uploaded_names(doc_files) + summarize_uploaded_names(image_files)
        if audio_upload is not None:
            attachment_names.append(str(getattr(audio_upload, "name", "voice-note")).strip() or "voice-note")
        display_text = message_text or "Please analyze the attached files or images."
        if append_user_message:
            append_hugyoku_chat_message(
                "user",
                display_text,
                reasoning=reasoning_mode,
                attachments=attachment_names,
            )
        with st.spinner("Hugyoku is thinking..."):
            quick_response = build_hugyoku_chat_quick_response(
                display_text,
                requested_model,
                reasoning_mode,
                workspace_name,
                has_attachment_context=bool(attachment_bundle.strip()),
            )
            if quick_response:
                result = quick_response
                used_model = requested_model
            else:
                result, used_model = run_generation_with_details(
                    build_hugyoku_chat_prompt(display_text, attachment_bundle, reasoning_mode),
                    "hugyoku chat reply",
                    requested_model=requested_model,
                )
        if result:
            result = tighten_hugyoku_chat_response(result)
            append_hugyoku_chat_message(
                "assistant",
                result,
                model_name=used_model or requested_model,
                reasoning=reasoning_mode,
            )
            st.session_state.hugyoku_chat_last_bundle = attachment_bundle
            status_bits = [bit for bit in [ocr_status, voice_status] if bit]
            st.session_state.hugyoku_chat_last_ocr_status = " ".join(status_bits).strip()
            st.session_state.hugyoku_chat_last_used_model = used_model or requested_model
            append_history_entry(
                "generation",
                "Hugyoku Chat reply generated",
                short_preview(display_text, 160),
                "hugyoku_chat",
                active_workspace_name(),
                "hugyoku_chat",
            )
            queue_reset("clear_hugyoku_chat_composer")
            st.rerun()

    def find_last_user_index(messages_list: list[dict[str, object]]) -> int:
        for idx in range(len(messages_list) - 1, -1, -1):
            if str(messages_list[idx].get("role", "")).strip().lower() == "user":
                return idx
        return -1

    def open_last_prompt_editor() -> None:
        current_messages = list(st.session_state.get("hugyoku_chat_messages", []))
        last_user_idx = find_last_user_index(current_messages)
        if last_user_idx < 0:
            return
        st.session_state.hugyoku_chat_edit_mode = True
        st.session_state.hugyoku_chat_edit_text = str(current_messages[last_user_idx].get("content", "")).strip()

    def apply_last_prompt_edit(regenerate: bool) -> None:
        current_messages = list(st.session_state.get("hugyoku_chat_messages", []))
        last_user_idx = find_last_user_index(current_messages)
        updated_prompt = str(st.session_state.get("hugyoku_chat_edit_text", "")).strip()
        if last_user_idx < 0 or not updated_prompt:
            st.warning("Add a valid prompt before saving the edit.")
            return
        current_messages[last_user_idx]["content"] = updated_prompt
        if regenerate:
            current_messages = current_messages[: last_user_idx + 1]
        st.session_state.hugyoku_chat_messages = current_messages
        st.session_state.hugyoku_chat_edit_mode = False
        if regenerate:
            bundle_text = str(st.session_state.get("hugyoku_chat_last_bundle", "")).strip()
            send_hugyoku_chat(
                updated_prompt,
                [],
                [],
                None,
                attachment_bundle_override=bundle_text,
                append_user_message=False,
            )
            return
        st.success("Last prompt updated.")
        st.rerun()

    pending_transcript = str(st.session_state.get("hugyoku_chat_pending_transcript", "")).strip()
    visible_messages = messages if show_full_history else messages[-18:]
    hidden_count = max(0, len(messages) - len(visible_messages))
    last_user_exists = find_last_user_index(messages) >= 0

    uploaded_refs: list[object] = []
    audio_upload = None

    st.markdown("<div class='hugyoku-chat-v2-root'>", unsafe_allow_html=True)
    st.markdown("<div class='hugyoku-chat-v2-topbar'><div class='hugyoku-chat-v2-topbar-row'>", unsafe_allow_html=True)
    top_left, top_right = st.columns([0.84, 0.16], gap="small")
    with top_left:
        st.markdown(
            f"""
            <div class="hugyoku-chat-v2-titlebar">
              <span class="hugyoku-chat-v2-topbar-icon">&#187;&#187;</span>
              <div class="hugyoku-chat-v2-title">{html_text(workspace_name)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_right:
        st.markdown("<div class='hugyoku-chat-v2-menu'>", unsafe_allow_html=True)
        with st.popover("⋯", use_container_width=True):
            st.selectbox("AI version", options=MODEL_SELECTION_OPTIONS, key="hugyoku_chat_model_choice")
            if st.session_state.hugyoku_chat_model_choice == "Custom":
                st.text_input("Custom AI model", key="hugyoku_chat_model_custom", placeholder="Custom model id")
            st.selectbox("Reasoning", options=["Fast", "Balanced", "Deep"], key="hugyoku_chat_reasoning_mode")
            st.checkbox("Show older messages", key="hugyoku_chat_show_full_history")
            uploaded_refs = st.file_uploader(
                "References",
                accept_multiple_files=True,
                type=["docx", "pdf", "txt", "md", "png", "jpg", "jpeg", "webp"],
                key=f"hugyoku_chat_refs_{upload_nonce}",
            )
            audio_upload = st.file_uploader(
                "Voice note",
                accept_multiple_files=False,
                type=["wav", "wave", "flac", "aiff", "aif"],
                key=f"hugyoku_chat_audio_{upload_nonce}",
            )
            doc_files_for_menu, image_files_for_menu = split_chat_uploads(list(uploaded_refs or []))
            if mic_transcription_available():
                transcript = speech_to_text(
                    language=st.session_state.get("hugyoku_chat_voice_language", "en-US"),
                    start_prompt="Record",
                    stop_prompt="Stop",
                    just_once=True,
                    use_container_width=True,
                    key=f"hugyoku_chat_mic_{upload_nonce}",
                )
                if transcript:
                    cleaned_transcript = str(transcript).strip()
                    if cleaned_transcript and cleaned_transcript != st.session_state.get("hugyoku_chat_last_transcript_text", ""):
                        st.session_state.hugyoku_chat_pending_transcript = cleaned_transcript
                        st.session_state.hugyoku_chat_last_transcript_text = cleaned_transcript
                        st.rerun()
            st.text_area(
                "Attachment note",
                key="hugyoku_chat_attachment_note",
                height=80,
                placeholder="Optional note for files, images, or voice context.",
            )
            if pending_transcript:
                st.caption(short_preview(pending_transcript, 160))
                transcript_a, transcript_b = st.columns(2, gap="small")
                if transcript_a.button("Send transcript", key="hugyoku_chat_send_transcript", use_container_width=True, type="primary", disabled=not ai_ready):
                    send_hugyoku_chat(pending_transcript, doc_files_for_menu, image_files_for_menu, audio_upload)
                if transcript_b.button("Clear transcript", key="hugyoku_chat_clear_transcript", use_container_width=True):
                    st.session_state.hugyoku_chat_pending_transcript = ""
                    st.rerun()
            if last_user_exists and st.button("Edit last prompt", key="hugyoku_chat_edit_last", use_container_width=True):
                open_last_prompt_editor()
            if st.button("New thread", key="hugyoku_chat_clear", use_container_width=True):
                queue_reset("clear_hugyoku_chat_workspace")
                st.rerun()
            st.caption(f"Current model: {selected_model}")
            st.caption(f"Last used: {last_used_model}")
            if st.session_state.hugyoku_chat_last_ocr_status:
                st.caption(st.session_state.hugyoku_chat_last_ocr_status)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    if st.session_state.get("hugyoku_chat_edit_mode", False):
        st.markdown("<div class='hugyoku-chat-v2-edit'>", unsafe_allow_html=True)
        with st.container(border=True):
            render_card_header(
                "Edit Last Prompt",
                "Refine the last user message, then regenerate the reply when the prompt looks right.",
                "Edit",
            )
            st.text_area(
                "Edited prompt",
                key="hugyoku_chat_edit_text",
                height=120,
                label_visibility="collapsed",
                placeholder="Update the last user prompt here.",
            )
            edit_a, edit_b, edit_c = st.columns(3, gap="small")
            if edit_a.button("Save Edit", key="hugyoku_chat_save_edit", use_container_width=True):
                apply_last_prompt_edit(False)
            if edit_b.button("Regenerate", key="hugyoku_chat_regen_edit", use_container_width=True, type="primary", disabled=not ai_ready):
                apply_last_prompt_edit(True)
            if edit_c.button("Cancel", key="hugyoku_chat_cancel_edit", use_container_width=True):
                st.session_state.hugyoku_chat_edit_mode = False
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='chat-container'><div class='chat-scroll'>", unsafe_allow_html=True)
    if hidden_count > 0 and not show_full_history:
        st.markdown("<div class='hugyoku-chat-v2-older'>", unsafe_allow_html=True)
        if st.button(f"Show {hidden_count} earlier message{'s' if hidden_count != 1 else ''}", key="hugyoku_chat_show_older"):
            st.session_state.hugyoku_chat_show_full_history = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if visible_messages:
        for message in visible_messages:
            role = str(message.get("role", "assistant")).strip().lower()
            bubble_class = "user" if role == "user" else "assistant"
            role_label = "You" if role == "user" else "Hugyoku"
            with st.chat_message("user" if role == "user" else "assistant"):
                st.markdown(f"<div class='chat-message {bubble_class}'>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='chat-message-role {bubble_class}'>{html_text(role_label)}</div>",
                    unsafe_allow_html=True,
                )
                header_bits: list[str] = []
                if message.get("timestamp"):
                    header_bits.append(str(message["timestamp"]))
                if message.get("reasoning"):
                    header_bits.append(f"Reasoning: {message['reasoning']}")
                if message.get("model"):
                    header_bits.append(f"Model: {message['model']}")
                if header_bits:
                    meta_html = "".join(f"<span>{html_text(bit)}</span>" for bit in header_bits)
                    st.markdown(f"<div class='chat-message-meta'>{meta_html}</div>", unsafe_allow_html=True)
                st.markdown(str(message.get("content", "")))
                attachments = list(message.get("attachments", []))
                if attachments:
                    chips = " ".join(f"<span class='hugyoku-chat-v2-chip'>{html_text(name)}</span>" for name in attachments)
                    st.markdown(chips, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='hugyoku-chat-v2-empty-hint'>Ask a question, attach a reference, or dictate a voice note to start the thread.</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div></div>", unsafe_allow_html=True)

    selected_doc_files, selected_image_files = split_chat_uploads(list(uploaded_refs or []))
    status_bits: list[str] = []
    if selected_doc_files:
        status_bits.append(f"{len(selected_doc_files)} file{'s' if len(selected_doc_files) != 1 else ''} attached")
    if selected_image_files:
        status_bits.append(f"{len(selected_image_files)} image{'s' if len(selected_image_files) != 1 else ''} attached")
    if audio_upload is not None:
        status_bits.append("voice note ready")
    if pending_transcript:
        status_bits.append("transcript ready")

    st.markdown("<div class='chat-input'><div class='chat-input-inner'>", unsafe_allow_html=True)
    if status_bits:
        st.markdown(f"<div class='chat-input-status'>{html_text(' • '.join(status_bits))}</div>", unsafe_allow_html=True)
    prompt = st.chat_input(
        "Message Hugyoku",
        key="hugyoku_chat_input_box",
        disabled=not ai_ready,
    )
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if prompt:
        send_hugyoku_chat(prompt, selected_doc_files, selected_image_files, audio_upload)

    if messages:
        render_hugyoku_chat_autoscroll(len(messages))


def render_dashboard() -> None:
    workspace = active_workspace()
    paths = folder_path_lines()
    current_mode = save_destination_mode()
    picker_ready = local_folder_picker_available()

    left, right = st.columns([1.15, 0.85], gap="large")
    with left:
        with st.container(border=True):
            render_card_header(
                "Profile Section",
                "Set your identity, choose how exports should behave, and keep the dashboard disciplined with compact progressive controls.",
                "Dashboard Identity",
                anchor="ID",
                tier="primary",
            )
            render_kpi_row(
                [
                    ("Identity", st.session_state.saved_name or "Session default"),
                    ("Date stamp", "Enabled" if st.session_state.profile_include_date_input else "Off"),
                    ("Destination", "Local" if st.session_state.profile_save_destination_mode_input == "local" else "Browser"),
                ]
            )
            identity_left, identity_right = st.columns([1.35, 0.65], gap="small")
            with identity_left:
                st.text_input("Enter your name", key="profile_name_input", placeholder="Name to attach to exports")
            with identity_right:
                st.checkbox("Add date today", key="profile_include_date_input")

            with st.expander("Save Destination", expanded=True):
                st.radio(
                    "Save destination",
                    options=["browser", "local"],
                    format_func=lambda value: (
                        "Browser Download (Mobile + PC Recommended)"
                        if value == "browser"
                        else "Local Folder Picker (Desktop Only)"
                    ),
                    key="profile_save_destination_mode_input",
                    horizontal=True,
                )

                if st.session_state.profile_save_destination_mode_input == "browser":
                    render_route_block(
                        "Save behavior",
                        "Works on both mobile and PC.\nTap the download button and let your browser save the file to your device.",
                    )
                    render_route_block("Download route", browser_export_label())
                else:
                    folder_col, pick_col, clear_col = st.columns([1.7, 0.9, 0.8], gap="small")
                    folder_col.text_input(
                        "Selected local folder",
                        value=st.session_state.profile_export_root_path_input or "",
                        disabled=True,
                        placeholder="No local folder selected yet",
                    )
                    if pick_col.button(
                        "Choose Folder",
                        key="choose_export_folder",
                        use_container_width=True,
                        disabled=not picker_ready,
                    ):
                        try:
                            selected_folder = pick_local_folder()
                            if selected_folder:
                                queue_export_root_selection(selected_folder)
                                st.rerun()
                        except Exception as exc:
                            st.warning(str(exc))
                    if clear_col.button("Clear Folder", key="clear_export_folder", use_container_width=True):
                        queue_export_root_selection(None)
                        st.rerun()

                    if picker_ready:
                        render_route_block(
                            "Desktop save behavior",
                            "Exports save directly into the selected folder with automatic tool subfolders.",
                        )
                    else:
                        st.info("Local folder picking is not available here, so browser download is the cross-device fallback.")

            with st.expander("Output Options", expanded=False):
                opt_left, opt_right = st.columns(2, gap="small")
                with opt_left:
                    st.checkbox("Include saved name in export", key="profile_output_include_name_input")
                    st.checkbox("Include date in export", key="profile_output_include_date_input")
                with opt_right:
                    st.checkbox("Include essay heading suggestion", key="profile_essay_include_heading_input")
                    st.checkbox("Include self-check tip", key="profile_essay_include_tip_input")

            action_left, action_right = st.columns(2, gap="small")
            if action_left.button("Save Profile", use_container_width=True, type="primary", key="dashboard_save_profile"):
                save_profile()
                st.success("Profile saved for this session.")
            if action_right.button("Clear Saved Profile", use_container_width=True, key="dashboard_clear_profile"):
                queue_reset("clear_profile", "Profile cleared.")
                st.rerun()

    with right:
        with st.container(border=True):
            render_card_header(
                "Active Workspace Snapshot",
                "Track the current project workspace, uploaded materials, output template, and export routing in one place.",
                "Workspace Overview",
                anchor="WS",
                tier="secondary",
            )
            render_meta_grid(
                [
                    ("Workspace", str(workspace.get("name", "General Workspace"))),
                    ("Source files", str(len(workspace.get("files", [])))),
                    ("Screenshots", str(len(workspace.get("images", [])))),
                    ("Saved outputs", str(len(workspace.get("outputs", [])))),
                ]
            )
            render_route_block(
                "Save destination",
                paths["main"] if current_mode == "local" else "Browser download to the user's device",
            )
            render_route_block(
                "Current mode",
                "Local folder picker" if current_mode == "local" else "Browser download (mobile + PC)",
            )
            render_route_block("Selected template", str(st.session_state.get("export_template", "Academic Classic")))

    with st.expander("Additional dashboard panels", expanded=False):
        extra_a, extra_b, extra_c, extra_d = st.tabs(["Quick Launch", "Recent Activity", "Routing", "Outputs"])
        with extra_a:
            first_col, second_col = st.columns(2, gap="small")
            if first_col.button("Open Workspaces", key="dashboard_open_workspaces", use_container_width=True, type="primary"):
                go("workspaces")
            if second_col.button("Open Academics", key="dashboard_open_academics", use_container_width=True):
                go("academics")
            third_col, fourth_col = st.columns(2, gap="small")
            if third_col.button("Open Developer", key="dashboard_open_developer", use_container_width=True):
                go("developer")
            if fourth_col.button("Open Settings", key="dashboard_open_settings", use_container_width=True):
                go("settings")
        with extra_b:
            render_history_snippets(limit=4)
        with extra_c:
            render_route_block("Academics suite", "\n".join([paths["reviewer"], paths["flashcards"], paths["practice_test"], paths["rubric"], paths["batch"]]))
            render_route_block("Developer suite", paths["codefix"])
        with extra_d:
            render_workspace_outputs(limit=4)


def render_workspaces_page(ai_ready: bool) -> None:
    workspace = active_workspace()
    with st.container(border=True):
        render_card_header(
            PAGE_DETAILS["workspaces"]["title"],
            PAGE_DETAILS["workspaces"]["subtitle"],
            "Workspace Manager",
            anchor="WS",
            tier="primary",
        )
        render_tag_row(["Project Workspaces", "Multi-File Upload", "Screenshot Intake", "Workspace Analysis"])

    top_left, top_right = st.columns(2, gap="large")
    with top_left:
        with st.container(border=True):
            render_card_header(
                "Create Workspace",
                "Use dedicated workspaces to separate subjects, projects, and source libraries.",
                "Create",
            )
            st.text_input("Workspace name", key="workspace_new_name_input")
            st.text_area("Workspace description", key="workspace_new_description_input", height=110)
            if st.button("Create Workspace", key="create_workspace_button", use_container_width=True, type="primary"):
                if create_workspace(st.session_state.workspace_new_name_input, st.session_state.workspace_new_description_input):
                    st.session_state.workspace_new_name_input = ""
                    st.session_state.workspace_new_description_input = ""
                    st.success("Workspace created.")
                    st.rerun()
                else:
                    st.warning("Enter a workspace name first.")

    with top_right:
        with st.container(border=True):
            render_card_header(
                "Active Workspace",
                "Switch workspaces here, inspect current stats, or remove the current workspace.",
                "Current Context",
            )
            workspace_ids = list(st.session_state.workspaces.keys())
            selector = st.selectbox(
                "Choose workspace",
                options=workspace_ids,
                index=workspace_ids.index(st.session_state.active_workspace_id),
                format_func=workspace_option_label,
                key="workspace_page_selector",
            )
            if selector != st.session_state.active_workspace_id:
                st.session_state.active_workspace_id = selector
                st.rerun()
            workspace = active_workspace()
            render_meta_grid(
                [
                    ("Created", str(workspace.get("created_at", "-"))),
                    ("Files", str(len(workspace.get("files", [])))),
                    ("Images", str(len(workspace.get("images", [])))),
                    ("Words", str(workspace_word_count(workspace))),
                ]
            )
            if len(st.session_state.workspaces) > 1 and st.button("Delete Active Workspace", key="delete_workspace_button", use_container_width=True):
                if delete_active_workspace():
                    st.success("Workspace deleted.")
                    st.rerun()

    mid_left, mid_right = st.columns(2, gap="large")
    with mid_left:
        with st.container(border=True):
            render_card_header(
                "Source Library",
                "Upload multiple text documents and add them to the active workspace in one step.",
                "Files",
            )
            uploaded_files = st.file_uploader(
                "Upload .docx, .pdf, .txt, or .md files",
                type=["docx", "pdf", "txt", "md"],
                accept_multiple_files=True,
                key="workspace_file_upload",
            )
            if st.button("Add Files To Workspace", key="add_workspace_files", use_container_width=True, type="primary"):
                if uploaded_files:
                    added, failures = add_source_files_to_active_workspace(uploaded_files)
                    if added:
                        st.success(f"Added {added} file(s) to {active_workspace_name()}.")
                    for failure in failures:
                        st.warning(failure)
                    st.rerun()
                else:
                    st.warning("Upload at least one file first.")
            file_names = [str(item.get("name", "")) for item in workspace.get("files", [])]
            st.caption("Current files: " + (", ".join(file_names[:8]) if file_names else "No files added yet."))

    with mid_right:
        with st.container(border=True):
            render_card_header(
                "Workspace Notes",
                "Keep manual notes, instructions, or OCR fallbacks attached to the current workspace.",
                "Notes",
            )
            notes_value = st.text_area(
                "Workspace notes",
                value=str(workspace.get("notes", "")),
                height=200,
                key=f"workspace_notes_editor_{workspace['id']}",
            )
            if st.button("Save Workspace Notes", key=f"save_workspace_notes_{workspace['id']}", use_container_width=True):
                workspace["notes"] = notes_value.strip()
                append_history_entry("workspace", f"Updated notes for {workspace['name']}", "Workspace notes saved.", "workspaces", str(workspace["name"]))
                st.success("Workspace notes saved.")

    bottom_left, bottom_right = st.columns(2, gap="large")
    with bottom_left:
        with st.container(border=True):
            render_card_header(
                "Screenshot Intake",
                "Attach screenshots or photos to the active workspace. OCR is not enabled yet, but the image record stays with the workspace.",
                "Images",
            )
            image_caption = st.text_input("Optional image note", key="workspace_image_caption")
            uploaded_images = st.file_uploader(
                "Upload screenshots",
                type=["png", "jpg", "jpeg", "webp"],
                accept_multiple_files=True,
                key="workspace_image_upload",
            )
            if st.button("Add Screenshots", key="add_workspace_images", use_container_width=True):
                if uploaded_images:
                    added = add_images_to_active_workspace(uploaded_images, image_caption)
                    st.success(f"Added {added} screenshot(s) to {active_workspace_name()}.")
                    st.rerun()
                else:
                    st.warning("Upload at least one image first.")
            with st.expander("Preview attached screenshots", expanded=False):
                if workspace.get("images"):
                    preview_images = [item.get("bytes") for item in workspace.get("images", [])[:3]]
                    st.image(preview_images, width=180)
                else:
                    st.caption("No screenshots attached yet.")

    with bottom_right:
        with st.container(border=True):
            render_card_header(
                "Workspace Analysis",
                "Generate a quick analysis over all current sources and notes inside the active workspace.",
                "Analysis",
            )
            source_bundle = workspace_source_bundle(workspace)
            st.caption(f"Prompt-ready source length: {len(source_bundle)} characters")
            if st.button(
                "Analyze Workspace Sources",
                key="analyze_workspace_sources",
                use_container_width=True,
                type="primary",
                disabled=not ai_ready,
            ):
                if not source_bundle:
                    st.warning("Add files, screenshots, or notes to the workspace first.")
                else:
                    prompt = (
                        "Analyze the study workspace sources below.\n\n"
                        f"Workspace: {workspace['name']}\n"
                        f"Description: {workspace.get('description', '') or 'No description provided'}\n\n"
                        f"Sources:\n{trim_prompt_source(source_bundle)}\n\n"
                        "Return these plain-text sections in this exact order:\n"
                        "Summary:\n"
                        "Key Concepts:\n"
                        "Likely Focus Areas:\n"
                        "Study Advice:\n\n"
                        "Do not use markdown symbols like ### or ####."
                    )
                    result = run_generation(prompt, "workspace analysis")
                    if result:
                        st.session_state.workspace_analysis_result = result
                        remember_output("Workspace Analysis", f"{workspace['name']} Workspace Analysis", result, "workspaces", "workspace_analysis")
                        st.success("Workspace analysis ready.")
            if st.session_state.workspace_analysis_result.strip():
                st.text_area("Analysis output", value=st.session_state.workspace_analysis_result, height=260, disabled=True)
            else:
                render_route_block(
                    "No analysis yet",
                    "Generate the workspace analysis first. This panel stays compact until there is a result to review.",
                )
            if st.session_state.workspace_analysis_result.strip():
                render_download_button(
                    f"{workspace['name']} Workspace Analysis",
                    st.session_state.workspace_analysis_result,
                    sanitize_filename(f"{workspace['name']}_workspace_analysis".lower().replace(" ", "_")),
                    "workspace_analysis",
                    "clear_workspace_analysis_workspace",
                )
    with st.expander("Additional workspace panels", expanded=False):
        list_left, list_right = st.columns(2, gap="large")
        with list_left:
            with st.container(border=True):
                render_card_header(
                    "Source Inventory",
                    "A quick list of the file assets currently attached to the active workspace.",
                    "Inventory",
                    compact=True,
                )
                if workspace.get("files"):
                    for file_entry in workspace.get("files", [])[:10]:
                        render_route_block(
                            str(file_entry.get("name", "source.txt")),
                            f"{file_entry.get('words', 0)} words • added {file_entry.get('added_at', '-')}",
                        )
                else:
                    st.caption("No source files in this workspace yet.")

        with list_right:
            with st.container(border=True):
                render_card_header(
                    "Workspace Outputs",
                    "Generated outputs remain attached to the active workspace for quick reuse.",
                    "Outputs",
                    compact=True,
                )
                render_workspace_outputs(limit=6)
