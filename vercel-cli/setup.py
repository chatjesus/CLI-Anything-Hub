from setuptools import setup
setup(
    name="cli-anything-vercel", version="1.0.0",
    description="Vercel REST API CLI for deployments and domains",
    author="AgentPuter", url="https://www.agentputer.com/cli-anything",
    py_modules=["vercel_cli"],
    install_requires=["click>=8.0"],
    entry_points={"console_scripts": ["vercel-cli=vercel_cli:cli"]},
    python_requires=">=3.9",
)