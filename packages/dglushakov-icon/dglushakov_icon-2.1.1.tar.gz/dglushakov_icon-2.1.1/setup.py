from setuptools import setup, find_packages

setup(name='dglushakov_icon',
      version='2.1.1',
      description='Icon AR2NS',
      packages=find_packages(),
      author_email='denis.glushakov@bk.ru',
      install_requires=[
          'requests'
      ],
      zip_safe=False)
