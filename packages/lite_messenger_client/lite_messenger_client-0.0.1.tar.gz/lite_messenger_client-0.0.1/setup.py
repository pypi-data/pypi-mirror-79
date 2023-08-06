from setuptools import setup, find_packages

setup(name="lite_messenger_client",
      version="0.0.1",
      description="lite_messenger_client",
      author="Dmitry Grodzinsky",
      author_email="dmitry.ml@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
