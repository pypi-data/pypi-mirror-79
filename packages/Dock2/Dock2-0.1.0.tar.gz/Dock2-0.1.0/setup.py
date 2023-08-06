from setuptools import setup
with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='Dock2',
    version='0.1.0',
    description="Simple wrapper for interacting with h2cs drivers (HTTP2 ClearText)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['h2'],
    url='https://github.com/Mwimwii/Dock2',
    author_email='qdyd65@gmail.com',
    author='goooby',
    py_modules=['Dock2'],
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: Proxy Servers',
        'Topic :: Security',
        'Operating System :: OS Independent',
    ],
    extras_require={
        'dev': [
            'pytest>=3.7'
        ]
    },
)
