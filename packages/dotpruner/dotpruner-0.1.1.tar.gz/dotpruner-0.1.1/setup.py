from setuptools import setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

setup(
    name='dotpruner',
    version='0.1.1',
    description='Pruning redundant nodes from DOT graphs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/ansonmiu0214/dotpruner',
    author='Anson Miu',
    author_email='me@ansonmiu.dev',
    license='MIT',
    packages=['dotpruner'],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    python_requires='>=3.6',
)