# Agentic AI Fraud Detection System

An end-to-end AI fraud detection platform combining machine learning, explainable AI, LLM-powered investigation, and a real-time monitoring dashboard.

This project demonstrates how modern financial institutions detect and investigate suspicious transactions using  multi-agent AI systems.

---

# Key Highlights

* Machine Learning Fraud Detection Model (XGBoost)
* Explainable AI using SHAP
* LLM-powered Investigation Agent
* Multi-Agent Architecture
* FastAPI Fraud Detection API
* Real-time Monitoring Dashboard (Streamlit)

The system automatically:

1. Detects suspicious transactions
2. Explains why they are suspicious
3. Generates investigation summaries
4. Displays alerts in a monitoring dashboard

---

# System Architecture

<pre class="overflow-visible! px-0!" data-start="1955" data-end="2198"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼ5 ͼj"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Transaction</span><br/><span>     │</span><br/><span>     ▼</span><br/><span>Detection Agent (XGBoost ML Model)</span><br/><span>     │</span><br/><span>     ▼</span><br/><span>Explainability Engine (SHAP)</span><br/><span>     │</span><br/><span>     ▼</span><br/><span>Investigation Agent (LLM)</span><br/><span>     │</span><br/><span>     ▼</span><br/><span>Decision Agent (Fraud Policy Engine)</span><br/><span>     │</span><br/><span>     ▼</span><br/><span>Fraud Monitoring Dashboard</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

<img width="1536" height="1024" alt="architechture" src="https://github.com/user-attachments/assets/e4d357d2-0d52-4a7b-8298-64383c6c6ff9" />

---

# Technology Stack

| Layer           | Technology     |
| --------------- | -------------- |
| ML Model        | XGBoost        |
| Explainability  | SHAP           |
| API             | FastAPI        |
| Dashboard       | Streamlit      |
| LLM Agent       | Google Gemini  |
| Data Processing | Pandas / NumPy |
| Deployment      | Uvicorn        |

---

# Multi-Agent Design

This project implements 3 cooperating AI agents.

### 1. Detection Agent

* Predicts fraud probability using XGBoost
* Uses behavioral features such as velocity and spending patterns

### 2. Investigation Agent

* Uses LLM reasoning to explain suspicious transactions
* Converts SHAP signals into analyst-friendly explanations

Example:

<pre class="overflow-visible! px-0!" data-start="2830" data-end="3017"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼ5 ͼj"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Transaction flagged because the transaction amount is significantly higher than the user's typical spending behavior and multiple transactions occurred within a short time window.</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

### 3. Decision Agent

Applies fraud policy rules:

<pre class="overflow-visible! px-0!" data-start="3072" data-end="3137"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼ5 ͼj"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>score > 0.7 → BLOCK</span><br/><span>0.4–0.7 → INVESTIGATE</span><br/><span>< 0.4 → APPROVE</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# Monitoring Dashboard

The Streamlit dashboard allows fraud analysts to:

* Input transaction details
* View fraud risk scores
* See automated investigation summaries
* Visualize risk features

Example output:

<pre class="overflow-visible! px-0!" data-start="3359" data-end="3475"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼ5 ͼj"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>Fraud Probability: 0.82</span><br/><span>Decision: BLOCK</span><br/><span>Reason: Unusual transaction amount and abnormal transaction velocity</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

![streamlit_fraud_detection_system](https://github.com/user-attachments/assets/580a4330-cf5d-43f6-8b15-76ddcebc0126)

---

# Fraud Features Used

The model uses behavioral features such as:

<pre class="overflow-visible! px-0!" data-start="3553" data-end="3706"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼ5 ͼj"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>TransactionAmt</span><br/><span>txn_count_1h</span><br/><span>txn_count_24h</span><br/><span>txn_count_7d</span><br/><span>avg_amt_1h</span><br/><span>avg_amt_24h</span><br/><span>avg_amt_7d</span><br/><span>max_amt_24h</span><br/><span>amount_zscore_24h</span><br/><span>velocity_risk</span><br/><span>is_night_txn</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

These capture  **transaction velocity, spending deviation, and behavioral anomalies** .

---

# Example API Request

<pre class="overflow-visible! px-0!" data-start="3826" data-end="3853"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼ5 ͼj"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>POST /predict_fraud</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Request:

<pre class="overflow-visible! px-0!" data-start="3865" data-end="4126"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class=""><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼ5 ͼj"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>{</span><br/><span>  "TransactionAmt": </span><span class="ͼb">500</span><span>,</span><br/><span>  "txn_count_1h": </span><span class="ͼb">5</span><span>,</span><br/><span>  "txn_count_24h": </span><span class="ͼb">20</span><span>,</span><br/><span>  "txn_count_7d": </span><span class="ͼb">40</span><span>,</span><br/><span>  "avg_amt_1h": </span><span class="ͼb">30</span><span>,</span><br/><span>  "avg_amt_24h": </span><span class="ͼb">35</span><span>,</span><br/><span>  "avg_amt_7d": </span><span class="ͼb">28</span><span>,</span><br/><span>  "max_amt_24h": </span><span class="ͼb">70</span><span>,</span><br/><span>  "amount_zscore_24h": </span><span class="ͼb">4.5</span><span>,</span><br/><span>  "velocity_risk": </span><span class="ͼb">0.85</span><span>,</span><br/><span>  "is_night_txn": </span><span class="ͼb">1</span><br/><span>}</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Response:

<pre class="overflow-visible! px-0!" data-start="4139" data-end="4378"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼ5 ͼj"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>{</span><br/><span> "fraud_probability": 0.83,</span><br/><span> "decision": "BLOCK",</span><br/><span> "investigation_summary": "The transaction amount is significantly higher than the user's normal spending pattern and multiple transactions occurred within a short time window."</span><br/><span>}</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

![fraud_prediction_fastapi_1](https://github.com/user-attachments/assets/490ce000-7246-4497-9bcd-a1c910889e45)

![fraud_prediction_fastapi_2](https://github.com/user-attachments/assets/6fe3d31d-c98c-4375-9596-1639db15f43d)

![fraud_prediction_fastapi_3](https://github.com/user-attachments/assets/ab49eefc-d2f4-4e6a-aa19-8bc0cb699f7f)

### Gemini Multi-Agent Response

![gemini_multi-agent_response_investigate](https://github.com/user-attachments/assets/1cd01fde-6c84-45e1-9e4f-2cf9c373cb08)

---

# How to Run the Project

### 1. Install dependencies

<pre class="overflow-visible! px-0!" data-start="4444" data-end="4483"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼ5 ͼj"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>pip install -r requirements.txt</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

### 2. Start the Fraud Detection API

<pre class="overflow-visible! px-0!" data-start="4529" data-end="4565"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼ5 ͼj"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>uvicorn api.app:app --reload</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

### 3. Launch the Dashboard

<pre class="overflow-visible! px-0!" data-start="4602" data-end="4646"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼ5 ͼj"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>streamlit run dashboard/dashboard.py</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Open:

<pre class="overflow-visible! px-0!" data-start="4655" data-end="4684"><div class="relative w-full mt-4 mb-1"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼ5 ͼj"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>http://localhost:8501</span></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

# Future Improvements

* Real-time streaming fraud detection
* Fraud graph network analysis
* Reinforcement learning fraud policies
* Automated case management system

---
