from setuptools import setup
import os

setup(
    name='remarkable-sim',
    version='1.0.4',
    packages=['remarkable_sim'],
    author="Evan Widloski",
    author_email="evan@evanw.org",
    description="evdev/framebuffer simulation for reMarkable desktop development",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="GPLv3",
    keywords="remarkable evdev sim simulator simulation tablet",
    url="https://github.com/evidlo/remarkable_sim",
    entry_points={
        'console_scripts': [
            'resim = remarkable_sim.sim:main',
            'remarkable_sim = remarkable_sim.sim:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
