from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='cccbr_methods',
      version='0.9',
      description='A Pythonic interface to the CCCBR Methods Library',
      long_description=readme(),
      url='http://github.com/lelandpaul/cccbr_methods',
      author='Leland Paul Kusmer',
      author_email='me@lelandpaul.com',
      license='MIT',
      packages=['cccbr_methods'],
      install_requires=[
          'bs4',
          'sqlalchemy',
          'lxml',
      ],
      entry_points = {
          'console_scripts': ['update-cccbr-methods=cccbr_methods.update:update_database'],
      },
      include_package_data=True,
      zip_safe=False)
