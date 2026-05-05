# AI API Self-Healing Platform

## Why we built this

In normal API testing (Postman/Newman), when a test fails:

* Execution stops or becomes unreliable
* Someone has to manually debug
* Pipelines become noisy and slow

We wanted to change that.

---

## 🎯 Our Vision

We are building an agent that can:

1. Execute Postman collections
2. Detect failures (401, 500, assertion issues, etc.)
3. Understand *why* it failed
4. Automatically fix or bypass the issue where possible
5. Continue execution (no pipeline break ❌)
6. Produce meaningful reports (with healing + AI insights)

---

## ✅ What is implemented (Phase 1 & Phase 2)

We have completed the **core engine**.

---

### Phase 1 — Self-Healing Engine

✔ Runs collections using Newman
✔ Detects failures from reports
✔ Handles:

* **401 (Auth issues)** → refresh token + retry
* **500 errors** → retry request
* Request-level re-execution (not full collection)
  ✔ Updates Postman environment dynamically

👉 This ensures execution does not fail immediately.

---

### Phase 2 — AI + Auto Fix

✔ AI analyzes failures
✔ Identifies:

* Root cause
* Suggested fix
* Confidence

✔ Auto-fix engine:

* Updates assertion status codes in collection
* Re-runs collection after fix

✔ Safe guards:

* Rate limit on AI calls
* Skip low-confidence fixes
* Skip non-numeric corrections

✔ Reports include:

* Failure type
* Healing result
* AI insight

---

## ⚠️ What is NOT implemented yet

Being honest here:

* No schema auto-fix
* No dynamic test data generation
* No learning from past failures
* Some requests can’t be re-run (missing raw URL in Newman)
* Auto-fix supports only limited assertion patterns

---

## 🏗️ Architecture (Simple View)

```
Postman Collection
        ↓
   Newman Runner
        ↓
  Failure Analyzer
        ↓
 ┌───────────────┬────────────────┐
 ↓               ↓                ↓
Healing Engine   AI Analyzer      Report Builder
 ↓               ↓
Request Runner   Auto Fix Engine
```

---

## 📁 Project Structure (Important Files Only)

### `main.py`

Main entry point.

Controls:

* Running collections
* Failure analysis
* Healing
* AI calls
* Auto-fix
* Reporting

👉 Start here if you are new.

---

### `config/settings.yaml`

Defines:

* Which collections to run
* Environment file
* AI model config

---

### `runner/newman_runner.py`

* Runs Postman collection using Newman
* Generates JSON report

---

### `runner/request_runner.py`

* Executes a single API request
* Used during healing
* Replaces variables from environment
* Injects auth token

---

### `analyzer/failure_analyzer.py`

* Reads Newman report
* Extracts failures
* Classifies them into types:

```
AUTH / SERVER / ASSERTION / DATA / PERMISSION / PREREQUEST / UNKNOWN
```

---

### `healing/healing_engine.py`

Core logic of Phase 1.

Handles:

* Token refresh (401)
* Retry (500 errors)
* Prevents repeated token calls
* Validates request before retry

---

### `healing/auto_fix_engine.py`

Phase 2 component.

* Takes AI suggestion
* Updates Postman collection
* Fixes assertion status codes

Example:

```
pm.response.to.have.status(200)
→ pm.response.to.have.status(404)
```

---

### `ai/ai_analyzer.py`

* Calls LLM (OpenAI)
* Sends failure details
* Gets:

  * root cause
  * suggested fix
  * confidence

Includes:

* API key handling
* Rate limiting
* Safe fallback

---

### `reporting/report_builder.py`

Generates:

* Excel report
* HTML report

Includes:

* Failure details
* Healing result
* AI output

---

### `utils/env_updater.py`

* Updates token inside Postman environment JSON

---

### `utils/dashboard.py`

* CLI dashboard
* Shows progress, logs, and summary

---

## ⚙️ Setup

### 1. Install dependencies

```
pip install requests rich openpyxl python-dotenv
```

---

### 2. Install Newman

```
npm install -g newman
```

---

### 3. Create `.env`

```
OPENAI_API_KEY=your_key_here
```

---

### 4. Configure collections

Edit:

```
config/settings.yaml
```

---

## ▶️ How to Run

### Run using Python

```
python3 main.py
```

---

### Run using Newman only (baseline)

```
newman run collections/user_flows.json \
  --environment collections/env/user_env.json
```

---

## 📊 Output

* Console logs (with healing + AI steps)
* `test_report.xlsx`
* `test_report.html`

---

## 🧠 How the flow works (simple)

1. Run collection
2. Capture failures
3. Try healing (auth / retry)
4. If still failing → call AI
5. If AI confident → apply fix
6. Re-run
7. Log everything

---

## 🚀 Phase 3 

Goal: **Make system smarter**

You should implement:

* Store failure history (file or DB)
* Learn from repeated failures
* Suggest fixes without AI call (cache)
* Generate new test cases based on patterns

👉 Start from:

* `failure_analyzer.py`
* Extend AI output usage

---

## 🚀 Phase 4 (scale this)

Goal: **Make it usable in real environments**

* CI/CD integration (GitHub Actions)
* Run multiple collections
* Add dashboard (UI)
* Add execution history

---

## 👨‍💻 Notes for Next Developer

* Do not change core flow in `main.py`
* Extend functionality, don’t break pipeline
* Keep AI optional (system should work without it)
* Maintain safety (no risky auto-fixes)

---

## 🔚 Final Note

We have built the **foundation**:

* Execution ✅
* Healing ✅
* AI understanding ✅
* Auto-fix (basic) ✅

Next phases are about:

* Intelligence
* Learning
* Scale

---

This is not a finished product yet —
but it is a strong base to build a **self-improving API testing system**.

---

