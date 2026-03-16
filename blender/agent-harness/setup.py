#!/usr/bin/env python3
"""
Setup script for cli-anything-blender

Install (dev mode):
    pip install -e .

Build:
    python -m build

Publish:
    twine upload dist/*
"""

from pathlib import Path
from setuptools import setup, find_namespace_packages

ROOT = Path(__file__).parent
README = ROOT / "cli_anything/blender/README.md"

long_description = README.read_text(encoding="utf-8") if README.exists() else ""

setup(
    name="cli-anything-blender",
    version="1.0.0",
    description="CLI harness for Blender - run 3D modeling, animation, and rendering via blender --background --python. AI-agent-friendly, JSON output, works with Claude/ChatGPT/Copilot",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="cli-anything contributors",
    author_email="",
    url="https://github.com/HKUDS/CLI-Anything",

    project_urls={
        "Documentation": "https://www.agentputer.com/cli-anything/blender/",
        "GitHub": "https://github.com/chatjesus/CLI-Anything-Hub",
        "Hub": "https://www.agentputer.com/cli-anything",
        "Agent Guide": "https://www.agentputer.com/cli-anything/docs.html",
    },

    license="MIT",

    packages=find_namespace_packages(include=("cli_anything.*",)),

    python_requires=">=3.10",

    install_requires=[
        "click>=8.1",
        "prompt-toolkit>=3.0",
    ],

    extras_require={
        "dev": [
            "pytest>=7",
            "pytest-cov>=4",
        ],
    },

    entry_points={
        "console_scripts": [
            "cli-anything-blender=cli_anything.blender.blender_cli:main",
        ],
    },

    include_package_data=True,
    zip_safe=False,

    keywords=[
        "cli",
        "blender",
        "3d",
        "rendering",
        "automation",
        "ai-agent",
        "agent-native",
        "cli-anything",
        "json-output",
        "llm-tools",
    ],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
