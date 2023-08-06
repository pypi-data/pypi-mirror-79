# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beet']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.2.0,<8.0.0',
 'click-help-colors>=0.8,<0.9',
 'click>=7.1.2,<8.0.0',
 'nbtlib>=1.8.0,<2.0.0',
 'pathspec>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['beet = beet.cli:main']}

setup_kwargs = {
    'name': 'beet',
    'version': '0.1.2',
    'description': 'The Minecraft pack development kit',
    'long_description': '# <img src="https://github.com/vberlier/beet/blob/master/docs/assets/logo.svg" alt="beet logo" width="30"> beet\n\n[![Build Status](https://travis-ci.com/vberlier/beet.svg?token=HSyYhdxSKy5kTTrkmWq7&branch=master)](https://travis-ci.com/vberlier/beet)\n[![PyPI](https://img.shields.io/pypi/v/beet.svg)](https://pypi.org/project/beet/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/beet.svg)](https://pypi.org/project/beet/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n> The Minecraft pack development kit.\n\n## Introduction\n\nOver the years, Minecraft [resource packs](https://minecraft.gamepedia.com/Resource_Pack) and [data packs](https://minecraft.gamepedia.com/Data_Pack) evolved into really powerful tools that anyone can use to customize the vanilla experience. It\'s now possible to implement almost any game mechanic imaginable using a resource pack and a data pack.\n\nWith the growing number of capabilities, there\'s been a matching drive from the community when it comes to establishing interoperability standards and developing reusable data pack libraries. As the community tries to create more and more things with these capabilities, it\'s becoming more and more apparent that resource packs and data packs aren\'t really suited as an _authoring_ format. They\'re simple and straight-forward to parse, which means that they fulfill their initial objective as a _distribution_ format, but they weren\'t created with a specific developer experience in mind.\n\nMany people started tackling the problem by building tools, from command pre-processors to full-blown programming languages and all kinds of frameworks, but none of these solutions could really talk to each other. Depending on the situation, some tools would provide more suitable abstractions than others, but most of them would be difficult to use together. Another problem is that by focusing on the abstractions, some of these tools either left out crucial quality-of-life features or each had to re-implement very similar development workflows.\n\nThe `beet` project is meant to serve as a platform for building interoperable higher-level frameworks by providing low-level abstractions, a composition model and a unified development workflow.\n\n### Features\n\n- The `beet` library provides carefully crafted abstractions for working with Minecraft resource packs and data packs in Python.\n\n  ```python\n  from beet import ResourcePack, Texture\n\n  with ResourcePack(path="stone.zip") as assets:\n      assets["minecraft:block/stone"] = Texture(source_path="custom.png")\n  ```\n\n  - Create, read, edit and merge resource packs and data packs\n  - Handle zipped and unzipped packs\n  - Fast and lazy by default, files are transparently loaded when accessing their content\n  - Statically typed API enabling rich intellisense and autocompletion\n\n- The `beet` toolchain makes it easy to create configurable resource packs and data packs by composing pack generators.\n\n  ```python\n  from beet import Context, Function\n\n  def greet(ctx: Context):\n      ctx.data["greet:hello"] = Function(["say hello"], tags=["minecraft:load"])\n  ```\n\n  - Generators are simple functions that can edit or inspect the generated resource pack and data pack\n  - Watch mode for building the project on file changes\n  - Link the project to Minecraft to automatically synchronize the generated resource pack and data pack\n  - Versatile caching API to prevent repeating expensive computations\n  - Simple use-cases like merging packs are built into the prelude and don\'t require any code\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\n$ pip install beet\n```\n\nYou can make sure that `beet` was successfully installed by trying to use the toolchain from the command-line.\n\n```bash\n$ beet --version\n```\n\n## Documentation\n\nThe project documentation is available at https://vberlier.github.io/beet/.\n\n### Library\n\n- [Getting Started]()\n- [Resource packs]()\n- [Data packs]()\n- [Generic file types]()\n- [Generic packs and namespaces]()\n\n### Toolchain\n\n- [Getting Started]()\n- [Writing generators]()\n- [Command-line interface]()\n- [Configuration]()\n- [The beet prelude]()\n- [Using the cache]()\n\n## Contributing\n\nContributions are welcome. This project uses [`poetry`](https://python-poetry.org).\n\n```bash\n$ poetry install\n```\n\nYou can run the tests with `poetry run pytest`. We use [`pytest-minecraft`](https://github.com/vberlier/pytest-minecraft) to run tests against actual Minecraft releases.\n\n```bash\n$ poetry run pytest\n$ poetry run pytest --minecraft-latest\n```\n\nThe project must type-check with [`mypy`](http://mypy-lang.org) and [`pylint`](https://www.pylint.org) shouldn\'t report any error.\n\n```bash\n$ poetry run mypy\n$ poetry run pylint beet tests\n```\n\nThe code follows the [`black`](https://github.com/psf/black) code style.\n\n```bash\n$ poetry run black beet tests\n$ poetry run black --check beet tests\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/beet/blob/master/LICENSE)\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vberlier/beet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
