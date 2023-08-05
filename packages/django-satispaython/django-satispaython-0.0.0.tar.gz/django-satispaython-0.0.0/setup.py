# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_satispaython',
 'django_satispaython.migrations',
 'django_satispaython.templatetags']

package_data = \
{'': ['*'], 'django_satispaython': ['templates/django_satispaython/*']}

install_requires = \
['django>=3,<4', 'satispaython']

setup_kwargs = {
    'name': 'django-satispaython',
    'version': '0.0.0',
    'description': 'A simple django app to manage Satispay payments following the Web-button flow.',
    'long_description': '# django-satispaython',
    'author': 'Daniele Pira',
    'author_email': 'daniele.pira@otto.to.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/otto-torino/django-satispaython',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
