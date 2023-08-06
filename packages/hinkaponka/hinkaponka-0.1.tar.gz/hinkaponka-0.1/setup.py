from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()
	
setup_args = dict(
    name='hinkaponka',
    version='0.1',
    description='Test Helo World package',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Sayjini Tay',
    author_email='shinyan1301@gmail.com',
    keywords=['Hello', 'World', 'HelloWorld'],
    url='https://github.com/shinjiniray/testpackage',
    download_url='https://pypi.org/project/hinkaponka/'
)

install_requires = [
    'numpy',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)