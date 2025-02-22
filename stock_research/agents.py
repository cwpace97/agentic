import os
import yaml
from crewai import Agent, Crew, Process
from crewai.project import agent, crew

from tools.calculator_tool import CalculatorTool
from tools.sec_analysis_tool import SEC10KTool #, SEC10QTool

from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

class StockAnalysisAgents:
    def __init__(self, ticker):
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
        current_folder = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(current_folder, "config/agents.yaml"), "r") as agent_stream: 
            self.agents_config = yaml.safe_load(agent_stream)
        self.ticker = ticker

    @agent
    def financial_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            verbose=True,
            llm=self.llm,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
                # SEC10QTool(self.ticker),
                SEC10KTool(self.ticker),
            ]
        )

    @agent
    def research_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['research_analyst'],
            verbose=True,
            llm=self.llm,
            tools=[
                ScrapeWebsiteTool(),
                # WebsiteSearchTool(), 
                # SEC10QTool(self.ticker),
                SEC10KTool(self.ticker),
            ]
        )
    
    # @agent
    # def financial_analyst_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['financial_analyst'],
    #         verbose=True,
    #         llm=self.llm,
    #         tools=[
    #             ScrapeWebsiteTool(),
    #             WebsiteSearchTool(),
    #             CalculatorTool(),
    #             SEC10QTool(),
    #             SEC10KTool(),
    #         ]
    #     )
    
    @agent
    def investment_advisor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['investment_advisor'],
            verbose=True,
            llm=self.llm,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
            ]
        )    
    
    @crew
    def crew(self) -> Crew:
        """Creates the Stock Analysis"""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )