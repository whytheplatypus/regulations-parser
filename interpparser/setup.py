from setuptools import setup, find_packages


setup(
    name='interpparser',
    version="0.0.1",
    packages=find_packages(),
    classifiers=[
        'License :: Public Domain',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    ],
    entry_points={
        'eregs_ns.parser.layer.cfr':
            'interpretations = interpparser.layers:Interpretations'
    }
)