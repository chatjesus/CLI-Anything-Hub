from setuptools import setup, find_packages

setup(
    name="feishu-cli",
    version="0.1.0",
    description="飞书开放平台 CLI — 让飞书 Agent-Native",
    py_modules=["feishu_cli"],
    install_requires=["click>=8.0", "requests>=2.28"],
    entry_points={
        "console_scripts": ["feishu-cli=feishu_cli:cli"]
    },
    python_requires=">=3.8",
)
