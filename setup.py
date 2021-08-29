from pkg_resources import parse_requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='foxhole-nospotterarty',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    py_modules=[
        'main',
    ],
    install_requires=['pygubu', 'tk', 'pillow']
)