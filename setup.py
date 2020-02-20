import codecs
import os
import re

from setuptools import Command, find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

version = "0.0.1"
changes = os.path.join(here, "CHANGES.rst")
match = r"^#*\s*(?P<version>[0-9]+\.[0-9]+(\.[0-9]+)?)$"
with codecs.open(changes, encoding="utf-8") as changes:
    for line in changes:
        res = re.match(match, line)
        if res:
            version = res.group("version")
            break


# Get the long description
with codecs.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

# Get requirements.txt
with codecs.open(os.path.join(here, "requirements.txt")) as f:
    install_requires = []
    for line in f:
        requirement = line.split("#", 1)[0].strip()
        if not requirement:
            continue

        if requirement.startswith("--"):
            continue

        install_requires.append(requirement)


class VersionCommand(Command):
    description = "print library version"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


class EntryPointsCommand(Command):
    description = "display entry points"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @classmethod
    def get_entry_points(cls):
        hooks = open(".pre-commit-hooks.yaml").readlines()
        entry_points = []
        for hook in hooks:
            if "id:" in hook:
                entry_points.append({"entry": hook.split(":")[-1].strip()})

            if "name:" in hook:
                entry_points[-1]["name"] = hook.split(":")[-1].strip()

        return ["{entry} = {name}:main".format(**ep) for ep in entry_points]

    def run(self):
        print("\n".join(self.get_entry_points()))


setup(
    name="hulks",
    version=version,
    description="Olist custom linting hooks",
    long_description=long_description,
    url="https://github.com/olist/hulks",
    author="Olist Developers",
    author_email="developers@olist.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Software Development :: Testing",
    ],
    packages=find_packages(exclude=["tests*"]),
    install_requires=install_requires,
    entry_points={"console_scripts": EntryPointsCommand.get_entry_points()},
    cmdclass={"version": VersionCommand, "show_hooks": EntryPointsCommand},
)
