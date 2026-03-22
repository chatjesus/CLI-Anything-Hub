from setuptools import setup

setup(
    name="cli-anything-bloomberg",
    version="1.0.0",
    description="Bloomberg Financial Data CLI (BLPAPI + HTTP MCP) - part of CLI Anything Hub.",
    long_description=open("README.md", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="AgentPuter",
    author_email="hello@agentputer.com",
    url="https://www.agentputer.com/cli-anything",
    project_urls={"GitHub": "https://github.com/chatjesus/CLI-Anything-Hub"},
    py_modules=["bloomberg_cli"],
    install_requires=["click>=8.0", "requests>=2.28"],
    entry_points={"console_scripts": ["cli-anything-bloomberg=bloomberg_cli:cli"]},
    python_requires=">=3.9",
    keywords=["cli", "bloomberg", "ai-agent", "agent-native", "cli-anything", "finance"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
