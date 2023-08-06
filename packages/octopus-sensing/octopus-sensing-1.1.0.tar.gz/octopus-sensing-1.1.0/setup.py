# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octopus_sensing',
 'octopus_sensing.common',
 'octopus_sensing.devices',
 'octopus_sensing.devices.audio',
 'octopus_sensing.devices.open_vibe',
 'octopus_sensing.devices.openbci',
 'octopus_sensing.devices.shimmer3',
 'octopus_sensing.devices.webcam',
 'octopus_sensing.questionnaire',
 'octopus_sensing.tests']

package_data = \
{'': ['*'], 'octopus_sensing': ['OpenVibe/*']}

install_requires = \
['bitstring>=3.1.7,<4.0.0',
 'bluepy>=1.3.0,<2.0.0',
 'msgpack>=1.0.0,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'pyOpenBCI>=0.13,<0.14',
 'pyaudio>=0.2.11,<0.3.0',
 'pyserial>=3.4,<4.0',
 'requests>=2.24.0,<3.0.0',
 'scipy>=1.5.2,<2.0.0',
 'sounddevice>=0.4.0,<0.5.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'octopus-sensing',
    'version': '1.1.0',
    'description': 'Library for recording data synchronously from different physiological sensors',
    'long_description': "Octopus Sensing\n===============\n\n![Travis](https://img.shields.io/travis/com/nastaran62/octopus-sensing)\n![Coveralls](https://img.shields.io/coveralls/github/nastaran62/octopus-sensing)\n![PyPI - Version](https://img.shields.io/pypi/v/octopus-sensing)\n![PyPI - License](https://img.shields.io/pypi/l/octopus-sensing)\n\nA tool to help you run scientific experiments that involve recording data synchronously from\nmultiple sources. You write steps of an experiment scenario, for example showing a stimulus and then\na questionnaire. The tool takes care of the rest.\n\nIt can collect data from multiple devices such as OpenBCI EEG headset, Shimmer sensor (GSR and PPG),\nVideo and Audio, etc. Data collection can be started and stopped synchronously across all devices.\nCollected data will be tagged with the timestamp of the start and stop of the experiment, the ID of\nthe experiment, etc.\n\nThe aim is to make the scripting interface so simple that people with minimum or no software\ndevelopment skills can define experience scenarios with no effort.\n\n#### Main features\n\n* Controls data recording from multiple sources using a simple unified interface\n* Tags an event on collected data, such as the start of an experiment, and events during the experiment, etc.\n* Can show stimuli (images and videos) and questionnaires\n* Monitoring interface that visualizes collected data in real-time\n\nGetting Started\n---------------\n\n#### requirements\n\nYou need [Python](https://python.org) installed on your computer (version 3.7 or higher). Refer to\n[this guide](https://realpython.com/installing-python/) if you need help.\n\n#### Quickstart Using init script (Linux & Mac)\n\nOctopus Sensing comes with a script that helps you quickly start a project. It uses\n[Pipenv](https://pipenv.pypa.io/) to create a [virtual\nenvironment](https://docs.python.org/3/tutorial/venv.html) in order to keep everything clean. It\nwill also create a sample application.\n\n\n```\nmkdir my-awesome-project\ncd my-awesome-project\ncurl https://raw.githubusercontent.com/nastaran62/octopus-sensing/master/init_script/init.sh\n# It's a good idea to read any script before executing it.\nsudo bash ./init.sh\nrm ./init.sh\n```\n\nThe created `main.py` file is a sample application. To run it:\n\n```\npipenv run python main.py\n```\n\nIf you don't want to use the script, you can use the following methods instead.\n\n#### Installation using Pipenv\n\nWe recommend using a package manager like [Pipenv](https://pipenv.pypa.io/) instead of globally\ninstalling Octopus Sensing using `pip` to prevent package conflicts. To do so, follow these\ncommands. (This is same as what the above script does.)\n\n```bash\nmkdir my-awesome-project\ncd my-awesome-project\n# Or replace it with your python version\npipenv --python python3.8\npipenv install octopus-sensing\n```\n\nIt installs Octopus Sensing inside the virtual environment created by Pipenv. You need to use\n`pipenv` to run your code. For example:\n\n```bash\npipenv run python main.py\n```\n\nRefer to [Pipenv website](https://pipenv.pypa.io/) for more info.\n\n#### Installation using pip\n\nYou can use `pip` to install `octopus-sensing` as simple as:\n\n```\npip3 install octopus-sensing\n```\n\n(You might need to replace `pip3` with `pip` depending on your system.)\n\nThen it can be imported like:\n\n```python\nimport octopus_sensing\n```\n\n#### Installation from source\n\nIf you want to compile it from source for development purposes or to have the un-released features,\nplease refer to [Development Guide](docs/Development.md).\n\nTutorial\n--------\n\nSee [Tutorial](docs/Tutorial.md) to learn how to use Octopus Sensing.\n\nTroubleshooting\n---------------\nIf the installation failed, and this error is in the logs:\n\n```fatal error: portaudio.h: No such file or directory```\n\nYou need to install `portaudio` package on your system. On a debian-based linux the package called\n`portaudio19-dev`.\n\nCopyright\n---------\nCopyright © 2020 Nastaran Saffaryazdi\n\nThis program is free software: you can redistribute it and/or modify it under the terms of the GNU\nGeneral Public License as published by the Free Software Foundation, either version 3 of the\nLicense, or (at your option) any later version.\n\nSee [License file](LICENSE) for full terms.\n",
    'author': 'Nastaran Saffaryazdi',
    'author_email': 'nsaffar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://octopus-sensing.nastaran-saffar.me',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
