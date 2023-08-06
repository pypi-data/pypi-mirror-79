from setuptools import setup

setup(
    name='DiscordMC',
    version='0.0.1',
    packages=['discordmc'],
    url='',
    license='GNU LIcense',
    author='Pixymon',
    author_email='nlarsen23.student@gmail.com',
    description='Access to your Minecraft Server through discord.',
    install_requires=['click', 'discord', 'mcserverapi'],
    entry_points={
        'console_scripts': ['discordmc=discordmc.cli:cli'],
    }
)
