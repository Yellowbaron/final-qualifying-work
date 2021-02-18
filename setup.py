from cx_Freeze import setup, Executable
executables = [Executable('Project777.py')]

setup(name='dates',
      version='0.9.1',
      description='insert tags with temporal information',
      executables=executables)