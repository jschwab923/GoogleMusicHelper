from setuptools import setup, find_packages
from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        print "Sup dude"


setup(
    cmdclass={
        'install': CustomInstallCommand,
    },
    name="MusicLibraryHelper",
    version="0.0.1",
    packages=find_packages(),
    author="Jeff Schwab",
    url="https://github.com/jschwab923/MusicLibraryHelper",
    description="Sync your music libraries"
)
