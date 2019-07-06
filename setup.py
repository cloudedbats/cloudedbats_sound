
from setuptools import setup

from sound4bats import __version__

setup(name='sound4bats',
    version=__version__,
    description='Sound Processing for bats, a part of the CloudedBats.org project.',
    url='https://github.com/cloudedbats/cloudedbats_sound',
    author='Arnold Andreasson',
    author_email='info@cloudedbats.org',
    license='MIT',
    packages=['sound4bats'],
    install_requires=[
        'numpy', 
        'matplotlib', 
    ],
    zip_safe=False)