from setuptools import setup, find_packages

setup(
    name="cli-anything-ms365",
    version="1.0.0",
    description="Microsoft 365 CLI — COM automation for Word / Excel / PowerPoint / Outlook",
    py_modules=["ms365_cli"],
    install_requires=[
        "click>=8.0",
        "pywin32>=306",
        "python-pptx>=0.6.21",
        "openpyxl>=3.1",
    ],
    entry_points={
        "console_scripts": [
            "ms365-cli=ms365_cli:cli",
        ],
    },
    python_requires=">=3.9",
)
