from setuptools import setup
from os.path import join, dirname

setup(name='easyhelloworld',
      version='1.0',
      description='Hello World',
      packages=['easyhelloworld'],
      author_email='easyhelloworld228@gmail.com',
      long_description=open(join(dirname(__file__), 'README.txt')).read(),
      zip_safe=False)
