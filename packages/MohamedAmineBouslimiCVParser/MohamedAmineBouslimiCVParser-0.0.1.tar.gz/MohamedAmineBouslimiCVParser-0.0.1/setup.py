from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='MohamedAmineBouslimiCVParser',
  version='0.0.1',
  description='Resume parser for french and english resumes',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Mohamed Amine Bouslimi',
  author_email='aminobouslimi@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='CVParser', 
  packages=find_packages(),
  install_requires=[''] 
)
