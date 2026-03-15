from setuptools import setup
setup(
    name="cli-anything-telegram", version="1.0.0",
    description="Telegram Bot API CLI for cli-anything engine",
    author="AgentPuter", url="https://www.agentputer.com/cli-anything",
    py_modules=["telegram_cli"],
    install_requires=["click>=8.0"],
    entry_points={"console_scripts": ["telegram-cli=telegram_cli:cli"]},
    python_requires=">=3.9",
)