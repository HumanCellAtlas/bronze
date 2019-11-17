from setuptools import setup, find_packages


setup(
    name='bronze',
    classifiers=['Programming Language :: Python :: 3'],
    description='The DCP Alarm Bronze',
    url='http://github.com/HumanCellAtlas/bronze',
    author='Human Cell Atlas Data Coordination Platform - Rex Wang',
    author_email='chengche@broadinstitute.org',
    license='BSD 3-clause "New" or "Revised" License',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client>=1.7.3',
        'requests>=2.20.0,<3',
        'google-auth>=1.6.1,<2',
        'pandas>=0.25.0,<0.26.0',
        'pyyaml>=5,<6',
        'pendulum>=2.0.5,<3',
    ],
    entry_points={'console_scripts': []},
    include_package_data=True,
)
