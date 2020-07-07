from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='methods_library',
      version='0.9',
      description='A Pythonic interface to the CCCBR Methods Library',
      long_description=readme(),
      url='http://github.com/lelandpaul/methods_library',
      author='Leland Paul Kusmer',
      author_email='me@lelandpaul.com',
      license='MIT',
      packages=['methods_library'],
      install_requires=[
          'bs4',
          'sqlalchemy',
          'lxml',
      ],
      entry_points = {
          'console_scripts': ['update-methods-library=methods_library.import:main'],
      },
      include_package_data=True,
      zip_safe=False)
