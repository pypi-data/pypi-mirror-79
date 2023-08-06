from setuptools import setup

setup(
    name='DiscordMC',
    version='0.0.5',
    packages=['discordmc'],
    license='GNU LIcense',
    author='Pixymon',
    author_email='nlarsen23.student@gmail.com',
    description='Access to your Minecraft Server through discord.',
    install_requires=['click', 'discord', 'mcserverapi']
)
