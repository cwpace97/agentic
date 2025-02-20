import os
from crewai import Crew

from dotenv import load_dotenv
from textwrap import dedent
from agents import WeatherAgents
from tasks import WeatherTasks

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class CustomCrew:
    def __init__(self, geolocation):
        self.geolocation = geolocation

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = WeatherAgents()
        tasks = WeatherTasks()

        # Define your custom agents and tasks here
        weather_agent = agents.weather_agent()
        writer_agent = agents.writer_agent()

        # Custom tasks include agent name and variables as input
        weather_task_1 = tasks.convert_geolocation(
            weather_agent,
            self.geolocation,
        )

        weather_task_2 = tasks.get_weather_data(weather_agent)

        writer_task_1 = tasks.summarize_weather_data(
            writer_agent,
        )

        # Define your custom crew here
        crew = Crew(
            agents=[weather_agent, writer_agent],
            tasks=[weather_task_1, weather_task_2, writer_task_1],
            verbose=True,
        )

        result = crew.kickoff()
        return result


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to AI Weather Crew")
    print("-------------------------------")
    geolocation = input(dedent("""Enter your geolocation: """))

    custom_crew = CustomCrew(geolocation)
    result = custom_crew.run()
    print("\n\n########################")
    print("## Here is you custom crew run result:")
    print("########################\n")
    print(result)
