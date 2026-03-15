from setuptools import setup
setup(
    name="cli-anything-shopify", version="1.0.0",
    description="Shopify Admin REST API CLI",
    author="AgentPuter", url="https://www.agentputer.com/cli-anything",
    py_modules=["shopify_cli"],
    install_requires=["click>=8.0"],
    entry_points={"console_scripts": ["shopify-cli=shopify_cli:cli"]},
    python_requires=">=3.9",
)