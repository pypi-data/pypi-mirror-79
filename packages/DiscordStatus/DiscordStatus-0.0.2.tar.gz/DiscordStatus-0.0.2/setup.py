import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DiscordStatus",
    version="0.0.2",
    author="Byron Mulvogue",
    author_email="not.2.me.damaged@gmail.com",
    description="A wrapper for talking to the Discord Status page's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SomewhatDamaged/discordstatus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests'
    ],
    python_requires='>=3.6',
)
