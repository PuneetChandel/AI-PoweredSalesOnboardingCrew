# AI-Powered Sales Onboarding Crew 🚀

An end-to-end automated sales onboarding workflow built using the crewAI agentic framework.

This system uses specialized AI agents to handle lead research, enrichment, scoring, CRM setup, billing, scheduling, logging, and notifications — all orchestrated in a structured, modular flow.

![Crew Architecture](crew.png)

## ✨ Features

- **Lead Research**: Automated research and enrichment via Serper and web scraping
- **Lead Scoring**: Intelligent scoring based on business attributes (employees, revenue, etc.)
- **CRM Integration**: Automated Salesforce account creation and management
- **Billing Setup**: Stripe customer setup and checkout session generation
- **Scheduling**: Personalized Calendly scheduling link generation
- **Data Logging**: Snowflake integration for structured onboarding data storage
- **Notifications**: Email notifications using SendGrid or SMTP

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Framework**: CrewAI (agent orchestration)
- **Data Warehouse**: Snowflake

## 🔄 How It Works

Each agent in the crew is configured with:
- A defined role and backstory
- One or more tools (custom or CrewAI-compatible)
- A task that processes structured input and produces structured output

The agents work sequentially (or concurrently if configured), passing validated data between each stage using CrewAI's task context.

## 🚀 Project Setup

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
pip install --upgrade pip
uv pip install -r requirements.txt

# If you get error for email-validator
pip install email-validator
```

### 2. Environment Configuration

Create a `.env` file with the following variables:

```env
# API Keys
SERPER_API_KEY=your_serper_api_key
OPENAI_API_KEY=your_openai_api_key

# Snowflake Configuration
SNOWFLAKE_USER=your_snowflake_user
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_ACCOUNT=your_snowflake_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema

# Salesforce Configuration
SF_ACCESS_TOKEN=your_sf_access_token
SF_INSTANCE_URL=your_sf_instance_url
SF_DOMAIN=your_sf_domain

# Stripe Configuration
STRIPE_SECRET_KEY=your_stripe_secret_key
```

## 📝 Usage

1. Start the Streamlit UI:
```bash
streamlit run streamlit_app.py
```

## 🏃‍♂️ Sample Run

Here's an example of how the crew processes a lead through all stages:

### Crew Execution Flow

```plaintext
🚀 Crew: Sales Onboarding Crew
├── 📋 Lead Research
│   └── 🤖 Agent: Lead Research Analyst
│       Status: ✅ Completed
│
├── 📋 Data Normalization
│   └── 🤖 Agent: Lead Data Normalizer
│       Status: ✅ Completed
│
├── 📋 Lead Scoring
│   └── 🤖 Agent: Lead Scoring Analyst
│       Status: ✅ Completed
│
├── 📋 CRM Integration
│   └── 🤖 Agent: Salesforce Integration Agent
│       Status: ✅ Completed
│
├── 📋 Meeting Scheduling
│   └── 🤖 Agent: Meeting Scheduler Bot
│       Status: ✅ Completed
│
├── 📋 Billing Setup
│   └── 🤖 Agent: Stripe Billing Specialist
│       Status: ✅ Completed
│
├── 📋 Summary Generation
│   └── 🤖 Agent: Summary Generator
│       Status: ✅ Completed
│
└── 📋 Audit Logging
    └── 🤖 Agent: Audit Logger
        Status: ✅ Completed
```

Each agent in the crew performs its specialized task and passes the processed data to the next agent in the workflow. The status indicators show the completion state of each task and agent.
