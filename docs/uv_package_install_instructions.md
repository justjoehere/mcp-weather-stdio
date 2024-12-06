# Run with UV - Preferred
- Run this command from the project root `uv pip install -e .`
- Then you can run the inspector to test it out  `npx @modelcontextprotocol/inspector uv --directory path\to\project\mcp-weather-stdio run mcp_weather_service_stdio`
- To Uninstall run `uv pip uninstall mcp_weather_service_stdio`

## Configure to run with claude desktop
```json

{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "path\\to\\project\\mcp-weather-stdio",
        "run",
        "mcp_weather_service_stdio"
      ]
    }
  }
}
```
## Configure to run with the Gradio MCP Client
If you're using [Gradio MCP Client](https://github.com/justjoehere/mcp_gradio_client) you'll need to create a `.bat` file to wrap and then run it.  This is because how gradio deals with stdio, so if we have to do some magic to get things working.
- **Note** You'll need to change the path to the project in the `.bat` file.  Note the `mcp-weather-stdio\src\mcp_weather_service_stdio`
```bat
@echo off
cd /d C:\path\to\project\mcp-weather-stdio\src\mcp_weather_service_stdio
uv run mcp_weather_service_stdio
```

- I recommend you save them in the gradio client's `mcp_stdio_server_bats` folder for ease of tracking.
- Then you need to configure the Gradio MCP Client `config.json` to point to the `.bat` file
```json

{
  "mcpServers": {
    "stdio_weather": {
      "type": "stdio",
      "command": "path\\to\\your\\bat\\file\\mcp_stdio_server_bats\\uv-run-weather.bat"
    }
  }
}

```