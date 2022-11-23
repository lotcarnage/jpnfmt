import os
from setuptools import setup
from jpnfmt import __version__


def _read_description():
    description_file_path = os.path.join(os.path.dirname(__file__), 'document/description.md')
    with open(description_file_path, 'rt', encoding='utf-8') as description_file:
        description_text = description_file.read()
    return description_text


setup(
    name='jpnfmt',
    version=__version__,
    author='lotcarnage',
    author_email='lotcarnage@gmail.com',
    url='https://github.com/lotcarnage/jpnfmt',
    packages=['jpnfmt'],
    license='MIT',
    install_requires=['numpy'],
    python_requires='>=3.8',
    description='日本語整形モジュール',
    long_description_content_type='text/markdown',
    long_description=_read_description()
)
