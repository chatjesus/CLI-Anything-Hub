from setuptools import setup, find_packages

setup(
    name="cli-anything-hub",
    version="1.0.0",
    description="Shared auth, subscription & Pro gating for all CLI-Anything tools. One login unlocks 160+ agent-ready CLIs.",
    long_description=open("README.md", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="AgentPuter",
    author_email="hello@agentputer.com",
    url="https://agentputer.com/cli-anything",
    project_urls={
        "Documentation": "https://agentputer.com/cli-anything/docs.html",
        "GitHub": "https://github.com/chatjesus/CLI-Anything-Hub",
        "Pricing": "https://agentputer.com/cli-anything/pricing",
    },
    packages=find_packages(),
    install_requires=["click>=8.0"],
    entry_points={
        "console_scripts": [
            "cli-anything=cli_anything_hub.cli:cli",
        ],
    },
    python_requires=">=3.9",
    keywords=[
        "cli-anything", "agent-native", "subscription", "stripe",
        "ai-agent", "llm-tools", "hub", "authentication",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
)
