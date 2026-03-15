from setuptools import setup
setup(
    name="cli-anything-slack", version="1.0.0",
    description="Slack Web API CLI for cli-anything engine",
    author="AgentPuter", url="https://www.agentputer.com/cli-anything",
    py_modules=["slack_cli"],
    install_requires=["click>=8.0", "slack-sdk>=3.0"],
    entry_points={"console_scripts": ["slack-cli=slack_cli:cli"]},
    python_requires=">=3.9",
)