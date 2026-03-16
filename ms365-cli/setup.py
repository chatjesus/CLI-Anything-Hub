from setuptools import setup

setup(
    name="cli-anything-ms365",
    version="1.0.0",
    description="Microsoft 365 COM Automation CLI - part of CLI Anything Hub. AI-agent-friendly, JSON output, works with Claude/ChatGPT/Copilot",
    long_description=open("README.md", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "Microsoft 365 COM Automation CLI wrapper for AI agents.",
    long_description_content_type="text/markdown",
    author="AgentPuter",
    author_email="hello@agentputer.com",
    url="https://www.agentputer.com/cli-anything",
    project_urls={
        "Documentation": "https://www.agentputer.com/cli-anything/ms365/",
        "GitHub": "https://github.com/chatjesus/CLI-Anything-Hub",
        "Hub": "https://www.agentputer.com/cli-anything",
        "Agent Guide": "https://www.agentputer.com/cli-anything/docs.html",
    },
    py_modules=["ms365_cli"],
    install_requires=['click>=8.0', 'pywin32>=306', 'python-pptx>=0.6.21', 'openpyxl>=3.1'],
    entry_points={
        "console_scripts": [
            "cli-anything-ms365=ms365_cli:cli",
        ],
    },
    python_requires=">=3.9",
    keywords=[
        "cli",
        "ms365",
        "automation",
        "ai-agent",
        "agent-native",
        "cli-anything",
        "json-output",
        "llm-tools",
        "command-line",
        "office",
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
