from setuptools import setup, find_packages

setup(name="Maxis_EA_server",
      version="0.0.1",
      description="mess_server",
      author="Maxim Baranov",
      author_email="maxis@ya.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
