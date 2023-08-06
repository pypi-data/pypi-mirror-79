from setuptools import find_packages, setup
import os
with open(os.path.join(__file__, '../README.rst'), encoding='utf-8') as f:
    long_description = f.read()
setup(name='aws-sagemaker-remote',
      version='0.0.1',
      author='Ben Striner',
      url='https://github.com/bstriner/aws-sagemaker-remote',
      install_requires=[
          'sagemaker'
      ],
      packages=find_packages(),
      long_description=long_description,
      long_description_content_type='text/x-rst')

# python setup.py bdist_wheel sdist && twine upload dist\*
