
# python
import pathlib
import setuptools

README_FILE_PATH = pathlib.Path(__file__).parent.absolute().joinpath(
    'README.md',
)
with open(README_FILE_PATH) as f:
    long_description = f.read()

setuptools.setup(
    name='aw11',
    version='0.1.0',
    author='Erik Soma',
    author_email='stillusingirc@gmail.com',
    description='Code and config formatting and linting.',
    tests_require=[
        'coverage[toml]',
        'mypy',
        'pytest',
        'pytest-cov',
        'flake8',
        'flake8-broken-line',
        'flake8-bugbear',
        'flake8-builtins',
        'flake8-commas',
        'flake8-comprehensions',
        'flake8-fixme',
        'flake8-print',
        'flake8-use-fstring',
    ],
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/esoma/aw11',
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            'aw11-clean = aw11.clean:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
