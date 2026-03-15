from setuptools import setup
setup(
    name="cli-anything-stripe", version="1.0.0",
    description="Stripe Payment API CLI for cli-anything engine",
    author="AgentPuter", url="https://www.agentputer.com/cli-anything",
    py_modules=["stripe_cli"],
    install_requires=["click>=8.0", "stripe>=7.0"],
    entry_points={"console_scripts": ["stripe-cli=stripe_cli:cli"]},
    python_requires=">=3.9",
)