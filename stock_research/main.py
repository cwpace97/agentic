import os
from crewai import Crew, Process

from dotenv import load_dotenv
from textwrap import dedent
from agents import StockAnalysisAgents
from tasks import StockAnalysisTasks

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SEC_API_KEY"] = os.getenv("SEC_API_KEY")

class CustomCrew:
    def __init__(self, ticker):
        self.ticker = ticker

    def run(self):
        # Define custom agents
        agents = StockAnalysisAgents(self.ticker)
        financial_agent = agents.financial_agent()
        research_analyst_agent = agents.research_analyst_agent()
        # financial_analyst_agent = agents.financial_analyst_agent()
        investment_advisor_agent = agents.investment_advisor_agent()

        #Define custom tasks
        tasks = StockAnalysisTasks()
        financial_analysis_task = tasks.financial_analysis(financial_agent)
        research_task = tasks.research(research_analyst_agent)
        filings_analysis_task = tasks.filings_analysis(financial_agent)
        recommend_task = tasks.recommend(investment_advisor_agent)

        # NEW
        options_task = tasks.find_options(research_analyst_agent)

        # Define your custom crew here
        crew = Crew(
            # agents=[financial_agent, research_analyst_agent, investment_advisor_agent],
            # tasks=[financial_analysis_task, research_task, filings_analysis_task, recommend_task],
            agents=[research_analyst_agent],
            tasks=[options_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        return result

if __name__ == "__main__":
    print("## Welcome to CrewAI Stock Analysis")
    print("-------------------------------")
    ticker = input(dedent("""Enter your ticker: """))

    custom_crew = CustomCrew(ticker)
    result = custom_crew.run()
    print("\n\n########################")
    print("## Here is you custom crew run result:")
    print("########################\n")
    print(result)
