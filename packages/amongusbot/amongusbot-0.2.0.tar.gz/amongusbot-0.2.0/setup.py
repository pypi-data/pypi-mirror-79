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
    'version': '0.2.0',
    'description': 'Bot for mass-muting users in a Discord channel whenever a hotkey is pressed.',
    'long_description': '# AmongUsBot\n\nShitty bot that toggles server muting of all members in a specific user\'s voice channel when a hotkey is pressed. Uses the [`keyboard`](https://pypi.org/project/keyboard/) module to listen for keypresses.\n\n## Installation\n\nClone the repository and install with [Poetry](https://python-poetry.org/):\n\n```bash\ngit clone https://github.com/PederHA/AmongUsBot.git\ncd amongusbot\npoetry install\n```\n\nAlternatively:\n\n```bash\npip install https://github.com/PederHA/AmongUsBot/releases/download/0.2.0/amongusbot-0.2.0.tar.gz\n```\n\n## Usage\n\nPress the hotkey whenever a round starts to mute everyone in your channel, and press it again whenever a meeting is convened or the game ends.\n\n### Configuration\n\n`amongusbot/config.py` defines the following configuration options:\n\n```python\n@dataclass\nclass Config:\n    user_id: int                            # Discord ID of user\'s channel to mute\n    hotkey: str = "|"                       # Trigger hotkey\n    log_channel_id: Optional[int] = None    # Log channel ID\n    poll_rate: float = 0.05                 # Keyboard polling rate (seconds)\n    command_prefix: str = "-"               # Command prefix\n    doubleclick: bool = False               # Require double-click of hotkey to trigger\n    doubleclick_window: float = 0.5         # Double-click activation window (seconds)\n    cooldown: float = 2.0                   # Trigger cooldown\n    sound: bool = True                      # Play sound when triggered\n    mute_sound: str = "audio/muted.wav"     # Mute sound\n    unmute_sound: str = "audio/unmuted.wav" # Unmute sound\n```\n\nDefaults can be overriden when running the bot:\n\n```python\nfrom amongusbot import run, Config\n\nrun("your_token", Config(user_id=123456, hotkey="f4"))\n```\n\n### Running\n\nSee `run_example.py`.\n\nWhen inviting the bot to your server, use the following permissions integer: `12962880`\n\n## Notes\n\nOnly tested on Windows.',
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
