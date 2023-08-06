from setuptools import setup
lond_d = '''pip install shellvaluepy

```py
#input
shell.value('dir')

#output
XXXXX XX XXXX
XXX X XXXXXXXXXXX X X
```

```py
#input
shell.install('shell_value')

#output
OK to install!
or
error!
```
'''
setup(name="shellvaluepy",
      version="0.1.0",
      url="https://github.com/hminkoo10/shell_value",
      license="MIT",
      author="hminkoo10",
      author_email="hmin.koo10@gmail.com",
      long_description=lond_d,
      long_description_content_type="text/markdown",
      description="made by hminkoo10, discord : Imposter#2879, email: hmin.koo10@gmail.com",
      packages=['shellvaluepy'],
      )
      
