from setuptools import setup

setup(
    name="inoftvocal",
    version="0.90.0",
    packages=["inoft_vocal_framework", "inoft_vocal_framework.cli", "inoft_vocal_framework.cli.deploy",
              "inoft_vocal_framework.utils", "inoft_vocal_framework.templates",
              "inoft_vocal_framework.templates.hello_world_1", "inoft_vocal_framework.templates.simple_adventure_game_1",
              "inoft_vocal_framework.templates.subscribe_google_user_to_notifications_group",
              "inoft_vocal_framework.speechs", "inoft_vocal_framework.databases",
              "inoft_vocal_framework.databases.dynamodb", "inoft_vocal_framework.skill_builder",
              "inoft_vocal_framework.platforms_handlers", "inoft_vocal_framework.platforms_handlers.alexa",
              "inoft_vocal_framework.platforms_handlers.alexa.response",
              "inoft_vocal_framework.platforms_handlers.alexa.audioplayer",
              "inoft_vocal_framework.platforms_handlers.simulator",
              "inoft_vocal_framework.platforms_handlers.simulator.request_samples",
              "inoft_vocal_framework.platforms_handlers.simulator.request_samples.alexa",
              "inoft_vocal_framework.platforms_handlers.simulator.request_samples.google",
              "inoft_vocal_framework.platforms_handlers.simulator.request_samples.bixby",
              "inoft_vocal_framework.platforms_handlers.dialogflow",
              "inoft_vocal_framework.platforms_handlers.samsungbixby",
              "inoft_vocal_framework.platforms_handlers.siri",
              "inoft_vocal_framework.platforms_handlers.endpoints_providers",
              "inoft_vocal_framework.tests", "inoft_vocal_framework.plugins"],
    include_package_data=True,
    install_requires=["PyYAML", "boto3", "click", "inflect", "discord.py"],
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

