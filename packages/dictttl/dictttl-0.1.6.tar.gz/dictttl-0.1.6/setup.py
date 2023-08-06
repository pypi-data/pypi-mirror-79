from setuptools import setup, find_packages

setup(name='dictttl',
      version='0.1.6',
      url='https://github.com/srivassid/DictTTL',
      license='MIT',
      author='Siddharth Srivastava',
      author_email='s.srivas@hotmail.com',
      description='Dictionary with TTL attached to the keys',
      packages=find_packages(),
      long_description=open('README.md').read(),
      zip_safe=False)