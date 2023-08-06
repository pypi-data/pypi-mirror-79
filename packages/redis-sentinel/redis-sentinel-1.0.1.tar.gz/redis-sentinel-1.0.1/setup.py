from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='redis-sentinel',
    version_format='{tag}',
    packages=['redis_sentinel'],
    url='https://gitlab.com/kael_k/python-redis-sentinel',
    description="Redis connection fully managed by sentinel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='kael_k (Kael D\'Alcamo)',
    author_email='dalcamkael@gmail.com',
    setup_requires=['setuptools-git-version'],
    install_requires=[
        'redis==3.*'
    ],
    python_requires='>=3'
)