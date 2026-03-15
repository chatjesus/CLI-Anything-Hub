from setuptools import setup
setup(
    name="cli-anything-salesforce", version="1.0.0",
    description="Salesforce REST API CLI for SOQL and records",
    author="AgentPuter", url="https://www.agentputer.com/cli-anything",
    py_modules=["salesforce_cli"],
    install_requires=["click>=8.0"],
    entry_points={"console_scripts": ["salesforce-cli=salesforce_cli:cli"]},
    python_requires=">=3.9",
)