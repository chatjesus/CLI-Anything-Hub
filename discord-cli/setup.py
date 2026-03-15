from setuptools import setup
setup(
    name="cli-anything-discord", version="1.0.0",
    description="Discord Bot API CLI for cli-anything engine",
    author="AgentPuter", url="https://www.agentputer.com/cli-anything",
    py_modules=["discord_cli"],
    install_requires=["click>=8.0"],
    entry_points={"console_scripts": ["discord-cli=discord_cli:cli"]},
    python_requires=">=3.9",
)