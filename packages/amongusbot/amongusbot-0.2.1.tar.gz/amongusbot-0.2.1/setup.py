# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amongusbot']

package_data = \
{'': ['*']}

install_requires = \
['discord.py>=1.4.1,<2.0.0', 'keyboard>=0.13.5,<0.14.0']

setup_kwargs = {
    'name': 'amongusbot',
    'version': '0.2.1',
    'description': 'Bot for mass-muting users in a Discord channel whenever a hotkey is pressed.',
    'long_description': '# AmongUsBot\n\nShitty (but lightweight) bot that toggles server muting of all members in a specific user\'s voice channel when a hotkey is pressed. Uses the [`keyboard`](https://pypi.org/project/keyboard/) module to listen for keypresses. \n\nIf you are looking for the project with the same very original name that uses Tesseract and Selenium go here: https://github.com/alpharaoh/AmongUsBot\n\n## Installation\n\n### Clone the Repository and Install with [Poetry](https://python-poetry.org/) (preferred)\n\n```bash\ngit clone https://github.com/PederHA/AmongUsBot.git\ncd amongusbot\npoetry install\n```\n\n### Install with pip (alternative)\n\n```bash\npip install https://github.com/PederHA/AmongUsBot/releases/download/0.2.1/amongusbot-0.2.1.tar.gz\n```\n\nNOTE: The version on PyPi does not include sound alerts and example run file! Download those files manually and place them in your project root if you choose to use pip.\n\n## Running\n\n### Create a Bot User\n\nGo to https://discord.com/developers/applications and create a new application, then add a bot user to the application by clicking on the "Bot" tab on the left-hand side of the page.\n\n### Invite the Bot to Your Server\n\nInvite the bot with the following URL (substitute with your bot\'s ID):\n`https://discord.com/oauth2/authorize?client_id=<BOT_CLIENT_ID>&scope=bot&permissions=12651520`\n\n### Run the Bot\n\nSee `run_example.py`.\n\nAdd the bot\'s secret token as an environment variable named `AUBOT_TOKEN` or pass it in as the first argument to the application when running it.\n\n### Configuration\n\n`amongusbot/config.py` defines the following configuration options:\n\n```python\n@dataclass\nclass Config:\n    user_id: int                            # ID of user to mute voice channel of\n    hotkey: str = "|"                       # Trigger hotkey\n    log_channel_id: Optional[int] = None    # Log channel ID\n    poll_rate: float = 0.05                 # Keyboard polling rate (seconds)\n    command_prefix: str = "-"               # Command prefix\n    doubleclick: bool = False               # Require double-click of hotkey to trigger\n    doubleclick_window: float = 0.5         # Double-click activation window (seconds)\n    cooldown: float = 2.0                   # Trigger cooldown\n    sound: bool = False                     # Play sound when triggered\n    mute_sound: str = "audio/muted.wav"     # Mute sound\n    unmute_sound: str = "audio/unmuted.wav" # Unmute sound\n```\n\nDefaults can be overridden when running the bot:\n\n```python\nfrom amongusbot import run, Config\n\nrun("your_token", Config(user_id=123456, hotkey="f4"))\n```\n\n## Usage\n\nPress the hotkey whenever a round starts to mute everyone in your channel, and press it again whenever a meeting is convened or the game ends.\n\n## Notes\n\nOnly tested on Windows.',
    'author': 'PederHA',
    'author_email': 'peder.andresen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PederHA/amongusbot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
