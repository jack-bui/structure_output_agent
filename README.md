# Financial Structured Output Agent

A small Google ADK agent that reads company financial reports and returns a **strict, structured JSON** containing `revenue`, `cogs`, `net_income`, and a `note`. The model is constrained by a Pydantic schema to ensure consistent keys and formatting.

---

## Contents

* [Overview](#overview)
* [Project Structure](#project-structure)
* [Requirements](#requirements)
* [Installation](#installation)
* [Configuration](#configuration)
* [How It Works](#how-it-works)
* [Usage](#usage)
* [Output Schema](#output-schema)
* [Examples](#examples)
* [Rounding & Currency Rules](#rounding--currency-rules)
* [Troubleshooting](#troubleshooting)
* [Development Notes](#development-notes)
* [License](#license)

---

## Overview

This agent extracts three headline financial metrics from a report:

* **Revenue** (in million USD, rounded to 2 decimals)
* **COGS** (Cost of Goods Sold, in million USD, rounded to 2 decimals)
* **Net Income** (in million USD, rounded to 2 decimals)
* **Note** (free text field to inform when currency isn’t USD or data is unavailable)

It is implemented with:

* **Pydantic v2** for the output schema validation
* **Google ADK** (`google.adk`) to orchestrate the agent and call the LLM
* **Gemini 2.0 Flash** as the default model

The agent’s system prompt instructs the model to answer **only** with a JSON object that matches the schema.

---

## Project Structure

```
.
├─ agent.py          # Defines and configures the ADK Agent
├─ __init__.py       # (optional) Package marker or local helpers
└─ README.md         # This file
```

> If your filenames differ, update commands below accordingly.

---

## Requirements

* **Python**: 3.10+ recommended
* **Pydantic**: v2+
* **google-adk** and its transitive deps
* **google-genai** (installed alongside ADK)

Install everything into a virtual environment for isolation.

---

## Installation

```bash
# 1) Create & activate a virtual environment (examples for bash/PowerShell)
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\\Scripts\\activate

# 2) Install dependencies
pip install --upgrade pip
pip install pydantic google-adk google-genai
```

> If you already have these in your environment, you can skip or pin exact versions as needed.

---

## Configuration

Set your Google Generative AI credentials so ADK can call Gemini. Typical environment variables include (names may vary by setup):

```bash
export GOOGLE_API_KEY="<your_api_key>"
# or, depending on your stack
export GOOGLE_GENAI_API_KEY="<your_api_key>"
```

> If your organization uses service accounts or different auth flows, follow the internal setup instructions for `google-adk`/`google-genai` in your environment.

---

## How It Works

1. **Schema definition** (Pydantic):

   ```python
   class Financial(BaseModel):
       revenue: str = Field(description="Revenue in million USD, rounded to 2 decimals")
       cogs: str = Field(description="Cost of goods sold in million USD, rounded to 2 decimals")
       net_income: str = Field(description="Net income in million USD, rounded to 2 decimals")
       note: str = Field(description="Explain if currency is not USD or data is unavailable")
   ```

2. **Agent configuration** (ADK): The agent binds the schema as `output_schema` and supplies strict system instructions telling the LLM to respond only with JSON matching the schema.

3. **Run**: You invoke the agent via the ADK CLI. The runner calls Gemini with the prompt and validates the response against the Pydantic schema.

---

## Usage

Two common ways to run with Google ADK CLI are:

```bash
# Option A: Run the module/script directly (most common)
adk run agent.py

# Option B: Run via adk web
# adk web
```

You’ll be dropped into an interactive session. Provide a pdf file and the agent will get to work


---

## Output Schema

The agent returns a **single JSON object** with these keys (all strings):

```json
{
  "revenue": "<amount in million USD, 2 decimals>",
  "cogs": "<amount in million USD, 2 decimals>",
  "net_income": "<amount in million USD, 2 decimals>",
  "note": "<explain non-USD currency or unavailable data>"
}
```

* **Formatting**: numeric values are strings formatted to **two decimals** (e.g., `"123.45"`).
* **On missing data or non-USD sources**: set `revenue`, `cogs`, and `net_income` to `"0.00"` and explain the reason in `note`.

---
