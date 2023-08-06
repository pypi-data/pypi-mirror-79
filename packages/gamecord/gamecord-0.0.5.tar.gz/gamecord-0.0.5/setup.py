from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='gamecord',
    version='0.0.5',
    description='A helper framework for making games in Discord with discord.py.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Anthony Louie',
    keywords=['Discord', 'discord.py'],
    url='https://github.com/lanthony42/GameCord',
    download_url='https://pypi.org/project/gamecord/'
)

install_requires = [
    'discord.py>=1.4.1',
    'python-dotenv'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
