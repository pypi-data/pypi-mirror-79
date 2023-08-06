from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='stringFun',
  version='0.0.2',
  description='It is a simple Strings related library,that simplifies some of the Strings operations and saves coding time specially while working on bigger projects.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Himanshu Kaushik',
  author_email='himanshukaushik1905@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['Python','strings','python strings'], 
  packages=find_packages(),
  install_requires=[''] 
)