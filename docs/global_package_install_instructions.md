# Global Install - NOT PREFERRABLE
- Run this command from the project root `python -m pip install .`
- Then you can run the inspector to test it out `npx @modelcontextprotocol/inspector python -m mcp_weather_service_stdio`
- To Uninstall run `pip uninstall mcp_weather_service_stdio`
- To run the server with claude desktop
```json

{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": [
        "-m",
        "mcp_weather_service_stdio"
      ]
    }
  }
}
```
- To run this with the Gradio MCP Client Config
If you're using [Gradio MCP Client](https://github.com/justjoehere/mcp_gradio_client) you'll need this config
```json

{
  "mcpServers": {
    "weather": {
      "type": "stdio",
      "command": "python",
      "args": [
        "-m",
        "mcp_weather_service_stdio"
      ]
    }
  }
}

```