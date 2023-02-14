"""crypto_recommendations_api"""

from setuptools import setup

PACKAGE_NAME = 'crypto_recommendations_api'

with open('./requirements.txt') as requirements_file:
  requirements = requirements_file.read().splitlines()

with open('./dev-requirements.txt') as extras_file:
  development_requirements = extras_file.read().splitlines()

setup(
  name=PACKAGE_NAME,
  package_dir={PACKAGE_NAME: './crypto_recommendations_api'},
  install_requires=requirements, # requirements outlined in `requirements.txt`
  extras_require=development_requirements
)