from setuptools import find_namespace_packages, setup

setup(
    name='snake-game',
    version='0.1',
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': [
            'snake=snake.cli:main'
        ]
    },

    # metadata to display on PyPI
    author="Ravi Kumar Nimmi",
    author_email="nimmi.ravikumar@gmail.com",
    description="Snake Game.",
    keywords="snake game",
    # url="http://example.com/HelloWorld/",   # project home page, if any
    # project_urls={
    #     "Bug Tracker": "https://bugs.example.com/HelloWorld/",
    #     "Documentation": "https://docs.example.com/HelloWorld/",
    #     "Source Code": "https://code.example.com/HelloWorld/",
    # },
    # classifiers=[
    #     "License :: OSI Approved :: Python Software Foundation License"
    # ]
)
