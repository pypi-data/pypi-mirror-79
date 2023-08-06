from setuptools import setup, find_packages

setup(
    name="inoftvocal",
    version="0.90.5.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["PyYAML", "pydantic", "boto3", "click", "inflect", "discord.py"],
    entry_points={
        "console_scripts": [
            "inoft = inoft_vocal_framework.cli.cli_index:cli",
            "inoftvocal = inoft_vocal_framework.cli.cli_index:cli",
        ],
    },
    url="https://github.com/Robinson04/inoft_vocal_framework",
    license="MIT",
    author="Inoft",
    author_email="robinson@inoft.com",
    description="Create advanced cross-platform skills for Alexa, Google Assistant and Samsung Bixby",
)

