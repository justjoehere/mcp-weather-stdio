import asyncio
import json
import logging
from typing import Any, Sequence

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource
)

from mcp_weather_service_stdio.weather_util import Weather

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("weather-mcp-server-stdio")

class WeatherServer:
    def __init__(self):
        logger.debug("Initializing WeatherServer")
        self.app = Server("weather-mcp-server-stdio")
        logger.debug("Setting up tools")
        self.setup_tools()
        logger.debug("Tools setup complete")

    def setup_tools(self):
        @self.app.list_tools()
        async def list_tools() -> list[Tool]:
            """List available weather tools."""
            logger.debug("Listing tools")
            tools = [
                Tool(
                    name="get_current_weather",
                    description="Get current weather and forecast for a location",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "location_name": {
                                "type": "string",
                                "description": "The location to get the weather for"
                            }
                        },
                        "required": ["location_name"]
                    }
                )
            ]
            logger.debug(f"Returning {len(tools)} tools")
            return tools

        @self.app.call_tool()
        async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """Handle tool calls for weather data."""
            logger.debug(f"Tool call received: {name} with arguments {arguments}")
            if name != "get_current_weather":
                logger.error(f"Unknown tool: {name}")
                raise ValueError(f"Unknown tool: {name}")

            if not isinstance(arguments, dict) or "location_name" not in arguments:
                logger.error("Invalid weather arguments")
                raise ValueError("Invalid weather arguments")

            try:
                location_name = arguments["location_name"]
                logger.debug(f"Getting weather for {location_name}")
                weather = await Weather(locale='en', unit='imperial').get_forecast(location_name)
                logger.debug("Weather data received")

                forecasts = []
                for forecast in weather.daily_forecasts:
                    forecasts.append({
                        'date': forecast.date.strftime('%Y-%m-%d'),
                        'high_temperature': forecast.highest_temperature,
                        'low_temperature': forecast.lowest_temperature
                    })

                weather_data = {
                    "currently": {
                        "current_temperature": weather.temperature,
                        "sky": weather.kind.emoji,
                        "feels_like": weather.feels_like,
                        "humidity": weather.humidity,
                        "wind_speed": weather.wind_speed,
                        "wind_direction": (weather.wind_direction.value + weather.wind_direction.emoji),
                        "visibility": weather.visibility,
                        "uv_index": weather.ultraviolet.index,
                        "description": weather.description,
                        "forecasts": forecasts
                    }
                }

                logger.debug("Returning weather data response")
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(weather_data, indent=2)
                    )
                ]

            except Exception as e:
                logger.error(f"Weather API error: {str(e)}")
                raise RuntimeError(f"Weather API error: {str(e)}")

    async def run(self):
        # Import here to avoid issues with event loops
        from mcp.server.stdio import stdio_server

        logger.debug("Starting STDIO Weather Server")
        async with stdio_server() as (read_stream, write_stream):
            logger.debug("Acquired stdio streams")
            init_options = self.app.create_initialization_options()
            logger.debug("Created initialization options")
            logger.debug("Executing server run command")
            await self.app.run(
                read_stream,
                write_stream,
                init_options
            )
            logger.debug("Server run complete")

# Entry point
async def main():
    logger.debug("Starting main")
    server = WeatherServer()
    logger.debug("Server created, starting run")
    await server.run()
    logger.debug("Run complete")

def cli_main():
    """Non-async entry point for command line."""
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()