#!/usr/bin/env python3
"""
setup.py for cli-anything-kdenlive

Install with: pip install -e .
Or publish to PyPI: python -m build && twine upload dist/*
"""

from setuptools import setup, find_namespace_packages

with open("cli_anything/kdenlive/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cli-anything-kdenlive",
    version="1.0.0",
    author="cli-anything contributors",
    author_email="",
    description="CLI harness for Kdenlive - Video editing and rendering via melt. Requires: melt (apt install melt). AI-agent-friendly, JSON output, works with Claude/ChatGPT/Copilot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HKUDS/CLI-Anything",
    project_urls={
        "Documentation": "https://www.agentputer.com/cli-anything/kdenlive/",
        "GitHub": "https://github.com/chatjesus/CLI-Anything-Hub",
        "Hub": "https://www.agentputer.com/cli-anything",
        "Agent Guide": "https://www.agentputer.com/cli-anything/docs.html",
    },

    packages=find_namespace_packages(include=["cli_anything.*"]),
    keywords=[
        "cli",
        "kdenlive",
        "automation",
        "ai-agent",
        "agent-native",
        "cli-anything",
        "json-output",
        "llm-tools",
        "command-line",
        "video",
    ],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video :: Non-Linear Editor",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=[
        "click>=8.0.0",
        "prompt-toolkit>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cli-anything-kdenlive=cli_anything.kdenlive.kdenlive_cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
