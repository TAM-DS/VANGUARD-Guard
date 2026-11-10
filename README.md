# VANGUARD-Guard · Cross-Functional Enterprise AI Playbook
### Your organization has an AI strategy. Can it prove who's accountable for the AI already in use?

**Inventory the tools. Identify the risks. Name the owners. Make oversight visible.**

AI adoption is not the same as AI governance. A policy alone cannot tell an organization which tools are in use, what information they process, where human approval is required, or who is accountable when something goes wrong.

**VANGUARD-Guard** (formerly **ai-governance-app**) is a free, open-source starting point for answering those questions—with a working, local-first Streamlit application and an accompanying governance methodology.

> **Public Edition · VANGUARD-Guard v1.1 available**
>
> A working **local, single-user** application with SQLite persistence and tested governance rules. **Not a production-ready, multi-user compliance or audit system.** Use synthetic records only; do not enter real employee or confidential client information.

---

## From text policies to traceable governance records

**The hook:** A friendly, Streamlit-driven risk review workbench for HR, CTOs, CAIOs, risk and cross-functional corporate leaders. Instead of relying on vague policy statements, teams record AI tools, risk explanations, mitigations, named owners and review status in a local SQLite-backed workflow.

**Implemented controls:** Seven-category assessment-completeness checks; a conservative maximum-severity overall risk; visible HIGH-risk flags even on incomplete drafts; required Accountable and Responsible fields; and persistent local records. These are application-level checks, **not database-enforced enterprise RACI constraints**, independent bias detection or live model monitoring.

**Planned engineering edge:** stronger relational and database-level RACI constraints, evidence-linked approval history, prompt-regression detection and bias-evaluation alerts *before* consequential operational deployment. These capabilities are **not implemented in v1.1**.

**Operating principle:** Capability is not authority. A saved assessment is not an approval to deploy or act.

## Start here: the workbook and the app

**One practical governance foundation. Two ways to engage with it.**

**For HR leaders, CTOs, CAIOs, and cross-functional risk owners:** the **AI Governance Excel Toolkit** helps establish the foundation—identify AI tools, structure risk assessments, assign accountability, and create a repeatable review process.

The **AI Governance Helper for HR** translates the approach into a guided Streamlit experience so nontechnical teams can register tools, work through risk reviews, assign owners, and view a summary. **Version 1.1 saves records locally in SQLite**, including after a restart. Shared access, tamper-resistant audit history, and advanced automation remain future work.

> **Available now:** clone the v1.1 Streamlit application and run it locally. **Coming soon:** an updated downloadable Excel Public Edition and additional supporting documentation.

### See the AI Governance Helper

![AI Governance Helper for HR — Streamlit home screen](docs/images/01-AI-Governance_App-HR-Teams.png)

*Screenshot of the original Streamlit interface. The published v1.1 release retains the guided workflow and adds local persistence and stronger validation.*

## Built to use. Open to adapt.

**No single governance workflow fits every organization. That's the point of making this open source.**

Start with the working local application and the documented governance methodology. Then **clone or download the repository, change the questions, extend the workflow, integrate your systems, and tailor it to your own organization's policies and risk tolerance**.

Different teams face different requirements:

- **HR leaders** may prioritize hiring fairness, privacy, human review, and employee-impact controls.
- **CTOs and AI platform teams** may focus on identity, access, integrations, reliability, and operational risk.
- **CAIOs, risk, and compliance teams** may adapt assessment criteria, accountable roles, reporting, and review cadence.

This project is a **starting point, not a one-size-fits-all mandate**. Its seven-category methodology is an example of a consistent baseline; adopting organizations must independently decide which additional assessments, controls, laws, or approvals apply to their use cases.

**Make it yours:** [Browse the source](https://github.com/TAM-DS/VANGUARD-Guard) · [Download ZIP](https://github.com/TAM-DS/VANGUARD-Guard/archive/refs/heads/main.zip) · [Suggest an improvement](https://github.com/TAM-DS/VANGUARD-Guard/issues)

Released under the [MIT License](LICENSE): you can use, modify, and redistribute the software, including commercially, provided you follow the license terms. **Do not use actual confidential HR or client data in the current local app**, and review security, privacy, and regulatory requirements before organizational deployment.

## The executive question

Before giving another AI system access to a consequential workflow, can your organization answer these questions?

| Question | What operational governance needs |
|---|---|
| **What AI is actually in use?** | A consistent inventory, including shadow-AI discovery practices |
| **What could go wrong?** | Repeatable risk categories, rationale, mitigations, and visible HIGH flags |
| **Who owns the outcome?** | Named owners and explicit Responsible / Accountable assignments |
| **What can be demonstrated?** | Evidence of review, current status, and documented decisions |
| **What needs attention next?** | A practical assessment and operating cadence |

**Capability is not authority.** A tool can generate an answer without being authorized to make the decision.

## What you'll find here

### 🖥️ Guided Streamlit experience

A friendly interface oriented toward nontechnical teams:

`Home → Add a Tool → My Tools → Assess Risks → Assign Owners → Summary`

**Version 1.1 is available as a local, single-user app.** Seven automated tests passed, and the owner verified the registration → assessment → ownership → dashboard workflow and persistence across restart. This is not independent certification or production security verification.

### 📘 Governance methodology

The accompanying implementation approach defines:

- **Seven risk categories:** Accuracy, Privacy, Bias, Security, Legal, Dependency, Reputation.
- **Explicit triage:** LOW, MEDIUM, HIGH, using the **highest category score** for overall risk.
- **Assessment completeness:** all seven categories require score, rationale, mitigation, owner, and date.
- **Early HIGH visibility:** recorded HIGH flags should remain visible even if an assessment is incomplete.
- **Named accountability:** exactly one Accountable (A), at least one Responsible (R), and a named accountable individual.
- **Review cadence:** an assessment becomes overdue after three calendar months.
- **Maturity assessment:** 20 questions scored 1–5, with no maturity level on partial or invalid responses.

These are **documented methodology rules**, not blanket claims about features already implemented in the Streamlit code.

### 📊 Supporting toolkit and public documentation

The Excel Governance Toolkit provides the structured foundation. **An updated downloadable Public Edition is coming soon**, together with an app screenshot, executive presentation, and implementation guide. Links will be added once the files are published.

## Who it's for

- **Business and HR teams:** understand the tools being used and surface ownership and review questions.
- **Risk, security, and compliance teams:** establish a structured conversation around evidence, controls, and gaps.
- **Cloud and AI platform engineers:** demonstrate where governance boundaries need to meet implementation.
- **Consultants and transformation leaders:** use a concise, repeatable starting point for discovery workshops.

This toolkit is **vendor-neutral** and does not require purchasing an enterprise governance platform to explore the methodology.

## Run VANGUARD-Guard v1.1 locally

**The application source, dependencies, and tests are published in this repository.** The following commands clone and run the local v1.1 application:

```bash
git clone https://github.com/TAM-DS/VANGUARD-Guard.git
cd VANGUARD-Guard

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL reported by Streamlit (typically `http://localhost:8501`). On Windows, activate with `.venv\Scripts\activate`.

**Do not upload local virtual environments, passwords, client files, employee records, or applicant information.** The repository includes a `.gitignore` for common local artifacts.

## Suggested demo: an AI resume-screening tool

Use entirely fictional names and synthetic data:

1. Register a hypothetical resume-screening application and describe its proposed use.
2. Consider the risk of incorrect rejection, bias, personal-data exposure, and security failures.
3. Record the mitigation and who must review decisions before any action is taken.
4. Assign a named accountable owner and examine the summary.
5. Stop and restart Streamlit, then confirm the saved tool, assessment, and owners remain available from the local SQLite database.

**Important:** An AI-generated recommendation to reject a candidate is **not authorization** to do so. Actual employment-related use requires appropriate human review, legal analysis, technical validation, and organizational controls.

## Implementation roadmap

| Stage | Focus | Evidence of completion |
|---|---|---|
| **1. Discover** | Tool inventory, data, users, stable IDs | Reconciled list of use cases |
| **2. Assess** | Seven risk categories and mitigations | Complete, reviewed risk records |
| **3. Assign** | Named owners and responsibility | Accountable owner + responsible roles |
| **4. Operate** | Review cadence and escalation | Dated decisions and tracked actions |
| **5. Improve** | Governance maturity and control gaps | Prioritized improvement plan |

The broader methodology offers an illustrative phased rollout; real scope depends on the organization.

## Trust boundaries and limitations

**This project does not:**

- certify compliance with NIST AI RMF, ISO/IEC 42001, the EU AI Act, or any law;
- replace legal advice, security reviews, bias testing, red teaming, or enterprise model evaluation;
- provide authentication, secure multi-user persistence, tamper-resistant audit trails, or production-grade access controls in the current app;
- prove that the Streamlit prototype enforces every rule in the accompanying governance methodology;
- authorize an AI tool to make consequential decisions about people, customers, finances, or operations.

**Standards alignment** means the methodology can *support* governance activities; it is not a certification or regulatory determination.

## Continuous improvement — release roadmap

The goal is a **useful, approachable governance tool that improves through real-world feedback**, not a one-time demo or a promise of enterprise features that do not yet exist.

| Stage | Focus | Status |
|---|---|---|
| **v1.0 · Streamlit prototype** | Register AI tools, assess risks, assign owners, and view a summary in a guided interface | Initial local prototype |
| **v1.1 · Practical usability upgrade** | Local SQLite persistence, stronger risk-completion checks, HIGH-risk visibility, and Responsible/Accountable validation | **Released — code and tests available** |
| **Next · Community-informed improvements** | Excel import/export, clearer reporting, accessibility, and additional tests | Planned; priorities will respond to user feedback |
| **Later · Multi-user capabilities** | Authentication, permissions, shared storage, and audit history | Exploratory; not part of the local release |

**Engineering principle:** make the basic workflow dependable, validate the controls, and expand only when users have a demonstrated need. Public release notes will distinguish *implemented and tested*, *in progress*, and *planned*.

**Want to help shape it?** Open a [GitHub Issue](https://github.com/TAM-DS/VANGUARD-Guard/issues) with a use case, bug report, accessibility improvement, or feature suggestion. Please do not post sensitive employee or client information.

### Future enhancement: AI Spend & Value

**AI governance should consider both risk and business value.** A future **AI Spend & Value** feature could help teams connect each registered AI tool to its cost, ownership, purpose, and measurable outcomes.

| Field | Business question |
|---|---|
| **Monthly AI cost** | How much are we spending? |
| **Business owner** | Who is accountable for the expense? |
| **Business purpose** | What are we trying to accomplish? |
| **Measurable outcome** | What improvement can we demonstrate? |
| **Review decision** | Continue, optimize, expand, or retire? |

**Status: proposed enhancement — not implemented.** This is a potential addition to the roadmap, subject to user feedback. The objective is to support more informed investment decisions, not simply enforce a flat spending cap.

### v1.1 usability improvements

Based on hands-on testing, v1.1 makes the assessment workflow clearer:

- **Save Assessment / Save Draft:** saving an incomplete assessment is allowed and does not imply approval
- **Visible completion requirements:** each of the seven categories needs a risk level, explanation, mitigation, named risk owner, and recorded date
- **Persistent save feedback:** explicitly confirms whether an assessment was saved as a draft or completed
- **Human scoring:** MEDIUM is an initial selection in the form, not an automatically determined risk
- **Early HIGH flags:** a known HIGH risk remains visible even when supporting fields are incomplete

**Verification:** seven automated tests passed and the user verified registration, risk scoring, RACI assignment, dashboard reporting, and persistence across a local application restart. This does not constitute a production security audit or independent compliance assessment. **The validated v1.1 source and tests are now published in this repository.**

## Before wider deployment

Current engineering priorities:

- [ ] Commit and inspect the actual Streamlit source and dependencies.
- [ ] Test the end-to-end registration → risk → ownership → summary path.
- [ ] Implement and test all seven-category completeness and severity rules.
- [ ] Validate RACI constraints, HIGH risk visibility, and overdue-review calculations.
- [ ] Add appropriate durable storage, authentication, authorization, and audit history.
- [ ] Publish tested, clearly labeled Public Edition supporting materials.
- [ ] Add reproducible automated tests and a guided synthetic-data demonstration.

Issues and thoughtful contributions are welcome—especially around usability, trustworthy governance boundaries, testing, accessibility, and maintainability.

## Why this exists

Enterprise AI governance should be **understandable to the people responsible for using it**, not confined to a policy document.

Start with the workflow. Make decisions explicit. Preserve human authority. Document the evidence.

**Clarity over cleverness. Correctness over speed. Evidence over hype.**

---

**Created by Tracy Anne Griffin Manning**  
AI Architect | Enterprise Cloud Architecture | AI Strategy & Consulting  
[Professional site](https://tam-ds.github.io/) · [LinkedIn](https://www.linkedin.com/in/tracymanning/) · [GitHub](https://github.com/TAM-DS)

**License:** [MIT](LICENSE). Free to use, modify, and share under the license terms.
