import streamlit as st
import pandas as pd
from datetime import date, datetime

st.set_page_config(
    page_title="VANGUARD-Guard | Enterprise AI Playbook",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from governance_store import CATEGORIES, DB_PATH, delete_tool, load_all, save, status, valid_raci

# Load persistent records once for this browser session. All writes go to SQLite.
if "gov_loaded" not in st.session_state:
    snapshot = load_all()
    st.session_state.tools = snapshot["tools"]
    st.session_state.risks = snapshot["risks"]
    st.session_state.raci = snapshot["raci"]
    st.session_state.gov_loaded = True

RISK_CATEGORIES = list(CATEGORIES)


def get_next_id():
    nums = [int(t["id"].split("-")[1]) for t in st.session_state.tools]
    return f"AI-{max(nums, default=0) + 1:03d}"


def tool_status(tool_id):
    return status([r for r in st.session_state.risks if r["tool_id"] == tool_id])


def calculate_overall_risk(tool_id):
    return tool_status(tool_id)[1]

# ---------- Sidebar ----------
st.sidebar.title("VANGUARD-Guard")
st.sidebar.markdown("**Cross-Functional Enterprise AI Playbook**")
st.sidebar.caption("Register tools. Review risks. Assign owners. Preserve human authority.")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "➕ Add a Tool", "📋 My Tools", "⚠️ Assess Risks", "👥 Assign Owners", "📊 Summary"]
)

# ---------- HOME ----------
if page == "🏠 Home":
    st.title("VANGUARD-Guard")
    st.markdown("""
    This workbench helps HR, technology, risk and business leaders **understand and review AI tools** used in the organization.
    
    You don't need to be a technical expert. We'll guide you step by step. Records are stored locally; this prototype does not authorize deployment or perform live model monitoring.
    """)
    
    st.info("**What is AI governance?**  \nIt means knowing which AI tools are being used, what risks they create, and who is responsible for them.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tools registered", len(st.session_state.tools))
    with col2:
        complete = sum(1 for t in st.session_state.tools if tool_status(t["id"])[0] == "Complete")
        st.metric("Fully assessed", complete)
    with col3:
        high = sum(1 for t in st.session_state.tools if tool_status(t["id"])[2])
        st.metric("High-risk tools", high)
    
    st.markdown("---")
    st.subheader("How to use this tool")
    st.markdown("""
    1. **Add a Tool** — Tell us about an AI tool your team uses (or is considering).
    2. **Assess Risks** — Answer simple questions about possible problems.
    3. **Assign Owners** — Decide who is responsible.
    4. **Review Summary** — See an overview of all tools.
    """)
    
    st.success("Start by adding your first tool →")

# ---------- ADD A TOOL ----------
elif page == "➕ Add a Tool":
    st.title("Add an AI Tool")
    st.markdown("Tell us about an AI tool used by HR or the broader organization.")
    
    with st.form("add_tool"):
        tool_name = st.text_input("Tool name*", placeholder="e.g. ChatGPT, Resume Screener, Workday AI")
        vendor = st.text_input("Who makes it?", placeholder="e.g. OpenAI, Workday, Microsoft")
        purpose = st.text_area("What is it used for?", placeholder="e.g. Screening resumes, writing job descriptions, answering employee questions")
        data_inputs = st.text_area("What information does it see?", placeholder="e.g. Resumes, employee names, performance reviews")
        classification = st.selectbox("How sensitive is the information?", 
            ["Public", "Internal", "Confidential", "Restricted (personal or highly sensitive)"])
        users = st.text_input("Who uses it?", placeholder="e.g. Recruiting team, All employees")
        owner = st.text_input("Named owner (person responsible)*", placeholder="e.g. Sarah Chen, HR Director")
        initial_risk = st.selectbox("How risky does this feel right now?", ["LOW", "MEDIUM", "HIGH"],
            help="LOW = advisory only, human decides. MEDIUM = internal use with review. HIGH = decisions about people or customer-facing.")
        
        submitted = st.form_submit_button("Add Tool", type="primary")
        
        if submitted:
            if not tool_name or not owner:
                st.error("Please fill in Tool name and Named owner.")
            else:
                new_tool = {
                    "id": get_next_id(),
                    "name": tool_name,
                    "vendor": vendor,
                    "purpose": purpose,
                    "data_inputs": data_inputs,
                    "classification": classification,
                    "users": users,
                    "owner": owner,
                    "initial_risk": initial_risk,
                    "date_added": date.today().isoformat()
                }
                st.session_state.tools.append(new_tool)
                save("tools", new_tool["id"], new_tool)
                st.success(f"Added **{tool_name}** (ID: {new_tool['id']})")
                st.balloons()

# ---------- MY TOOLS ----------
elif page == "📋 My Tools":
    st.title("My Tools")
    if not st.session_state.tools:
        st.info("No tools added yet. Go to **Add a Tool** to get started.")
    else:
        for t in st.session_state.tools:
            overall = calculate_overall_risk(t["id"])
            high_flag = tool_status(t["id"])[2]
            color = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟢", "Incomplete": "⚪"}.get(overall, "⚪")
            with st.expander(f"{'🔴' if high_flag else color} {t['name']}  ({t['id']}) — Risk: {overall}{' · HIGH flag' if high_flag and overall == 'Incomplete' else ''}"):
                st.write(f"**Purpose:** {t['purpose']}")
                st.write(f"**Owner:** {t['owner']}")
                st.write(f"**Data sensitivity:** {t['classification']}")
                st.write(f"**Initial feeling:** {t['initial_risk']}")
                if st.button(f"Remove {t['name']}", key=f"del_{t['id']}"):
                    st.session_state.tools = [x for x in st.session_state.tools if x["id"] != t["id"]]
                    st.session_state.risks = [r for r in st.session_state.risks if r["tool_id"] != t["id"]]
                    st.session_state.raci = [r for r in st.session_state.raci if r["tool_id"] != t["id"]]
                    delete_tool(t["id"])
                    st.rerun()

# ---------- ASSESS RISKS ----------
elif page == "⚠️ Assess Risks":
    st.title("Assess Risks")
    st.markdown("For each tool, answer a few simple questions. This helps decide how carefully the tool should be managed.")
    st.info("**How saving works:** You can save an unfinished assessment as a **draft**. To mark it **Complete**, fill in a risk level, explanation, mitigation, and named risk owner for **all seven categories**. A HIGH risk is flagged immediately, even in a draft. MEDIUM is the starting selection, **not an automatic risk judgment**.")
    
    if not st.session_state.tools:
        st.info("Add a tool first.")
    else:
        tool_options = {f"{t['name']} ({t['id']})": t["id"] for t in st.session_state.tools}
        selected_label = st.selectbox("Choose a tool to assess", list(tool_options.keys()))
        tool_id = tool_options[selected_label]
        tool = next(t for t in st.session_state.tools if t["id"] == tool_id)
        
        st.subheader(f"Assessing: {tool['name']}")
        
        existing = {r["category"]: r for r in st.session_state.risks if r["tool_id"] == tool_id}
        if st.session_state.get("last_saved_assessment") == tool_id:
            state = tool_status(tool_id)[0]
            if state == "Complete":
                st.success("Assessment saved — all seven categories complete.")
            else:
                st.warning("Draft saved. Complete the explanation, mitigation, and risk owner for each category to finalize.")
            st.session_state.last_saved_assessment = None
        
        with st.form(f"risk_{tool_id}"):
            for cat in RISK_CATEGORIES:
                st.markdown(f"### {cat}")
                if cat == "Accuracy":
                    st.caption("Could wrong answers cause problems for candidates, employees, or the business?")
                elif cat == "Privacy":
                    st.caption("Does this tool see personal or sensitive information?")
                elif cat == "Bias":
                    st.caption("Could this tool treat some people unfairly?")
                elif cat == "Security":
                    st.caption("Is the tool protected so only the right people can use it?")
                elif cat == "Legal":
                    st.caption("Are there laws or rules that apply (hiring, privacy, etc.)?")
                elif cat == "Dependency":
                    st.caption("What happens if this tool stops working?")
                elif cat == "Reputation":
                    st.caption("Could problems with this tool hurt the company's reputation?")
                
                score = st.selectbox(f"Risk level for {cat}", ["LOW", "MEDIUM", "HIGH"], 
                    index=["LOW", "MEDIUM", "HIGH"].index(existing.get(cat, {}).get("score", "MEDIUM")),
                    key=f"score_{tool_id}_{cat}")
                rationale = st.text_area(f"Why? (short note)", value=existing.get(cat, {}).get("rationale", ""),
                    key=f"rat_{tool_id}_{cat}", height=60)
                mitigation = st.text_input(f"What can we do to reduce the risk?", 
                    value=existing.get(cat, {}).get("mitigation", ""),
                    key=f"mit_{tool_id}_{cat}")
                risk_owner = st.text_input(f"Who owns this risk?", value=existing.get(cat, {}).get("owner", ""),
                    key=f"owner_{tool_id}_{cat}", placeholder="Name of person")
                st.divider()
            
            st.caption("You can save now and finish later. Saving a draft does not approve the tool.")
            if st.form_submit_button("Save Assessment / Save Draft", type="primary"):
                # Remove old
                st.session_state.risks = [r for r in st.session_state.risks if r["tool_id"] != tool_id]
                for cat in RISK_CATEGORIES:
                    st.session_state.risks.append({
                        "tool_id": tool_id,
                        "category": cat,
                        "score": st.session_state[f"score_{tool_id}_{cat}"],
                        "rationale": st.session_state[f"rat_{tool_id}_{cat}"],
                        "mitigation": st.session_state[f"mit_{tool_id}_{cat}"],
                        "owner": st.session_state[f"owner_{tool_id}_{cat}"],
                        "date": date.today().isoformat()
                    })
                    save("risks", f"{tool_id}::{cat}", st.session_state.risks[-1])
                st.session_state.last_saved_assessment = tool_id
                st.rerun()
        
        overall = calculate_overall_risk(tool_id)
        st.metric("Overall Risk", overall)
        if tool_status(tool_id)[2] and overall == "Incomplete":
            st.error("HIGH risk identified in a draft assessment — review it now.")

# ---------- ASSIGN OWNERS (RACI) ----------
elif page == "👥 Assign Owners":
    st.title("Assign Owners")
    st.markdown("Decide who is responsible for each tool. This makes accountability clear.")
    
    if not st.session_state.tools:
        st.info("Add a tool first.")
    else:
        tool_options = {f"{t['name']} ({t['id']})": t["id"] for t in st.session_state.tools}
        selected_label = st.selectbox("Choose a tool", list(tool_options.keys()))
        tool_id = tool_options[selected_label]
        
        existing = next((r for r in st.session_state.raci if r["tool_id"] == tool_id), {})
        
        with st.form(f"raci_{tool_id}"):
            st.markdown("**Who is accountable?** (owns the outcome — usually one person)")
            accountable = st.text_input("Accountable person*", value=existing.get("accountable", ""),
                placeholder="e.g. Sarah Chen, HR Director")
            
            st.markdown("**Who does the work?** (at least one person)")
            responsible = st.text_input("Responsible person(s)", value=existing.get("responsible", ""),
                placeholder="e.g. Recruiting Manager")
            
            st.markdown("**Who should be consulted?** (optional)")
            consulted = st.text_input("Consulted", value=existing.get("consulted", ""),
                placeholder="e.g. Legal, IT Security")
            
            st.markdown("**Who needs to be informed?** (optional)")
            informed = st.text_input("Informed", value=existing.get("informed", ""),
                placeholder="e.g. All HR managers")
            
            if st.form_submit_button("Save Owners", type="primary"):
                if not valid_raci(accountable, responsible):
                    st.error("Name exactly one Accountable person and at least one Responsible person.")
                else:
                    st.session_state.raci = [r for r in st.session_state.raci if r["tool_id"] != tool_id]
                    st.session_state.raci.append({
                        "tool_id": tool_id,
                        "accountable": accountable,
                        "responsible": responsible,
                        "consulted": consulted,
                        "informed": informed
                    })
                    save("raci", tool_id, st.session_state.raci[-1])
                    st.success("Owners saved!")

# ---------- SUMMARY ----------
elif page == "📊 Summary":
    st.title("Summary Dashboard")
    
    if not st.session_state.tools:
        st.info("No tools yet. Add some to see the summary.")
    else:
        data = []
        for t in st.session_state.tools:
            overall = calculate_overall_risk(t["id"])
            raci_entry = next((r for r in st.session_state.raci if r["tool_id"] == t["id"]), {})
            data.append({
                "Tool": t["name"],
                "ID": t["id"],
                "Owner": t["owner"],
                "Overall Risk": overall,
                "HIGH Flag": "YES" if tool_status(t["id"])[2] else "NO",
                "Assessment": tool_status(t["id"])[0],
                "Accountable": raci_entry.get("accountable", "—"),
                "Data Sensitivity": t["classification"]
            })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        high_tools = [t["name"] for t in st.session_state.tools if tool_status(t["id"])[2]]
        if high_tools:
            st.warning(f"**High-risk tools that need attention:** {', '.join(high_tools)}")
        else:
            st.success("No high-risk tools currently identified.")
        
        st.download_button(
            "Download summary as CSV",
            df.to_csv(index=False).encode("utf-8"),
            "vanguard_guard_summary.csv",
            "text/csv"
        )

st.sidebar.markdown("---")
st.sidebar.caption("VANGUARD-Guard v1.1 · Local-first, single-user prototype. Use fictional data only.")
