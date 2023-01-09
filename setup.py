from setuptools import setup, find_packages

setup(name='fartlib',
      version='1.0.0',
      description='Burp Intruder but more 💩',
      author='jro',
      install_requires=["requests", "tqdm"],
      packages=find_packages())
