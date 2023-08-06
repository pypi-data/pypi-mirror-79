from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()
	
setup_args = dict(
    name='loganalysispackage',
    version='0.6',
    description='loganalysispackage',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Shinjini Ray',
    author_email='shinjini.ray@gmail.com',
    keywords=['log', 'analysis', 'neuralnetwork'],
    url='https://github.com/shinjiniray/loganalysispackage',
    download_url='https://pypi.org/project/loganalysispackage'
)

install_requires = [
	'pymongo',
	'dnspython',
	'elasticsearch',
	'numpy==1.18.5',
	'sklearn',
	'tensorflow',
	'matplotlib'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)