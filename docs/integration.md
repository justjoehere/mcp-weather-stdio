# Integration Guide: Connecting Your MCP Server

This guide explores how to integrate your MCP server with various AI platforms and tools. We'll use our weather service example to demonstrate different integration patterns and help you understand the communication flow between your server and AI models.

## Understanding MCP Communication

Before diving into specific integrations, let's understand how MCP servers communicate with AI platforms. The Model Context Protocol uses a standard message format over STDIO (Standard Input/Output), which means your server can integrate with any platform that supports this protocol.

## The Communication Flow

Here's what happens when an AI model uses your MCP server:

1. **Initialization**: The AI platform starts your server as a subprocess
2. **Tool Discovery**: The AI requests a list of available tools
3. **Tool Selection**: The AI chooses a tool based on its needs
4. **Execution**: Your server processes the request and returns results
5. **Interpretation**: The AI processes the results and continues its task

Let's look at how this plays out in different integration scenarios.

## Integrating with Claude Desktop

Claude Desktop provides a straightforward way to integrate MCP servers. Let's explore both recommended approaches:

### Using UV (Recommended)

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

This configuration tells Claude Desktop to:
1. Use UV to manage the Python environment
2. Find your server in the specified directory
3. Run it using the proper entry point

### Using Global Installation

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

This simpler configuration works when your server is installed globally, but offers less isolation.

## Integrating with Gradio MCP Client

Gradio requires special handling due to its STDIO management. Let's understand why and how to handle it:

### The STDIO Challenge

Gradio's handling of STDIO requires us to wrap our server in a batch file. This ensures proper stream handling and environment setup. Here's how we do it:

### UV Integration (Recommended)

1. Create a wrapper batch file (`uv-run-weather.bat`):
```batch
@echo off
cd /d C:\path\to\project\src\mcp_weather_service_stdio
uv run mcp_weather_service_stdio
```

2. Configure Gradio:
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

### Understanding the Integration Process

Let's break down what happens when an AI model requests weather information:

1. **Starting the Server**:
   ```mermaid
   sequenceDiagram
       participant AI as AI Platform
       participant Config as Configuration
       participant Server as MCP Server
       
       AI->>Config: Read server configuration
       Config->>AI: Return command and args
       AI->>Server: Start server process
       Server->>AI: Acknowledge initialization
   ```

2. **Tool Discovery and Usage**:
   ```mermaid
   sequenceDiagram
       participant AI as AI Model
       participant Server as MCP Server
       participant Weather as Weather API
       
       AI->>Server: Request available tools
       Server->>AI: Return tool list
       AI->>Server: Call get_current_weather
       Server->>Weather: Fetch weather data
       Weather->>Server: Return data
       Server->>AI: Return formatted response
   ```

## Debugging Integration Issues

When integrating your server, you might encounter various issues. Here's how to diagnose and fix common problems:

### 1. Communication Issues

If your server isn't receiving requests:
1. Check STDIO handling in your configuration
2. Verify process permissions
3. Enable debug logging:
   ```python
   logging.basicConfig(
       level=logging.DEBUG,
       filename='mcp_server.log'
   )
   ```

### 2. Data Format Problems

If the AI platform can't understand your responses:
1. Verify your JSON formatting
2. Check content type specifications
3. Validate against the MCP schema

### 3. Environment Issues

If the server won't start:
1. Verify path configurations
2. Check Python environment setup
3. Confirm dependency installation

## Testing Your Integration

Before deploying, test your integration thoroughly:

1. **Using the MCP Inspector**:
   ```bash
   npx @modelcontextprotocol/inspector uv --directory path/to/project run mcp_weather_service_stdio
   ```

2. **Manual Testing**:
   ```python
   import subprocess
   import json
   
   # Start your server
   process = subprocess.Popen(
       ['uv', 'run', 'mcp_weather_service_stdio'],
       stdin=subprocess.PIPE,
       stdout=subprocess.PIPE
   )
   
   # Send a test request
   request = {
       "type": "tool_call",
       "tool": "get_current_weather",
       "arguments": {"location_name": "London"}
   }
   
   process.stdin.write(json.dumps(request).encode() + b'\n')
   process.stdin.flush()
   
   # Read response
   response = process.stdout.readline()
   print(json.loads(response))
   ```

## Security Considerations

When integrating your MCP server, consider these security aspects:

1. **Input Validation**: Always validate input before processing
2. **Resource Limits**: Implement timeouts and resource constraints
3. **Error Handling**: Don't expose sensitive information in error messages
4. **Authentication**: Consider adding authentication if needed

## Advanced Integration Patterns

As your server grows more complex, consider these advanced patterns:

### 1. Stateful Integration

If your server needs to maintain state:
```python
class WeatherServer:
    def __init__(self):
        self.session_cache = {}
        
    async def call_tool(self, name: str, arguments: Any):
        session_id = arguments.get('session_id')
        if session_id in self.session_cache:
            # Use cached data
```

### 2. Batch Processing

For handling multiple requests efficiently:
```python
async def call_tool(self, name: str, arguments: Any):
    if name == "batch_weather":
        locations = arguments["locations"]
        tasks = [self.get_weather(loc) for loc in locations]
        results = await asyncio.gather(*tasks)
        return [TextContent(text=json.dumps(results))]
```

## Next Steps

After setting up your integration:

1. Monitor server performance and reliability
2. Gather feedback from AI model interactions
3. Plan for scaling and improvements
4. Consider adding more sophisticated tools

Remember: Good integration requires both technical correctness and practical usability. Test thoroughly with real-world scenarios and adapt based on actual usage patterns.