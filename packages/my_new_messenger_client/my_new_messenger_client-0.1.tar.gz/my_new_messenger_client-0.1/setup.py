from setuptools import setup, find_packages

setup(name="my_new_messenger_client",
      version="0.1",
      description="Messenger_client",
      author="Sergei Makarenko",
      author_email="makarenko.s@inbox.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
