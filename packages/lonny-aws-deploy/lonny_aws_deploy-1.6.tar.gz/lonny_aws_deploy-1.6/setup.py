from setuptools import setup, find_packages

with open("requirements.in") as f:
    setup(
        name = "lonny_aws_deploy",
        version = "1.6",
        packages = find_packages(),
        scripts = ["bin/aws_deploy"],
        install_requires = f.read().splitlines()
    )