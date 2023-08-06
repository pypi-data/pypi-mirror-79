
import re 
from os import path

from setuptools import setup
from codecs import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def read(*parts):
    return open(path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^version = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='discord-notifier',
    version=find_version('discordnotifier','__init__.py'),
    description='Simple discord notification bot',
    long_description=long_description,
    long_description_content_type="text/markdown",

    # The project's main homepage.
    url='https://github.com/josephbmanley/discord-notifier',

    # Author details
    author='Joseph Manley',
    author_email='j@cloudsumu.com',

    # Choose your license
    license='MIT',

    # See https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords='AWS,Discord,Cloud,Notification',
    packages=["discordnotifier"],
    install_requires=['boto3','discord.py'],
    package_data={},
    entry_points={
        'console_scripts' : [
            'discordnotifier = discordnotifier:main'
        ]
    }
)
