from setuptools import setup, find_packages

setup(
    name = "Unified Tracker",
    version = "0.1",
    packages = find_packages(),

    author="Sandy Maguire",
    author_email="sandy@sandymaguire.me",
    description="The unified tracker for qualified self",

    entry_points={
        "console_scripts": {
            "ute = ute.curses:main",
        }
    },

    install_requires=[
        "urwid>=1.3.0"
    ],
)

