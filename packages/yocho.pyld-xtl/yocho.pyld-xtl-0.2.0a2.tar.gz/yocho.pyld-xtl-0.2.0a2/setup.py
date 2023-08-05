# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yocho', 'yocho.pyld_xtl']

package_data = \
{'': ['*']}

install_requires = \
['pyld>=2.0.3,<3.0.0', 'pyyaml>=5.3.1,<6.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['pyld-xtl = yocho.pyld_xtl.cli:main']}

setup_kwargs = {
    'name': 'yocho.pyld-xtl',
    'version': '0.2.0a2',
    'description': 'Extra tools for pyld',
    'long_description': '# Extra command line tools for pyld\n\nTODO\n\nUsage examples:\n\n```bash\n# Install pipx\npip3 install --user --upgrade pipx\n\n# (optionally) clear pipx cache if you want the latest version ...\n\\rm -vr ~/.local/pipx/.cache/\n\n# check version\npipx run --spec yocho.pyld-xtl pyld-xtl --version\n```\n',
    'author': 'Iwan Aucamp',
    'author_email': 'aucampia@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/aucampia/wip/pyld-xtl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
