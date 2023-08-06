from setuptools import setup


setup(
    name='suds_requests4',
    version='1.0.1',
    description='A suds transport implemented with requests using suds-community',
    long_description=open('README.rst').read(),
    long_description_content_type='text/markdown',
    author='Jason Michalski',
    author_email='jmrosal@crosal-research.com',
    py_modules=['suds_requests'],
    install_requires=['requests', 'suds-community'],
    license='MIT',
    url='https://github.com/genusistimelord/suds_requests4',
	python_requires='>=3.7',
)
