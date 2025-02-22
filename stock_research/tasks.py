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
    def research(self, market_research_analyst_agent) -> Task:
        return Task(
            config=self.tasks_config['research'],
            agent=market_research_analyst_agent,
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
    
    # NEW TASKS
    @task
    def gather_stock_history(self, stock_history_agent) -> Task:
        return Task(
            config=self.tasks_config['gather_stock_history'],
            agent=stock_history_agent,
        )