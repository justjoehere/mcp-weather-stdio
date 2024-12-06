# Installation and Running Your MCP Server

This guide explores different ways to install and run your MCP server, using our weather service as an example. We'll cover the pros and cons of each approach and when to use them.

## Understanding Python Package Management

Before diving into installation methods, let's understand why we offer different approaches. Python package management can be complex, especially when dealing with dependencies and different environments. We'll explore two main methods: using UV (our recommended approach) and traditional pip installation.

## Method 1: Using UV (Recommended)

UV is a modern Python package installer that offers better dependency resolution and isolation. Here's why we recommend it:

### Installation
```bash
uv pip install -e .
```

### Running
```bash
uv --directory path/to/project run mcp_weather_service_stdio
```

### Why UV?

1. **Better Dependency Management**: UV handles dependencies more efficiently and predictably.
2. **Development Mode**: The `-e` flag installs in "editable" mode, perfect for development.
3. **Isolation**: UV provides better isolation from your system Python environment.

### Integration Configuration

When using UV with Claude Desktop:
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

## Method 2: Global Installation

While not recommended for development, global installation might be suitable for end users or simple deployments.

### Installation
```bash
python -m pip install .
```

### Running
```bash
python -m mcp_weather_service_stdio
```

### Integration Configuration

With global installation, Claude Desktop configuration is simpler:
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

## Understanding Entry Points

Our `setup.py` defines how the package can be run:

```python
setup(
    # ... other configuration ...
    entry_points={
        'console_scripts': [
            'mcp_weather_service_stdio=mcp_weather_service_stdio.weather_server:cli_main',
        ],
    }
)
```

This creates a command-line entry point that enables:
1. Running as a module: `python -m mcp_weather_service_stdio`
2. Running directly: `mcp_weather_service_stdio`
3. Running with UV: `uv run mcp_weather_service_stdio`

## Special Considerations for Gradio Integration

When integrating with Gradio MCP Client, we need to handle STDIO differently. Here's why:
Working Directory Issue:

### Gradio spawns processes from its own working directory ###
- When using UV with a local package, the working directory matters because UV needs to find the package and its dependencies
- Without changing the working directory, UV would try to run the package from Gradio's directory and fail

### Environment Resolution ###
- UV needs to correctly resolve the package and its environment
- When running directly from Gradio's config, UV would try to use Gradio's environment context
- This could lead to dependency conflicts or missing package issues

### Process Isolation ###
- The batch file creates a clean process context
- By explicitly setting the working directory (cd /d path/to/project), we ensure UV runs in the correct package context
- This prevents cross-contamination with Gradio's own Python environment

### Design Notes ###
- You could technically avoid the batch file if you
- Install the package globally (not recommended)
- Use full absolute paths in the UV command
- Handle environment variables differently

But the batch file approach is cleaner because it
- Maintains proper package isolation
- Ensures consistent environment setup
- Makes configuration more maintainable
- Avoids potential path and environment issues

### UV Method (Recommended)

Create a batch file to handle the environment setup:
```batch
@echo off
cd /d C:\path\to\project\src\mcp_weather_service_stdio
uv run mcp_weather_service_stdio
```

Configure in Gradio:
```json
{
  "mcpServers": {
    "stdio_weather": {
      "type": "stdio",
      "command": "path\\to\\your\\bat\\file\\uv-run-weather.bat"
    }
  }
}
```

### Global Installation Method

Direct configuration in Gradio is easier to setup:
```json
{
  "mcpServers": {
    "weather": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp_weather_service_stdio"]
    }
  }
}
```

## Development Workflow

Here's our recommended development workflow:

1. **Initial Setup**
   ```bash
   git clone <repository>
   cd <repository>
   uv pip install -e .
   ```

2. **Testing Changes**
   ```bash
   npx @modelcontextprotocol/inspector uv --directory . run mcp_weather_service_stdio
   ```

3. **Integration Testing**
   Configure Claude Desktop or Gradio as shown above and test with real AI interactions.

## Troubleshooting Common Issues

### Path Issues
If you encounter "command not found" errors:
1. Check your Python environment activation
2. Verify the installation path
3. Ensure entry points are properly configured

### STDIO Communication
If the server isn't communicating:
1. Check if the process has proper access to STDIN/STDOUT
2. Verify no other processes are capturing the streams
3. Enable debug logging for more information

### Dependency Conflicts
If you encounter dependency issues:
1. Try UV's dependency resolution
2. Check for conflicting packages
3. Consider creating a fresh virtual environment

## Next Steps

Once you have your server running:
1. Explore the [Integration Guide](integration.md) for connecting with AI platforms
2. Check the [Implementation Guide](implementation.md) for adding features
3. Consider containerization for deployment

Remember: The installation method you choose should align with your use case. UV is great for development, while global installation might be better for simple deployments.