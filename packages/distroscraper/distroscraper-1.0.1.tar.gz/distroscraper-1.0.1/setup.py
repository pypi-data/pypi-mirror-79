import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="distroscraper",
    version="1.0.1",
    author="Jeff Tickle",
    author_email="jeff.tickle+pypi@protonmail.com",
    description="Scrape Linux Distro torrents and add to Transmission automatically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://jefftickle.com/projects/distroscraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Communications :: File Sharing",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Operating System",
        "Topic :: System :: Software Distribution",
        "Topic :: Utilities"
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4',
        'lxml',
        'requests',
        'transmissionrpc',
        'htmlmin',
    ]
)
