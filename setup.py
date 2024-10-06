from setuptools import setup, find_packages


def parse_requirements():
    with open("requirements.txt", "r") as requirements:
        return requirements.read().splitlines()


setup(
    name='logging_notifications',
    version='0.1',
    packages=find_packages(),
    install_requires=parse_requirements(),
    description='Logging and encrypted message handler package',
    author='Leo Martinez',
    author_email='leojmartinez@proton.me',
    url='https://github.com/thecheetahcat/logging-notifications',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
