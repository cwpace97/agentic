import os
import yaml

from crewai import Task
from crewai.project import task

class StockAnalysisTasks:
    def __init__(self):
        current_folder = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(current_folder, "config/tasks.yaml"), "r") as task_stream: 
            self.tasks_config = yaml.safe_load(task_stream)
    
    @task
    def financial_analysis(self, financial_agent) -> Task: 
        return Task(
            config=self.tasks_config['financial_analysis'],
            agent=financial_agent
        )
    
    @task
    def research(self, research_analyst_agent) -> Task:
        return Task(
            config=self.tasks_config['research'],
            agent=research_analyst_agent,
        )
    
    # @task
    # def financial_analysis(self, financial_analyst_agent) -> Task: 
    #     return Task(
    #         config=self.tasks_config['financial_analysis'],
    #         agent=financial_analyst_agent,
    #     )
    
    @task
    def filings_analysis(self, financial_analyst_agent) -> Task:
        return Task(
            config=self.tasks_config['filings_analysis'],
            agent=financial_analyst_agent,
        )

    @task
    def recommend(self, investment_advisor_agent) -> Task:
        return Task(
            config=self.tasks_config['recommend'],
            agent=investment_advisor_agent,
        )
    
    @task
    def find_options(self, research_analyst_agent) -> Task:
        return Task(
            config=self.tasks_config['options'],
            agent=research_analyst_agent
        )