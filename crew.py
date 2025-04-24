# crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool
from tools.salesforce_api_tool import SalesforceAPITool
from tools.calendly_link_tool import CalendlyLinkGeneratorTool
from tools.snowflake_logger_tool import SnowflakeLoggerTool
from tools.stripe_customer_tool import StripeCustomerTool
from schemas.lead import Lead


from dotenv import load_dotenv
import yaml

load_dotenv()

@CrewBase
class SalesOnboardingCrew():
    def __init__(self):
        self.agents_config = self._load_yaml("config/agents.yaml")
        self.tasks_config = self._load_yaml("config/tasks.yaml")

    def _load_yaml(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    @agent
    def lead_research_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_research_analyst'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            memory=False,
        )

    @agent
    def lead_normalizer_agent(self) -> Agent:
        return Agent(
            config={
                "role": "Lead Data Normalizer",
                "goal": "Convert raw LLM output into structured, valid Lead JSON.",
                "backstory": "You ensure lead instructions conforms exactly to a known structure using JSON. You remove summaries and unnecessary nesting."
            },
            tools=[],  # No tools needed
            verbose=True,
            memory=False,
        )

    @agent
    def lead_scoring_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_scoring_agent'],
            tools=[FileReadTool(file_path='instructions/scoring_rules.txt')],
            verbose=True,
            memory=False,)

    @agent
    def salesforce_account_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['salesforce_account_creator'],
            tools=[SalesforceAPITool()],
            verbose=True,
            memory=False,
        )

    @agent
    def meeting_scheduler(self) -> Agent:
        return Agent(
            config=self.agents_config['meeting_scheduler'],
            tools=[CalendlyLinkGeneratorTool()],
            verbose=True,
            memory=False,
        )

    @agent
    def stripe_customer_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['stripe_customer_creator'],
            tools=[StripeCustomerTool()],
            verbose=True,
            memory=False,
        )

    @agent
    def final_summary_agent(self) -> Agent:
        return Agent(
            config={"role": "Summary Generator", "goal": "Combine outputs",
                    "backstory": "You're a finalizer that merges outputs."},
            tools=[],
            verbose=True,
            memory=False,
        )

    @agent
    def logger_agent(self) -> Agent:
        return Agent(
            config={
                "role": "Audit Logger",
                "goal": "Write outputs to Snowflake for tracking",
                "backstory": "You log onboarding records to Snowflake"
            },
            tools=[SnowflakeLoggerTool()],
            verbose=True,
            memory=False,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.lead_research_analyst(),
        )

    @task
    def normalize_research_output_task(self) -> Task:
        return Task(
            description="""
            Take the output from `research_task`, which may be wrapped in 'input', 'metadata', or 'description',
            and return a valid flat JSON object that matches the Lead schema.

            Remove any summary text, markdown formatting, or irrelevant keys.

            Output must exactly match this format:
            {
              "name": "Square Inc.",
              "email": "support@square.com",
              "phone": "1234567890",
              "website": "https://squareup.com",
              "address": "San Francisco, CA",
              "industry": "Financial Services",
              "number_of_employees": 5000,
              "annual_revenue": "$4.7B",
              "decision_makers": [{"name": "Jack Dorsey", "role": "CEO", "linkedin": ""}],
              "recent_news": [],
              "funding_stage": "",
              "ipo_status": "",
              "source_links": []
            }
            """,
            agent=self.lead_normalizer_agent(),
            context=[self.research_task()],
            expected_output="Cleaned and structured Lead JSON with all fields at top level"
        )

    @task
    def lead_scoring_task(self) -> Task:
        return Task(
           config=self.tasks_config['lead_scoring_task'],
           agent=self.lead_scoring_agent(),
           context=[self.normalize_research_output_task()],
        )

    @task
    def create_salesforce_account_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_salesforce_account_task'],
            agent=self.salesforce_account_creator(),
            context=[self.normalize_research_output_task()]
        )

    @task
    def schedule_meeting_task(self) -> Task:
        return Task(
            config=self.tasks_config['schedule_meeting_task'],
            agent=self.meeting_scheduler(),
            context=[self.normalize_research_output_task()],
        )



    @task
    def create_stripe_customer_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_stripe_customer_task'],
            agent=self.stripe_customer_creator(),
            context=[self.normalize_research_output_task()]
        )


    @task
    def final_summary_task(self) -> Task:
        return Task(
            agent=self.final_summary_agent(),
            context=[
                self.normalize_research_output_task(),
                self.lead_scoring_task(),
                self.create_salesforce_account_task(),
                self.schedule_meeting_task(),
                self.create_stripe_customer_task()
            ],
            config=self.tasks_config['final_summary_task'],)

    @task
    def log_final_output_task(self) -> Task:
        return Task(
            description="Log the final onboarding output JSON to Snowflake",
            agent=self.logger_agent(),
            context=[self.final_summary_task()],
            expected_output="Confirmation from Snowflake logging",
            input_template="""
            {
              "step": "final_summary",
              "payload": {final_summary_task.output}
            }
            """
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks + [self.log_final_output_task()],
            process=Process.sequential,
            verbose=True,
        )
