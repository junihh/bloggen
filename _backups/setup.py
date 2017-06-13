from setuptools import setup

# https://python-packaging.readthedocs.io/en/latest/minimal.html
# https://github.com/pallets/flask

setup(
    name = 'Bloggen',
    version = '0.18',
    description = 'Just another python static site generator.',
    url = 'https://github.com/junihh/bloggen',
    author = 'Junior Hernández',
    author_email = 'junihh@me.com',
    license = 'GPL-3.0',
    packages = ['modules'],
    zip_safe = False,
    platforms = 'any',
    install_requires = [
        'PyYAML>=3.12',
        'mistune>=0.7.4',
        'Jinja2>=2.9.6',
        'beautifulsoup4>=4.6.0'
    ]
)
