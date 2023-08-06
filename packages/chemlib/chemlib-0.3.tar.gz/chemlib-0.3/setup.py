from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='chemlib',
    version='0.3',
    description='Easy-to-use library to perform chemistry calculations.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Hari Ambethkar',
    author_email='harirakul.a@gmail.com',
    keywords=['Chemistry', 'Chemlib'],
    url='https://github.com/harirakul/chemlib',
    download_url='https://pypi.org/project/chemlib/'
)

install_requires = [
    'pandas',
    'numpy',
    'sympy'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)