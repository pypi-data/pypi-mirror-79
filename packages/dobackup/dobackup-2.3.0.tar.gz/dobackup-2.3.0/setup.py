import setuptools

from dobackup import __version__

with open("README.md", encoding="utf-8") as readme_file:
    full_description = readme_file.read()
    readme_file.close()

setuptools.setup(
    name="dobackup",
    version=__version__,
    description="Automated Offline Or Live Snapshots Of Digitalocean Droplets",
    license="GNU General Public License v3 or later (GPLv3+)",
    author="JGill",
    zip_safe=False,
    author_email="joty@mygnu.org",
    url="https://github.com/jotyGill/digitalocean-backup/",
    keywords=[
        "backup",
        "automated-backup",
        "digitalocean",
        "digital-ocean",
        "backups",
        "automation",
        "digitalocean-backup",
        "snapshots",
    ],
    python_requires=">=3.5",
    install_requires=["python-digitalocean>=1.15.0", "requests"],
    tests_require=["mock", "pytest", "pytest-cov"],
    platforms=["GNU/Linux", "Ubuntu", "Debian", "Kali", "CentOS", "Arch", "Fedora"],
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["dobackup = dobackup.dobackup:main"]},
    include_package_data=True,
    long_description=full_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
        "Topic :: System :: Archiving",
        "Topic :: System :: Archiving :: Backup",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
)
