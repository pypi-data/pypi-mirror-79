from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='libreriasuma',
  version='0.0.1',
  description='Una suma',
  long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Usuario Test',
  author_email='cuenta.medium@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='suma', 
  packages=find_packages(),
  install_requires=[] 
  # En este caso no necesito ninguna libreria, si me hiciera falta alguna
  # solo tengo que agregarlo, ej: 'pandas', 'pyspark'
)