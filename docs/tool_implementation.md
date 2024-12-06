# Implementation Guide: Building Your MCP Server

This guide walks through the implementation of an MCP server step by step, using our weather service as a practical example. We'll explore not just what each piece of code does, but why we made specific design choices and how you can apply these patterns to your own MCP servers.

## Starting with the Foundation

Let's begin by examining how we set up the basic structure of our server. The foundation of any MCP server starts with importing the necessary components and establishing our server class:

```python
import asyncio
import json
import logging
from typing import Any, Sequence

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("weather-mcp-server-stdio")

class WeatherServer:
    def __init__(self):
        self.app = Server("weather-mcp-server-stdio")
        self.setup_tools()
```

In this setup, we're doing several important things. First, we establish logging - a crucial component for debugging and monitoring your server. The logger will help you understand what's happening inside your server as it processes requests. We also create our server instance with a specific identifier that helps distinguish it in logs and communications.

## Defining Your Tools

Tools are the heart of any MCP server. They define the capabilities your server offers to AI models. Let's look at how we define and implement tools:

```python
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
        return tools
```

The tool definition includes several crucial elements:
1. A clear, descriptive name that AI models will use to identify the tool
2. A detailed description that helps AI models understand when to use the tool
3. An input schema that defines exactly what information the tool needs

Think of this like writing an API documentation - the better you describe your tools, the more effectively AI models can use them.

## Implementing Tool Logic

Once we've defined our tools, we need to implement their actual functionality. Here's how we handle tool calls:

```python
@self.app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls for weather data."""
    logger.debug(f"Tool call received: {name} with arguments {arguments}")
    
    if name != "get_current_weather":
        logger.error(f"Unknown tool: {name}")
        raise ValueError(f"Unknown tool: {name}")

    try:
        location_name = arguments["location_name"]
        weather = await Weather(locale='en', unit='imperial').get_forecast(location_name)
        
        # Transform the data into a consistent format
        weather_data = {
            "currently": {
                "temperature": weather.temperature,
                "description": weather.description,
                # ... other weather details ...
            }
        }

        return [
            TextContent(
                type="text",
                text=json.dumps(weather_data, indent=2)
            )
        ]
    except Exception as e:
        logger.error(f"Weather API error: {str(e)}")
        raise RuntimeError(f"Weather API error: {str(e)}")
```

This implementation shows several important patterns:

1. **Input Validation**: We verify that we received a valid tool name and the required arguments.
2. **Error Handling**: We wrap our core logic in try/except blocks and provide meaningful error messages.
3. **Data Transformation**: We convert our internal data format into a consistent, well-structured response.
4. **Logging**: We log important events and errors to aid in debugging.

## Managing Communication

MCP servers communicate via STDIO, and we need to set this up properly:

```python
async def run(self):
    from mcp.server.stdio import stdio_server

    logger.debug("Starting STDIO Weather Server")
    async with stdio_server() as (read_stream, write_stream):
        init_options = self.app.create_initialization_options()
        await self.app.run(
            read_stream,
            write_stream,
            init_options
        )
```

This code establishes the communication channels that allow your server to talk with AI models. The `async with` context manager ensures proper cleanup of resources.

## Entry Points and CLI

To make our server runnable, we need to set up proper entry points:

```python
async def main():
    logger.debug("Starting main")
    server = WeatherServer()
    await server.run()

def cli_main():
    """Non-async entry point for command line."""
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()
```

This setup provides flexibility in how the server can be started, whether as a module or a direct script.

## Extending Your Server

When you want to add new capabilities to your server, follow these steps:

1. Define the new tool in `list_tools()`
2. Implement the tool logic in `call_tool()`
3. Add appropriate error handling and logging
4. Test the new functionality

For example, adding a new tool for historical weather data might look like:

```python
# In list_tools():
Tool(
    name="get_historical_weather",
    description="Get historical weather data for a location",
    inputSchema={
        "type": "object",
        "properties": {
            "location_name": {"type": "string"},
            "date": {"type": "string", "format": "date"}
        },
        "required": ["location_name", "date"]
    }
)

# In call_tool():
if name == "get_historical_weather":
    location = arguments["location_name"]
    date = arguments["date"]
    historical_data = await Weather().get_historical(location, date)
    return [TextContent(text=json.dumps(historical_data))]
```

## Best Practices

Throughout your implementation, keep these principles in mind:

1. **Consistent Error Handling**: Always provide clear error messages that help diagnose issues.
2. **Comprehensive Logging**: Log important events, errors, and state changes.
3. **Input Validation**: Validate all inputs before processing.
4. **Clean Code Structure**: Keep your code organized and well-documented.
5. **Resource Management**: Properly manage any external resources or connections.

## Next Steps

Now that you understand the implementation details:

1. Try adding a new tool to the server
2. Implement more complex data transformations
3. Add additional error handling and edge cases
4. Explore the [Integration Guide](integration.md) to connect your server with AI platforms

Remember: The implementation shown here is a foundation. As you build more complex MCP servers, you'll discover additional patterns and requirements, but these core concepts will remain the same.