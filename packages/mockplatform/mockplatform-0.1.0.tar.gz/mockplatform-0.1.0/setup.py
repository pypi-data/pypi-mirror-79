from setuptools import setup, find_packages

packages = find_packages()

setup_kwargs = {
    'name': 'mockplatform',
    'version': '0.1.0',
    'url': 'https://github.com/jakewan/mockplatform',
    'author': 'Jacob Wan',
    'author_email': 'jacobwan840@gmail.com',
    'packages': packages,
    'install_requires': [
        'sanic'
    ],
    'extras_require': {
        'dev': [
            'pycodestyle',
            'autopep8',
            'pytest'
        ]
    },
    'entry_points': {
        'console_scripts': [
            'mockplatform = mockplatform.app:run'
        ]
    },
    'include_package_data': True,
    'python_requires': '>=3.7.3',
}

setup(**setup_kwargs)
