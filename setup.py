from setuptools import setup
import re

with open("logger_serv_py_cli/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read(), re.M).group(1)

setup(
    name="logger_serv_py_cli",
    version=version,
    install_requires=["requests", "requests-futures"],
)