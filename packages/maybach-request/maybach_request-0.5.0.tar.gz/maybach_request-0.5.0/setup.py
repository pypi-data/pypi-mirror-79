from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
  name = 'maybach_request',
  version = '0.5.0',
  long_description=long_description,  
  long_description_content_type="text/markdown", 
  url = 'https://gitlab.xiguacity.cn/fee/python/maybach_request',
  author = 'cuvee',
  author_email = 'cuizaiyong@xigua.club',
  license = 'MIT',
  packages = find_packages(),
)