# To know more about the Task class, visit: https://docs.crewai.com/concepts/tasks
from crewai import Task
from textwrap import dedent


class WeatherTasks:

    def convert_geolocation(self, agent, geolocation):
        return Task(
            description=dedent(
                f"""
                Given the geolocation below, you will use the web to retrieve the exact coordinates of geolocation.
            
                Geolocation: {geolocation}
                """
            ),
            expected_output="You will return the precise longitude and latitude of the geolocation.",
            agent=agent,
        )

    def get_weather_data(self, agent):
        return Task(
            description=dedent(
                f"""
                Given the latitude and longitude generated from the 'convert_geolocation' task, you will call the 
                `retrieve_weather_data` function to retrieve the weather data for the given coordinates.
                """
            ),
            expected_output="You will return the JSON output of the retrieve_weather_data function.",
            agent=agent,
        )


    def summarize_weather_data(self, agent):
        return Task(
            description=dedent(
                f"""
                You will examine the output from the get_weather_data task and provide a summary of the weather. Make sure
                that you convert everything to farenheit.
                """
            ),
            expected_output="You will return a public-friends weather report.",
            agent=agent,
        )
