from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='krishanfirstpackage',
    version='0.0.1',
    description='Sample package',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGE.txt').read(),
    long_description_content_type='text/x-rst',
    url='',  
    author='Kun Han',
    author_email='khan7@uci.edu',
    license='MIT', 
    classifiers=classifiers,
    keywords='package sample', 
    packages=find_packages(),
    install_requires=[''] 
)