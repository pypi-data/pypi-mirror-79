from setuptools import find_packages, setup

setup(
    name='pure-protobuf',
    version='2.0.1',
    description='Python implementation of Protocol Buffers data types with dataclasses support',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pavel Perestoronin',
    author_email='eigenein@gmail.com',
    url='https://github.com/eigenein/protobuf',
    packages=find_packages(exclude=['tests*']),
    zip_safe=True,
    install_requires=[
        'dataclasses>=0.6,<1.0; python_version < "3.7"',
    ],
    extras_require={
        'dev': ['flake8', 'isort', 'pytest', 'pytest-cov', 'coveralls'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
    project_urls={
        'Changelog': 'https://github.com/eigenein/protobuf/blob/master/CHANGELOG.md',
    },
)
