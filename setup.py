from setuptools import setup, find_namespace_packages

setup(
    name="mcp_weather_service_stdio",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=[
        "mcp",
        # other dependencies will be installed from requirements.txt
    ],
    python_requires=">=3.10",
    entry_points={
            'console_scripts': [
                'mcp_weather_service_stdio=mcp_weather_service_stdio.weather_server:cli_main',
            ],
    }
)