from setuptools import setup

setup(
    name="cli-anything-docker",
    version="1.0.0",
    description="Docker engine CLI — cli-anything engine",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="AgentPuter",
    url="https://www.agentputer.com/cli-anything",
    py_modules=["docker_cli"],
    install_requires=[
        "click>=8.0",
        "docker>=7.0",
    ],
    entry_points={
        "console_scripts": [
            "docker-cli=docker_cli:cli",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
