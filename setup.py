from setuptools import setup

setup(name='logger_serv_py_cli',
      version='0.1',
      description='Server for logs',
      url='https://github.com/mlnagents/logger_serv_py_cli',
      author='Andrey Kusko',
      author_email='a.kusko@list.ru',
      license='MA',
      packages=['logger_serv_py_cli'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
