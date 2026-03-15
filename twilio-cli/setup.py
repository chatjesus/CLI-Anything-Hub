from setuptools import setup
setup(
    name="cli-anything-twilio", version="1.0.0",
    description="Twilio SMS Voice WhatsApp CLI",
    author="AgentPuter", url="https://www.agentputer.com/cli-anything",
    py_modules=["twilio_cli"],
    install_requires=["click>=8.0"],
    entry_points={"console_scripts": ["twilio-cli=twilio_cli:cli"]},
    python_requires=">=3.9",
)