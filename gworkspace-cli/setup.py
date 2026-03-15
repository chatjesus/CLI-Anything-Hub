from setuptools import setup
setup(
    name="cli-anything-gworkspace",
    version="1.0.0",
    description="Google Workspace CLI for cli-anything engine (Drive/Gmail/Calendar/Sheets/Docs/Chat)",
    author="AgentPuter",
    url="https://www.agentputer.com/cli-anything/gworkspace/",
    py_modules=["gworkspace_cli"],
    install_requires=[
        "click>=8.0",
        "google-auth>=2.0",
        "google-auth-oauthlib>=1.0",
    ],
    extras_require={
        "full": ["google-api-python-client>=2.0"],
    },
    entry_points={
        "console_scripts": ["gworkspace-cli=gworkspace_cli:cli"],
    },
    python_requires=">=3.9",
)
