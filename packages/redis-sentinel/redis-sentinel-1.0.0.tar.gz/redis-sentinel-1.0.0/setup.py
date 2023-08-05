from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='redis-sentinel',
    version='1.0.0',
    packages=['redis_sentinel'],
    url='https://gitlab.com/kael_k/python-redis-sentinel',
    description="Redis connection fully managed by sentinel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='kael_k (Kael D\'Alcamo)',
    author_email='dalcamkael@gmail.com',
    install_requires=[
        'redis==3.*'
    ],
    python_requires='>=3'
)