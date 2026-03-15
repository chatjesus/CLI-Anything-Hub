from setuptools import setup
setup(
    name="cli-anything-jira", version="1.0.0",
    description="Atlassian Jira REST API CLI",
    author="AgentPuter", url="https://www.agentputer.com/cli-anything",
    py_modules=["jira_cli"],
    install_requires=["click>=8.0"],
    entry_points={"console_scripts": ["jira-cli=jira_cli:cli"]},
    python_requires=">=3.9",
)