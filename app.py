import streamlit as st
import pandas as pd
import subprocess
import os

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FeedbackIQ",
    page_icon="📋",
    layout="wide"
)

# ── Styling ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f0f4ff;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem; max-width: 1400px; }

/* ── Top header ── */
.topbar {
    background: linear-gradient(135deg, #1a3a6e 0%, #1e4db7 60%, #2563eb 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 32px rgba(30, 77, 183, 0.25);
}

.topbar-title {
    font-size: 26px;
    font-weight: 700;
    color: white;
    letter-spacing: -0.5px;
}

.topbar-sub {
    font-size: 13px;
    color: rgba(255,255,255,0.65);
    margin-top: 4px;
    font-weight: 400;
}

.topbar-badge {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    color: white;
    font-size: 12px;
    font-weight: 500;
    padding: 6px 14px;
    border-radius: 99px;
    font-family: 'DM Mono', monospace;
}

/* ── Metric cards ── */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 28px;
}

.metric-card {
    background: white;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border-top: 3px solid transparent;
}

.metric-card.total  { border-top-color: #1e4db7; }
.metric-card.bug    { border-top-color: #ef4444; }
.metric-card.feature{ border-top-color: #3b82f6; }
.metric-card.praise { border-top-color: #22c55e; }
.metric-card.other  { border-top-color: #f59e0b; }

.metric-label {
    font-size: 11px;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 30px;
    font-weight: 700;
    color: #0f172a;
    line-height: 1;
}

.metric-sub {
    font-size: 11px;
    color: #94a3b8;
    margin-top: 4px;
}

/* ── Filter bar ── */
.filter-label {
    font-size: 12px;
    font-weight: 600;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}

/* ── Kanban board ── */
.kanban-board {
    display: grid;
    gap: 16px;
}

.kanban-col-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}

.kanban-col-title {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

.kanban-count {
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 99px;
}

/* ── Ticket card ── */
.ticket-card {
    background: white;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    border-left: 4px solid transparent;
    transition: box-shadow 0.2s;
    position: relative;
}

.ticket-card:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.ticket-card.Bug            { border-left-color: #ef4444; }
.ticket-card.Feature\ Request { border-left-color: #3b82f6; }
.ticket-card.Praise         { border-left-color: #22c55e; }
.ticket-card.Complaint      { border-left-color: #f59e0b; }
.ticket-card.Spam           { border-left-color: #94a3b8; }

.ticket-id {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #94a3b8;
    margin-bottom: 6px;
}

.ticket-title {
    font-size: 13px;
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 10px;
    line-height: 1.4;
}

.ticket-meta {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    align-items: center;
}

.badge {
    font-size: 10px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

.badge-bug       { background: #fee2e2; color: #b91c1c; }
.badge-feature   { background: #dbeafe; color: #1d4ed8; }
.badge-praise    { background: #dcfce7; color: #15803d; }
.badge-complaint { background: #fef3c7; color: #b45309; }
.badge-spam      { background: #f1f5f9; color: #64748b; }

.badge-critical  { background: #fef2f2; color: #dc2626; }
.badge-high      { background: #fff7ed; color: #c2410c; }
.badge-medium    { background: #fefce8; color: #a16207; }
.badge-low       { background: #f0fdf4; color: #166534; }

.badge-pass      { background: #dcfce7; color: #15803d; }
.badge-review    { background: #fef3c7; color: #b45309; }

.ticket-details {
    font-size: 11px;
    color: #64748b;
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid #f1f5f9;
    font-family: 'DM Mono', monospace;
    line-height: 1.5;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-title { font-size: 18px; font-weight: 600; color: #0f172a; margin-bottom: 8px; }
.empty-sub { font-size: 14px; color: #94a3b8; }

/* ── Section header ── */
.section-header {
    font-size: 15px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Streamlit button override ── */
.stButton > button {
    background: linear-gradient(135deg, #1e4db7, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 28px !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    transform: translateY(-1px) !important;
}

.stSelectbox > div > div {
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────
def load_tickets():
    path = "output/generated_tickets.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        if "solved" not in df.columns:
            df["solved"] = False
        return df
    return None

def load_log():
    path = "output/processing_log.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

def category_badge(cat):
    cat = str(cat)
    cls = cat.lower().replace(" ", "")
    map_ = {
        "bug": "bug", "featurerequest": "feature",
        "praise": "praise", "complaint": "complaint", "spam": "spam"
    }
    css = map_.get(cls, "spam")
    return f'<span class="badge badge-{css}">{cat}</span>'

def priority_badge(pri):
    pri = str(pri) if pd.notna(pri) else "Low"
    css = pri.lower() if pri.lower() in ["critical","high","medium","low"] else "low"
    return f'<span class="badge badge-{css}">{pri}</span>'

def status_badge(status):
    status = str(status) if pd.notna(status) else "Pass"
    css = "pass" if status == "Pass" else "review"
    return f'<span class="badge badge-{css}">{status}</span>'

def cat_color(cat):
    return {
        "Bug": "#ef4444", "Feature Request": "#3b82f6",
        "Praise": "#22c55e", "Complaint": "#f59e0b", "Spam": "#94a3b8"
    }.get(str(cat), "#94a3b8")

def cat_bg(cat):
    return {
        "Bug": "#fee2e2", "Feature Request": "#dbeafe",
        "Praise": "#dcfce7", "Complaint": "#fef3c7", "Spam": "#f1f5f9"
    }.get(str(cat), "#f1f5f9")

def cat_icon(cat):
    return {
        "Bug": "🐛", "Feature Request": "✨",
        "Praise": "💚", "Complaint": "⚠️", "Spam": "🚫"
    }.get(str(cat), "📋")


# ── Top bar ───────────────────────────────────────────────────────────────
df = load_tickets()
log_df = load_log()

total = len(df) if df is not None else 0
last_run = "Not run yet"
if df is not None and total > 0:
    last_run = "Pipeline complete"

st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">📋 FeedbackIQ</div>
        <div class="topbar-sub">Intelligent User Feedback Analysis System · {last_run}</div>
    </div>
    <div class="topbar-badge">CrewAI · Gemini 2.5 Flash</div>
</div>
""", unsafe_allow_html=True)


# ── Run pipeline ──────────────────────────────────────────────────────────
col_btn, col_status = st.columns([2, 8])
with col_btn:
    run = st.button("🔍 Analyse Feedback")

if run:
    with st.spinner("Running multi-agent pipeline..."):
        result = subprocess.run(
            ["python", "main.py"],
            capture_output=True, text=True
        )
    if result.returncode == 0:
        st.success("✅ Pipeline complete! Tickets generated successfully.")
        df = load_tickets()
        log_df = load_log()
        st.rerun()
    else:
        st.error(f"Pipeline failed: {result.stderr[-500:] if result.stderr else 'Unknown error'}")


# ── Metrics ───────────────────────────────────────────────────────────────
if df is not None and total > 0:
    bugs = len(df[df["category"] == "Bug"])
    features = len(df[df["category"] == "Feature Request"])
    praise = len(df[df["category"] == "Praise"])
    other = len(df[~df["category"].isin(["Bug","Feature Request","Praise"])])

    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-card total">
            <div class="metric-label">Total Tickets</div>
            <div class="metric-value">{total}</div>
            <div class="metric-sub">All feedback processed</div>
        </div>
        <div class="metric-card bug">
            <div class="metric-label">Bugs</div>
            <div class="metric-value">{bugs}</div>
            <div class="metric-sub">Requires engineering</div>
        </div>
        <div class="metric-card feature">
            <div class="metric-label">Feature Requests</div>
            <div class="metric-value">{features}</div>
            <div class="metric-sub">Product backlog</div>
        </div>
        <div class="metric-card praise">
            <div class="metric-label">Praise</div>
            <div class="metric-value">{praise}</div>
            <div class="metric-sub">Positive signals</div>
        </div>
        <div class="metric-card other">
            <div class="metric-label">Other</div>
            <div class="metric-value">{other}</div>
            <div class="metric-sub">Complaints & spam</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ── Tabs ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🗂️ Kanban Board", "📊 Quality Log", "✏️ Edit Tickets"])

# ── TAB 1: Kanban ─────────────────────────────────────────────────────────
with tab1:
    if df is None or total == 0:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <div class="empty-title">No tickets yet</div>
            <div class="empty-sub">Click "Analyse Feedback" to run the pipeline and generate tickets.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # merge quality scores if available
        display_df = df.copy()
        if log_df is not None and "quality_status" in log_df.columns:
            merge_cols = ["source_id", "quality_score", "quality_notes", "quality_status"]
            available = [c for c in merge_cols if c in log_df.columns]
            display_df = display_df.merge(log_df[available], on="source_id", how="left")

        # filter bar
        col_f1, col_f2, col_f3 = st.columns([3, 3, 4])
        with col_f1:
            categories = ["All"] + sorted(display_df["category"].dropna().unique().tolist())
            cat_filter = st.selectbox("Filter by category", categories)
        with col_f2:
            priorities = ["All"] + sorted(display_df["priority"].dropna().unique().tolist())
            pri_filter = st.selectbox("Filter by priority", priorities)
        with col_f3:
            show_solved = st.checkbox("Hide solved tickets", value=False)

        filtered = display_df.copy()
        if cat_filter != "All":
            filtered = filtered[filtered["category"] == cat_filter]
        if pri_filter != "All":
            filtered = filtered[filtered["priority"] == pri_filter]
        if show_solved:
            filtered = filtered[filtered["solved"] == False]

        # determine columns to show
        if cat_filter != "All":
            cols_to_show = [cat_filter]
        else:
            cols_to_show = ["Bug", "Feature Request", "Praise", "Complaint", "Spam"]

        active_cols = [c for c in cols_to_show if c in filtered["category"].values]

        if not active_cols:
            st.info("No tickets match the current filter.")
        else:
            grid_cols = st.columns(len(active_cols))

            for i, cat in enumerate(active_cols):
                cat_tickets = filtered[filtered["category"] == cat]
                color = cat_color(cat)
                bg = cat_bg(cat)
                icon = cat_icon(cat)
                count = len(cat_tickets)

                with grid_cols[i]:
                    st.markdown(f"""
                    <div class="kanban-col-header">
                        <span style="font-size:16px;">{icon}</span>
                        <span class="kanban-col-title" style="color:{color};">{cat}</span>
                        <span class="kanban-count" style="background:{bg}; color:{color};">{count}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    for _, row in cat_tickets.iterrows():
                        source_id = str(row.get("source_id",""))
                        title = str(row.get("suggested_title", "Untitled"))
                        priority = str(row.get("priority","Low")) if pd.notna(row.get("priority")) else "Low"
                        source_type = str(row.get("source_type","")).replace("_"," ").title()
                        tech = str(row.get("technical_details","")) if pd.notna(row.get("technical_details")) else ""
                        solved = bool(row.get("solved", False))
                        qs = row.get("quality_status", None)
                        qscore = row.get("quality_score", None)

                        solved_style = "opacity:0.45;" if solved else ""

                        quality_html = ""
                        if qs is not None and pd.notna(qs):
                            quality_html = f'{status_badge(qs)}'
                            if qscore is not None and pd.notna(qscore):
                                quality_html += f' <span style="font-size:10px;color:#94a3b8;">Q:{int(qscore)}/10</span>'

                        tech_html = ""
                        if tech and tech != "No technical details required" and tech != "nan":
                            tech_html = f'<div class="ticket-details">{tech}</div>'

                        st.markdown(f"""
                        <div class="ticket-card {cat}" style="{solved_style}">
                            <div class="ticket-id">{source_id} · {source_type}</div>
                            <div class="ticket-title">{"✅ " if solved else ""}{title}</div>
                            <div class="ticket-meta">
                                {priority_badge(priority)}
                                {quality_html}
                            </div>
                            {tech_html}
                        </div>
                        """, unsafe_allow_html=True)


# ── TAB 2: Quality Log ────────────────────────────────────────────────────
with tab2:
    if log_df is None:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🔍</div>
            <div class="empty-title">No quality log yet</div>
            <div class="empty-sub">Run the pipeline to generate quality reviews.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols_to_show = [c for c in [
            "source_id", "category", "suggested_title",
            "priority", "quality_score", "quality_notes", "quality_status"
        ] if c in log_df.columns]
        st.dataframe(
            log_df[cols_to_show],
            use_container_width=True,
            hide_index=True
        )


# ── TAB 3: Edit Tickets ───────────────────────────────────────────────────
with tab3:
    if df is None or total == 0:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">✏️</div>
            <div class="empty-title">No tickets to edit</div>
            <div class="empty-sub">Run the pipeline first.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("**Edit tickets below. Toggle 'solved' to mark tickets as resolved.**")

        edit_cols = [c for c in [
            "source_id", "category", "suggested_title",
            "priority", "technical_details", "solved"
        ] if c in df.columns]

        edited = st.data_editor(
            df[edit_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "solved": st.column_config.CheckboxColumn("Solved ✅"),
                "priority": st.column_config.SelectboxColumn(
                    "Priority",
                    options=["Critical", "High", "Medium", "Low"]
                ),
                "suggested_title": st.column_config.TextColumn("Title", width="large"),
                "technical_details": st.column_config.TextColumn("Technical Details", width="large"),
            }
        )

        if st.button("💾 Save changes"):
            for col in edited.columns:
                df[col] = edited[col]
            df.to_csv("output/generated_tickets.csv", index=False)
            st.success("Changes saved to generated_tickets.csv")
            st.rerun()