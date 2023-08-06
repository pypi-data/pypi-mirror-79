import os

from setuptools import setup, find_packages

path = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(path, 'README.md')) as f:
        long_description = f.read()
except Exception as e:
    long_description = "customize okta cli"

setup(
    name="test-github-action",
    version="0.0.2",
    keywords=("pip", "okta", "cli", "cmd", "steven"),
    description="okta cli",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.5.0",
    license="MIT Licence",

    url="https://github.com/MaHu6/TestGithubAction",
    author="husima",
    author_email="simahu@outlook.com",

    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests", "click"],
    platforms="any",

    scripts=[],
    entry_points={
        'console_scripts': [
            'okta-cmd=oktacmd:main_cli'
        ]
    }
)
