from setuptools import setup, find_packages

setup(name='fartlib',
      version='1.1.1',
      description='Burp Intruder but more 💩',
      author='jro',
      install_requires=["requests", "tqdm"],
      package_data={'': ['wordlists/usernames.txt','wordlists/passwords.txt']},
      include_package_data=True,
      packages=find_packages())
