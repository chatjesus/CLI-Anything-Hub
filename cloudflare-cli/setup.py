from setuptools import setup

setup(
    name="cli-anything-cloudflare",
    version="1.0.0",
    description="Cloudflare DNS & Workers API CLI - part of CLI Anything Hub",
    long_description=open("README.md", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "Cloudflare DNS & Workers API CLI wrapper for AI agents.",
    long_description_content_type="text/markdown",
    author="AgentPuter",
    author_email="hello@agentputer.com",
    url="https://www.agentputer.com/cli-anything",
    project_urls={
        "GitHub": "https://github.com/chatjesus/CLI-Anything-Hub",
        "Hub": "https://www.agentputer.com/cli-anything",
    },
    py_modules=["cloudflare_cli"],
    install_requires=['click>=8.0'],
    entry_points={
        "console_scripts": [
            "cli-anything-cloudflare=cloudflare_cli:cli",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
)
