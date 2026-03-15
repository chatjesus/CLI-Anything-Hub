from setuptools import setup

setup(
    name="cli-anything-github",
    version="1.0.0",
    description="GitHub REST API CLI — cli-anything engine",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="AgentPuter",
    url="https://www.agentputer.com/cli-anything",
    py_modules=["github_cli"],
    install_requires=[
        "click>=8.0",
        "PyGithub>=2.1",
    ],
    entry_points={
        "console_scripts": [
            "github-cli=github_cli:cli",
        ],
    },
    python_requires=">=3.9",
)
