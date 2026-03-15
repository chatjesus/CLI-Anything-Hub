from setuptools import setup
setup(
    name="cli-anything-cloudflare", version="1.0.0",
    description="Cloudflare REST API CLI for DNS and Workers",
    author="AgentPuter", url="https://www.agentputer.com/cli-anything",
    py_modules=["cloudflare_cli"],
    install_requires=["click>=8.0"],
    entry_points={"console_scripts": ["cloudflare-cli=cloudflare_cli:cli"]},
    python_requires=">=3.9",
)