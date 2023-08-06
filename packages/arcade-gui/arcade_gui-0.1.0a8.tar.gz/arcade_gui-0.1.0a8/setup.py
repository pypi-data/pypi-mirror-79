# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcade_gui']

package_data = \
{'': ['*']}

install_requires = \
['arcade>=2.3.15,<3.0.0']

setup_kwargs = {
    'name': 'arcade-gui',
    'version': '0.1.0a8',
    'description': 'Experimental components that could migrate into arcade.',
    'long_description': "[![Build Status](https://travis-ci.org/eruvanos/arcade_gui.svg?branch=master)](https://travis-ci.org/eruvanos/arcade_gui)\n\n# GUI Library for Python Arcade\n\nThis library contained a first draft of GUI components for arcade game library.\nThese components are now fully integrated into python arcade.\n\n# Experimental GUI Components\n\nStarting with the version `0.2.0` all components that are included\nin arcade will be removed.\n\nStarting with version `0.2.0` this library will\ncontain experimental components, that could move into the arcade standard. \nConsider them as alpha, so breaking changes could happen in every version update.  \n\n\n## Basic Components until version `0.1.0`\n\n#### UIView\nCentral class to manager the ui components.\nConverts `on_` callback functions into events, so that UIElements\njust have to contain one method to interact with user input.\n\n#### UIElement\nA general interface of an UI element.\n\n## Examples\n\nExamples providing an overview of features, there will be dedicated documentation soon.\n\n* [UILabel](https://github.com/eruvanos/arcade_gui/blob/master/examples/show_uilabel.py)\n* [UIButton](https://github.com/eruvanos/arcade_gui/blob/master/examples/show_uibutton.py)\n* [UIInputBox](https://github.com/eruvanos/arcade_gui/blob/master/examples/show_uiinputbox.py)\n* [Example with ID](https://github.com/eruvanos/arcade_gui/blob/master/examples/show_id_example.py)\n\n### Screenshots\n\n![Example with ID Screenshot](https://github.com/eruvanos/arcade_gui/blob/master/docs/assets/ProGramer.png)\n\n\n## Features planned to work on\n\n* [ ] Enhancements\n    * [ ] layered UI\n* [ ] Layout\n    * [ ] Modal \n        * [ ] open \n        * [ ] close \n        * [ ] colour background \n        * [ ] image background \n* [ ] New Components\n    * [ ] UITextArea\n    * [ ] Scrollbar\n\n### Chores\n\n* [ ] \n\n## Background information and other frameworks\n\n### Reference Pygame GUI projects\n\n[Overview](https://www.pygame.org/wiki/gui)\n\n* ThorPy\n    * http://www.thorpy.org/index.html\n* Phil's pyGame Utilities\n    * https://www.pygame.org/project/108\n* OcempGUI\n    * https://www.pygame.org/project/125\n* PyGVisuals\n    * https://github.com/Impelon/PyGVisuals\n* Pygame GUI\n    * [Homepage](https://github.com/MyreMylar/pygame_gui)\n    * [Examples](https://github.com/MyreMylar/pygame_gui_examples)\n    * [QuickStart Example](https://github.com/MyreMylar/pygame_gui_examples/blob/master/quick_start.py)\n    * Concept\n        * UIManager manages every interaction, new elements get the UIManager on creation\n        * Elements create events and hook into pygames event system\n        * Themes can be read from JSON files\n",
    'author': 'Maic Siemering',
    'author_email': 'maic@siemering.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eruvanos/arcade_gui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
