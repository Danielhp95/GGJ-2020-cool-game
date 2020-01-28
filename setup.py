from setuptools import setup, find_packages

setup(name='gym_cool_game',
      version='0.1',
      description='OpenAI gym environment our cool game jam game',
      url='https://github.com/Danielhp95/GGJ-2020-cool-game',
      author='Sarios',
      author_email='madness@xcape.com',
      packages=find_packages(),
      install_requires=['gym', 'numpy', 'pygame']
      )
