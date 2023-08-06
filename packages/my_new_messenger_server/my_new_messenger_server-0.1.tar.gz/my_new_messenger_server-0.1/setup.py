from setuptools import setup, find_packages

setup(name="my_new_messenger_server",
      version="0.1",
      description="Messenger_server",
      author="Sergei Makarenko",
      author_email="makarenko.s@inbox.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
