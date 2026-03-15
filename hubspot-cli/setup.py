from setuptools import setup
setup(
    name="cli-anything-hubspot", version="1.0.0",
    description="HubSpot CRM REST API CLI",
    author="AgentPuter", url="https://www.agentputer.com/cli-anything",
    py_modules=["hubspot_cli"],
    install_requires=["click>=8.0"],
    entry_points={"console_scripts": ["hubspot-cli=hubspot_cli:cli"]},
    python_requires=">=3.9",
)