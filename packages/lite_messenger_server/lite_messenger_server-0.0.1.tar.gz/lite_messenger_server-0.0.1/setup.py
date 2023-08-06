from setuptools import setup, find_packages

setup(name="lite_messenger_server",
      version="0.0.1",
      description="lite_messenger_server",
      author="Dmitry Grodzinsky",
      author_email="dmitry.ml@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
