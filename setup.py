from distutils.core import setup

setup(
    name="elgato",
    version="0.1.0",
    author="Roni Choudhury",
    author_email="aichoudh@gmail.com",
    packages=["elgato"],
    entry_points={
        "console_scripts": ["elgato=elgato.__main__:main"],
    },
    url="https://github.com/waxlamp/elgato",
    license="LICENSE",
    description="Control script for El Gato brand keylights",
    long_description=open("README.md").read(),
    install_requires=[
        "leglight == 0.2.0",
    ],
)
