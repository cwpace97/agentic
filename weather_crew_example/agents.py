from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from WeaterAPI import retrieve_weather_data


class WeatherAgents:
    def __init__(self):
        # self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4o = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

    def weather_agent(self):
        return Agent(
            role="Weather Data Retriever",
            backstory=dedent(f"""You are a renowned Weather Data Retriever."""),
            goal=dedent(f"""
            Convert geolocations to longitude and latitude coordinates.
            Retrieve weather data from the Weather API endpoint.
            """),
            tools=[retrieve_weather_data],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )

    def writer_agent(self):
        return Agent(
            role="Weather Analyst",
            backstory=dedent(f"""You have spent your entire life reporting on weather data."""),
            goal=dedent(f"""Take the information from the weather agent and present a report to the general public."""),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )
