from setuptools import setup

setup(
    name="cli-anything-notion",
    version="1.0.0",
    description="Notion REST API CLI — cli-anything engine",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="AgentPuter",
    url="https://www.agentputer.com/cli-anything",
    py_modules=["notion_cli"],
    install_requires=[
        "click>=8.0",
    ],
    entry_points={
        "console_scripts": [
            "notion-cli=notion_cli:cli",
        ],
    },
    python_requires=">=3.9",
)
