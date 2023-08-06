from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='strictdf',
  version='0.0.11',
  description='A very basic dataframe check',
  long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Test Test',
  author_email='testpypi01@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='strictdf', 
  packages=find_packages(),
  install_requires=['pandas', 'pyspark'] 
)
