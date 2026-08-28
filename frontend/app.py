import requests
import pandas as pd
import plotly.express as px
import streamlit as st


API_URL = "http://127.0.0.1:8000"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Narrate IQ",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Executive"

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


# ============================================================
# API
# ============================================================

@st.cache_data(ttl=20)
def get_json(endpoint: str):

    response = requests.get(
        f"{API_URL}{endpoint}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def post_json(
    endpoint: str,
    payload: dict,
):

    response = requests.post(
        f"{API_URL}{endpoint}",
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


def refresh_data():

    st.cache_data.clear()


# ============================================================
# FORMAT
# ============================================================

def money(value):

    if value is None:
        return "—"

    return f"${float(value):,.0f}"


def pct(value):

    if value is None:
        return "—"

    return f"{float(value) * 100:.0f}%"


def signed_pct(value):

    if value is None:
        return "—"

    return f"{float(value):+.2f}%"


def signed_number(value):

    if value is None:
        return "—"

    return f"{float(value):+,.0f}"


# ============================================================
# PREMIUM DARK THEME
# ============================================================

st.markdown(
    """
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 80% 0%,
            rgba(42, 84, 160, 0.12),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #080b11 0%,
            #0c1017 100%
        );

    color: #f5f7fa;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #090c12;
    border-right: 1px solid #1d2430;
}

section[data-testid="stSidebar"] * {
    color: #dce3ec;
}

/* Main content */

.block-container {
    max-width: 1500px;
    padding-top: 1.6rem;
    padding-bottom: 4rem;
}

/* Typography */

h1, h2, h3 {
    color: #f8fafc !important;
    letter-spacing: -0.03em;
}

p, label {
    color: #aab4c2;
}

/* Cards */

.niq-card {
    background:
        linear-gradient(
            145deg,
            rgba(22, 28, 38, 0.95),
            rgba(15, 20, 28, 0.95)
        );

    border:
        1px solid #202936;

    border-radius: 18px;

    padding: 22px;

    box-shadow:
        0 10px 35px rgba(0, 0, 0, 0.28);

    margin-bottom: 16px;
}

.niq-card:hover {
    border-color: #354154;
}

/* KPI */

.kpi-label {
    color: #7f8b9c;
    font-size: 0.76rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.kpi-value {
    color: #f8fafc;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 8px;
}

.kpi-change-down {
    color: #ff6b6b;
    font-size: 0.85rem;
    font-weight: 600;
    margin-top: 4px;
}

.kpi-change-up {
    color: #35d49a;
    font-size: 0.85rem;
    font-weight: 600;
    margin-top: 4px;
}

/* Hero */

.hero {
    background:
        linear-gradient(
            135deg,
            rgba(127, 29, 29, 0.24),
            rgba(22, 28, 38, 0.96)
        );

    border: 1px solid #3b2b32;

    border-radius: 22px;

    padding: 30px;

    margin-bottom: 20px;
}

.hero-eyebrow {
    color: #98a3b3;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
}

.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-top: 8px;
    color: #ffffff;
}

.hero-subtitle {
    color: #aeb8c5;
    margin-top: 8px;
    font-size: 1rem;
}

/* Tags */

.tag {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 999px;
    background: #1b2430;
    color: #dce4ed;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
}

/* Section label */

.section-label {
    color: #7f8b9c;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 10px;
}

/* Evidence */

.evidence-line {
    padding: 12px 0;
    border-bottom: 1px solid #202936;
}

.evidence-line:last-child {
    border-bottom: none;
}

/* Impact */

.impact-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 11px 0;
    border-bottom: 1px solid #202936;
}

.impact-name {
    color: #e8edf3;
    font-weight: 600;
}

.impact-value {
    color: #ff7474;
    font-weight: 700;
}

/* Action */

.action-box {
    background:
        linear-gradient(
            135deg,
            rgba(17, 94, 89, 0.24),
            rgba(15, 20, 28, 0.96)
        );

    border: 1px solid #214844;
    border-radius: 18px;
    padding: 22px;
}

/* Buttons */

.stButton > button {
    border-radius: 10px;
    border: 1px solid #2b3544;
    background: #151b24;
    color: #f5f7fa;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #53647c;
    color: white;
}

/* Inputs */

.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    background: #111721 !important;
    color: #f5f7fa !important;
    border-color: #2a3442 !important;
}

/* Dataframe */

[data-testid="stDataFrame"] {
    border: 1px solid #202936;
    border-radius: 12px;
}

/* Divider */

hr {
    border-color: #202936;
}

/* Chat */

[data-testid="stChatMessage"] {
    background: #111720;
    border: 1px solid #202936;
    border-radius: 16px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:1.4rem;
        font-weight:800;
        letter-spacing:-0.04em;
        margin-bottom:4px;
    ">
        ◉ NARRATE IQ
    </div>

    <div style="
        color:#718096;
        font-size:0.75rem;
        margin-bottom:22px;
    ">
        BUSINESS INTELLIGENCE TERMINAL
    </div>
    """,
    unsafe_allow_html=True,
)


pages = {
    "Executive": "Executive",
    "Root Cause": "Root Cause",
    "Experiments": "Experiments",
    "Learning": "Learning",
    "Data": "Data",
    "Chat": "AI Copilot",
}


st.session_state.page = st.sidebar.radio(
    "NAVIGATION",
    list(pages.keys()),
    index=list(pages.keys()).index(
        st.session_state.page
    ),
)


st.sidebar.divider()


if st.sidebar.button(
    "↻ Refresh",
    use_container_width=True,
):

    refresh_data()
    st.rerun()


st.sidebar.markdown(
    """
    <div style="
        margin-top:24px;
        color:#667085;
        font-size:0.72rem;
        line-height:1.6;
    ">
        Intelligence Engine<br>
        Evidence Graph<br>
        Experiment Loop<br>
        Historical Learning<br>
        Groq Copilot
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# EXECUTIVE
# ============================================================

if st.session_state.page == "Executive":

    try:

        decision = get_json(
            "/decision"
        )

    except requests.RequestException as exc:

        st.error(
            "Unable to load Narrate IQ decision."
        )

        st.code(str(exc))
        st.stop()

    kpi = decision["kpi"]

    hypothesis = decision[
        "leading_hypothesis"
    ]

    validation = decision[
        "validation"
    ]

    recommendation = decision.get(
        "recommendation"
    )

    experiment = decision.get(
        "experiment"
    )

    learning = decision.get(
        "historical_learning"
    )

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:end;
            margin-bottom:20px;
        ">
            <div>
                <div style="
                    color:#708096;
                    font-size:0.72rem;
                    font-weight:700;
                    letter-spacing:0.15em;
                    text-transform:uppercase;
                ">
                    EXECUTIVE INTELLIGENCE
                </div>

                <h1 style="
                    margin:4px 0 0 0;
                    font-size:2.4rem;
                ">
                    Business Situation
                </h1>
            </div>

            <div style="
                color:#758297;
                font-size:0.8rem;
            ">
                {decision["date"]} · LIVE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Hero
    # --------------------------------------------------------

    change = float(
        kpi["revenue_change_pct"]
    )

    st.markdown(
        f"""
        <div class="hero">

            <div class="hero-eyebrow">
                {"Revenue deterioration" if change < 0 else "Revenue movement"}
            </div>

            <div class="hero-title">
                {"Revenue is under pressure" if change < 0 else "Revenue has moved"}
            </div>

            <div class="hero-subtitle">
                Revenue changed
                <strong>{change:.2f}%</strong>
                week-over-week to
                <strong>{money(kpi["revenue"])}</strong>.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # KPI row
    # --------------------------------------------------------

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"""
            <div class="niq-card">
                <div class="kpi-label">Revenue</div>
                <div class="kpi-value">
                    {money(kpi["revenue"])}
                </div>
                <div class="kpi-change-down">
                    {change:+.2f}% WoW
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
            <div class="niq-card">
                <div class="kpi-label">Units Sold</div>
                <div class="kpi-value">
                    {float(kpi["units_sold"]):,.0f}
                </div>
                <div class="muted">
                    Current period
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            f"""
            <div class="niq-card">
                <div class="kpi-label">Confidence</div>
                <div class="kpi-value">
                    {pct(hypothesis["confidence_score"])}
                </div>
                <div class="muted">
                    {hypothesis["confidence"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k4:
        st.markdown(
            f"""
            <div class="niq-card">
                <div class="kpi-label">Evidence Strength</div>
                <div class="kpi-value">
                    {pct(validation["validation_score"])}
                </div>
                <div class="muted">
                    Validated signal
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # Leading hypothesis
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">01 · WHY</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(
        [3, 1]
    )

    with c1:

        st.markdown(
            f"""
            <div class="niq-card">

                <div class="kpi-label">
                    LEADING HYPOTHESIS
                </div>

                <div style="
                    font-size:2rem;
                    font-weight:800;
                    margin-top:8px;
                ">
                    {hypothesis["name"]}
                </div>

                <div style="
                    margin-top:10px;
                    color:#99a5b4;
                ">
                    Status:
                    <strong>
                        {hypothesis["status"]}
                    </strong>
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:

        st.markdown(
            f"""
            <div class="niq-card">

                <div class="kpi-label">
                    RANK
                </div>

                <div style="
                    font-size:2.5rem;
                    font-weight:800;
                    margin-top:6px;
                ">
                    #{hypothesis["rank"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # Evidence cards
    # --------------------------------------------------------

    e1, e2, e3, e4 = st.columns(4)

    evidence_items = [
        (
            e1,
            "Validation",
            validation["validation_score"],
        ),
        (
            e2,
            "Statistical",
            validation["statistical_score"],
        ),
        (
            e3,
            "Segment",
            validation["segment_evidence_score"],
        ),
        (
            e4,
            "Business Context",
            validation["event_context_score"],
        ),
    ]

    for col, label, value in evidence_items:

        with col:

            st.markdown(
                f"""
                <div class="niq-card">

                    <div class="kpi-label">
                        {label}
                    </div>

                    <div class="kpi-value">
                        {pct(value)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        f"""
        <div class="niq-card">

            <div class="kpi-label">
                SUPPORTING EVIDENCE
            </div>

            <div style="
                font-size:1rem;
                line-height:1.75;
                margin-top:10px;
                color:#d8dee7;
            ">
                {validation["supporting_evidence"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Impact
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">02 · WHERE</div>',
        unsafe_allow_html=True,
    )

    segments = decision.get(
        "top_segments",
        [],
    )

    if segments:

        impact_col, detail_col = st.columns(
            [1.2, 2]
        )

        with impact_col:

            st.markdown(
                '<div class="niq-card">',
                unsafe_allow_html=True,
            )

            st.markdown(
                "### Biggest Contributors"
            )

            for segment in segments[:5]:

                st.markdown(
                    f"""
                    <div class="impact-row">

                        <div>
                            <div class="impact-name">
                                {segment["value"]}
                            </div>

                            <div class="muted">
                                {segment["dimension"]}
                            </div>
                        </div>

                        <div class="impact-value">
                            {signed_number(segment["unit_change"])}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )

        with detail_col:

            chart_data = pd.DataFrame(
                [
                    {
                        "Segment": str(
                            row["value"]
                        ),
                        "Unit Change": float(
                            row["unit_change"]
                        ),
                    }
                    for row in segments[:10]
                ]
            )

            if not chart_data.empty:

                fig = px.bar(
                    chart_data,
                    x="Unit Change",
                    y="Segment",
                    orientation="h",
                )

                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#dce3ec",
                    margin=dict(
                        l=10,
                        r=10,
                        t=10,
                        b=10,
                    ),
                    height=320,
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

    # --------------------------------------------------------
    # Action
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">03 · WHAT NOW</div>',
        unsafe_allow_html=True,
    )

    if recommendation:

        priority = str(
            recommendation["priority"]
        ).upper()

        st.markdown(
            f"""
            <div class="action-box">

                <div class="kpi-label">
                    RECOMMENDED ACTION
                </div>

                <div style="
                    margin-top:10px;
                    margin-bottom:12px;
                ">
                    <span class="tag">
                        {priority} PRIORITY
                    </span>
                </div>

                <div style="
                    color:#e7edf5;
                    font-size:1.1rem;
                    line-height:1.7;
                ">
                    {recommendation["action"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # Experiment
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">04 · DID IT WORK</div>',
        unsafe_allow_html=True,
    )

    if experiment:

        ex1, ex2, ex3, ex4 = st.columns(4)

        with ex1:
            st.metric(
                "Status",
                experiment["status"].upper(),
            )

        with ex2:
            st.metric(
                "Target",
                experiment["target_metric"],
            )

        with ex3:

            measured = experiment.get(
                "measured_change_pct"
            )

            st.metric(
                "Measured",
                (
                    f"{measured:.2f}%"
                    if measured is not None
                    else "—"
                ),
            )

        with ex4:

            outcome = experiment.get(
                "outcome"
            )

            st.metric(
                "Outcome",
                (
                    outcome.upper()
                    if outcome
                    else "—"
                ),
            )

    # --------------------------------------------------------
    # Learning
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">05 · WHAT DID WE LEARN</div>',
        unsafe_allow_html=True,
    )

    if learning:

        l1, l2, l3, l4 = st.columns(4)

        with l1:
            st.metric(
                "Reliability",
                pct(
                    learning[
                        "historical_reliability"
                    ]
                ),
            )

        with l2:
            st.metric(
                "Attempts",
                learning["attempts"],
            )

        with l3:
            st.metric(
                "Successes",
                learning["successes"],
            )

        with l4:
            st.metric(
                "Partials",
                learning["partials"],
            )

    else:

        st.info(
            "No historical learning yet."
        )


# ============================================================
# ROOT CAUSE
# ============================================================

elif st.session_state.page == "Root Cause":

    st.header(
        "🔎 Root Cause"
    )

    try:

        data = get_json(
            "/root-cause"
        )

    except requests.RequestException as exc:

        st.error(str(exc))
        st.stop()

    graph = data.get(
        "graph",
        [],
    )

    hypotheses = [
        row
        for row in graph
        if row.get("node_type")
        == "hypothesis"
    ]

    segments = [
        row
        for row in graph
        if row.get("node_type")
        == "segment"
    ]

    st.markdown(
        "### Hypothesis Ranking"
    )

    st.dataframe(
        [
            {
                "Rank": int(
                    row["rank"]
                ),
                "Hypothesis": row["node"],
                "Confidence": pct(
                    row["confidence_score"]
                ),
                "Validation": pct(
                    row["validation_score"]
                ),
                "Status": row["status"],
            }
            for row in hypotheses
        ],
        use_container_width=True,
        hide_index=True,
    )

    if segments:

        st.markdown(
            "### Contribution Explorer"
        )

        dimensions = sorted(
            {
                row["dimension"]
                for row in segments
            }
        )

        dimension = st.selectbox(
            "Dimension",
            dimensions,
        )

        filtered = [
            row
            for row in segments
            if row["dimension"]
            == dimension
        ]

        filtered = sorted(
            filtered,
            key=lambda row: row[
                "unit_change"
            ],
        )

        df = pd.DataFrame(
            [
                {
                    "Segment": row[
                        "dimension_value"
                    ],
                    "Unit Change": float(
                        row["unit_change"]
                    ),
                }
                for row in filtered
            ]
        )

        if not df.empty:

            fig = px.bar(
                df,
                x="Unit Change",
                y="Segment",
                orientation="h",
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=420,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        st.dataframe(
            [
                {
                    "Segment": row[
                        "dimension_value"
                    ],
                    "Unit Change": row[
                        "unit_change"
                    ],
                    "Change %": row[
                        "unit_change_pct"
                    ],
                    "Contribution %": row[
                        "contribution_share_pct"
                    ],
                }
                for row in filtered
            ],
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# EXPERIMENTS
# ============================================================

elif st.session_state.page == "Experiments":

    st.header(
        "🧪 Experiments"
    )

    try:

        experiments = get_json(
            "/experiments"
        )

    except requests.RequestException as exc:

        st.error(str(exc))
        st.stop()

    for exp in experiments:

        with st.container():

            st.markdown(
                f"""
                <div class="niq-card">

                    <div class="kpi-label">
                        EXPERIMENT
                    </div>

                    <h2>
                        {exp["hypothesis"]}
                    </h2>

                </div>
                """,
                unsafe_allow_html=True,
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Status",
                    exp["status"].upper(),
                )

            with c2:

                st.metric(
                    "Confidence",
                    f"{exp['confidence_score']:.0%}",
                )

            with c3:

                st.metric(
                    "Threshold",
                    f"{exp['success_threshold_pct']:.1f}%",
                )

            st.write(
                exp["action"]
            )

            if exp["status"] == "proposed":

                baseline = st.number_input(
                    "Baseline",
                    min_value=0.000001,
                    value=1.0,
                    step=1.0,
                    key=(
                        f"baseline_"
                        f"{exp['experiment_id']}"
                    ),
                )

                if st.button(
                    "▶ Start",
                    key=(
                        f"start_"
                        f"{exp['experiment_id']}"
                    ),
                    type="primary",
                ):

                    try:

                        post_json(
                            (
                                f"/experiments/"
                                f"{exp['experiment_id']}"
                                "/start"
                            ),
                            {
                                "baseline_value": baseline
                            },
                        )

                        refresh_data()
                        st.rerun()

                    except requests.RequestException as exc:

                        st.error(
                            str(exc)
                        )

            elif exp["status"] == "running":

                baseline = exp.get(
                    "baseline_value"
                )

                observed = st.number_input(
                    "Observed value",
                    min_value=0.000001,
                    value=float(
                        baseline
                        if baseline is not None
                        else 1.0
                    ),
                    step=1.0,
                    key=(
                        f"observed_"
                        f"{exp['experiment_id']}"
                    ),
                )

                if st.button(
                    "✅ Record Outcome",
                    key=(
                        f"complete_"
                        f"{exp['experiment_id']}"
                    ),
                    type="primary",
                ):

                    try:

                        post_json(
                            (
                                f"/experiments/"
                                f"{exp['experiment_id']}"
                                "/outcome"
                            ),
                            {
                                "observed_value": observed
                            },
                        )

                        refresh_data()
                        st.rerun()

                    except requests.RequestException as exc:

                        st.error(
                            str(exc)
                        )

            elif exp["status"] == "completed":

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric(
                        "Baseline",
                        exp[
                            "baseline_value"
                        ],
                    )

                with c2:
                    st.metric(
                        "Observed",
                        exp[
                            "observed_value"
                        ],
                    )

                with c3:

                    value = exp.get(
                        "measured_change_pct"
                    )

                    st.metric(
                        "Change",
                        (
                            f"{value:.2f}%"
                            if value is not None
                            else "—"
                        ),
                    )

                outcome = exp.get(
                    "outcome"
                )

                if outcome == "success":

                    st.success(
                        "SUCCESS"
                    )

                elif outcome == "partial":

                    st.warning(
                        "PARTIAL"
                    )

                else:

                    st.error(
                        "FAILED"
                    )


# ============================================================
# LEARNING
# ============================================================

elif st.session_state.page == "Learning":

    st.header(
        "📈 Learning"
    )

    try:

        data = get_json(
            "/learning"
        )

    except requests.RequestException as exc:

        st.error(str(exc))
        st.stop()

    summary = data.get(
        "summary",
        [],
    )

    history = data.get(
        "history",
        [],
    )

    if summary:

        st.subheader(
            "Hypothesis Reliability"
        )

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    if history:

        st.subheader(
            "Experiment History"
        )

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# DATA
# ============================================================

elif st.session_state.page == "Data":

    st.header(
        "📥 Data"
    )

    st.caption(
        "Manage the active business datasets used by Narrate IQ."
    )

    files = {
        "Sales": "sales.csv",
        "Inventory": "inventory.csv",
        "Marketing": "marketing.csv",
        "Events": "business_events.csv",
    }

    ready = {}

    for name, filename in files.items():

        ready[name] = (
            Path("data/raw")
            / filename
        ).exists()

    c1, c2, c3, c4 = st.columns(4)

    for col, (name, exists) in zip(
        [c1, c2, c3, c4],
        ready.items(),
    ):

        with col:

            st.markdown(
                f"""
                <div class="niq-card">

                    <div class="kpi-label">
                        {name}
                    </div>

                    <div style="
                        font-size:1.15rem;
                        font-weight:700;
                        margin-top:8px;
                    ">
                        {"● READY" if exists else "○ OPTIONAL"}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    st.info(
        "Use the existing upload/mapping flow to replace datasets."
    )

    st.markdown(
        """
        ### Recommended workflow

        **1. Upload**

        **2. Map columns**

        **3. Validate**

        **4. Save**

        **5. Run Narrate IQ Analysis**
        """
    )

    if st.button(
        "🚀 Run Narrate IQ Analysis",
        type="primary",
        use_container_width=True,
    ):

        sales_exists = (
            Path("data/raw/sales.csv")
            .exists()
        )

        if not sales_exists:

            st.error(
                "Sales data is required."
            )

        else:

            with st.spinner(
                "Running intelligence pipeline..."
            ):

                logs = []
                success = True

                modules = [
                    "src.kpi.engine",
                    "src.anomaly.engine",
                    "src.drivers.engine",
                    "src.attribution.engine",
                    "src.confidence.engine",
                    "src.drilldown.sales",
                    "src.context.events",
                    "src.evidence.validator",
                    "src.learning.history",
                    "src.learning.engine",
                    "src.hypotheses.engine",
                    "src.recommendations.engine",
                    "src.rootcause.engine",
                    "src.experiments.engine",
                    "src.decision.engine",
                    "src.llm.narrative",
                ]

                import subprocess
                import sys

                for module in modules:

                    process = subprocess.run(
                        [
                            sys.executable,
                            "-m",
                            module,
                        ],
                        capture_output=True,
                        text=True,
                    )

                    logs.append(
                        process.stdout
                        + process.stderr
                    )

                    if process.returncode != 0:

                        success = False
                        break

            if success:

                refresh_data()

                st.session_state.page = (
                    "Executive"
                )

                st.rerun()

            else:

                st.error(
                    "Pipeline failed."
                )

                with st.expander(
                    "Pipeline logs"
                ):

                    st.code(
                        "\n".join(
                            logs
                        )
                    )


# ============================================================
# AI COPILOT
# ============================================================

elif st.session_state.page == "Chat":

    st.header(
        "◉ AI Copilot"
    )

    st.caption(
        "Ask questions about the current Narrate IQ intelligence."
    )

    if st.button(
        "Clear conversation"
    ):

        st.session_state.chat_messages = []

        st.rerun()

    st.divider()

    # Suggested questions

    s1, s2, s3 = st.columns(3)

    selected = None

    with s1:

        if st.button(
            "Why did revenue decline?",
            use_container_width=True,
        ):

            selected = (
                "Why did revenue decline?"
            )

    with s2:

        if st.button(
            "Why not marketing?",
            use_container_width=True,
        ):

            selected = (
                "Why not marketing?"
            )

    with s3:

        if st.button(
            "Did the experiment work?",
            use_container_width=True,
        ):

            selected = (
                "Did the experiment work?"
            )

    if selected:

        history = (
            st.session_state
            .chat_messages
        )

        payload = [
            {
                "role": message["role"],
                "content": message["content"],
            }
            for message in history
        ]

        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": selected,
            }
        )

        try:

            result = post_json(
                "/chat",
                {
                    "question": selected,
                    "conversation": payload,
                },
            )

            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": result["answer"],
                }
            )

        except requests.RequestException as exc:

            st.error(
                str(exc)
            )

        st.rerun()

    for message in (
        st.session_state.chat_messages
    ):

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    question = st.chat_input(
        "Ask Narrate IQ anything about the current analysis..."
    )

    if question:

        history = (
            st.session_state
            .chat_messages
        )

        payload = [
            {
                "role": message["role"],
                "content": message["content"],
            }
            for message in history
        ]

        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Analyzing evidence..."
            ):

                try:

                    result = post_json(
                        "/chat",
                        {
                            "question": question,
                            "conversation": payload,
                        },
                    )

                    answer = result[
                        "answer"
                    ]

                    st.markdown(
                        answer
                    )

                    st.session_state.chat_messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                        }
                    )

                except requests.RequestException as exc:

                    st.error(
                        str(exc)
                    )