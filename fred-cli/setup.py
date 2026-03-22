from setuptools import setup

setup(
    name="cli-anything-fred",
    version="1.0.0",
    description="FRED (Federal Reserve Economic Data) API CLI - part of CLI Anything Hub.",
    long_description=open("README.md", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="AgentPuter",
    author_email="hello@agentputer.com",
    url="https://www.agentputer.com/cli-anything",
    project_urls={
        "Documentation": "https://www.agentputer.com/cli-anything/fred/",
        "GitHub": "https://github.com/chatjesus/CLI-Anything-Hub",
    },
    py_modules=["fred_cli"],
    install_requires=['click>=8.0', 'requests>=2.28'],
    entry_points={"console_scripts": ["cli-anything-fred=fred_cli:cli"]},
    python_requires=">=3.9",
    keywords=["cli", "fred", "automation", "ai-agent", "agent-native", "cli-anything", "json-output", "finance", "economics", "federal-reserve"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
