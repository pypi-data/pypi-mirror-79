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
    'version': '0.1.3',
    'description': 'The Minecraft pack development kit',
    'long_description': '# <img src="https://github.com/vberlier/beet/blob/master/docs/assets/logo.svg" alt="beet logo" width="30"> beet\n\n[![Build Status](https://travis-ci.com/vberlier/beet.svg?token=HSyYhdxSKy5kTTrkmWq7&branch=master)](https://travis-ci.com/vberlier/beet)\n[![PyPI](https://img.shields.io/pypi/v/beet.svg)](https://pypi.org/project/beet/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/beet.svg)](https://pypi.org/project/beet/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n> The Minecraft pack development kit.\n\n## Introduction\n\nAs Minecraft\'s vanilla customization capabilities keep growing, it\'s becoming more and more apparent that [resource packs](https://minecraft.gamepedia.com/Resource_Pack) and [data packs](https://minecraft.gamepedia.com/Data_Pack) can be pretty limiting as an _authoring_ format. Their simple structure allows them to fulfill their initial objective as a _distribution_ format, but without the ability to parametrize or create abstractions over assets and data pack resources, the reusability and interoperability of community-created projects and libraries is greatly limited.\n\nThe community is tackling the problem by building independent tooling left and right, from command pre-processors to frameworks of all kinds and full-blown programming languages. However, there\'s no silver bullet and in situations where a combination of these tools could actually provide the most suited abstractions, the separate toolchains and the poor interoperability make it difficult for them to coexist.\n\nThe `beet` project is meant to serve as a platform for building interoperable higher-level frameworks by providing a flexible composition model and a unified, user-friendly development workflow.\n\n### Library\n\n> [Documentation]()\n\n```python\nfrom beet import ResourcePack, Texture\n\nwith ResourcePack(path="stone.zip") as assets:\n    assets["minecraft:block/stone"] = Texture(source_path="custom.png")\n```\n\nThe `beet` library provides carefully crafted abstractions for working with Minecraft resource packs and data packs in Python.\n\n- Create, read, edit and merge resource packs and data packs\n- Handle zipped and unzipped packs\n- Fast and lazy by default, files are transparently loaded when needed\n- Statically typed API enabling rich intellisense and autocompletion\n\n### Toolchain\n\n> [Documentation]()\n\n```python\nfrom beet import Context, Function\n\ndef greet(ctx: Context):\n    ctx.data["greet:hello"] = Function(["say hello"], tags=["minecraft:load"])\n```\n\nThe `beet` toolchain makes it easy to create configurable resource packs and data packs by composing pack generators.\n\n- Write simple functions that can edit or inspect the generated resource pack and data pack\n- Cache expensive computations and heavy files with a versatile caching API\n- Automatically rebuild the project on file changes with watch mode\n- Link the project to Minecraft to synchronize the generated resource pack and data pack\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\n$ pip install beet\n```\n\nYou can make sure that `beet` was successfully installed by trying to use the toolchain from the command-line.\n\n```bash\n$ beet --help\nUsage: beet [OPTIONS] COMMAND [ARGS]...\n\n  The beet toolchain.\n\nOptions:\n  -C, --directory DIRECTORY  The project directory.\n  --version                  Show the version and exit.\n  --help                     Show this message and exit.\n\nCommands:\n  build  Build the current project.\n  cache  Inspect or clear the cache.\n  init   Initialize a new project.\n  link   Link the generated resource pack and data pack to Minecraft.\n  watch  Watch the project directory and rebuild on file changes.\n```\n\n## Contributing\n\nContributions are welcome. This project uses [`poetry`](https://python-poetry.org).\n\n```bash\n$ poetry install\n```\n\nYou can run the tests with `poetry run pytest`. We use [`pytest-minecraft`](https://github.com/vberlier/pytest-minecraft) to run tests against actual Minecraft releases.\n\n```bash\n$ poetry run pytest\n$ poetry run pytest --minecraft-latest\n```\n\nThe project must type-check with [`mypy`](http://mypy-lang.org) and [`pylint`](https://www.pylint.org) shouldn\'t report any error.\n\n```bash\n$ poetry run mypy\n$ poetry run pylint beet tests\n```\n\nThe code follows the [`black`](https://github.com/psf/black) code style.\n\n```bash\n$ poetry run black beet tests\n$ poetry run black --check beet tests\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/beet/blob/master/LICENSE)\n',
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
