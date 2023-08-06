from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mypythonutils',
  version='1.0.1',
  description='A few useful functions',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Paul Gasnier',
  author_email='paulgasnier49@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='utils', 
  packages=find_packages(),
  install_requires=[''] 
)