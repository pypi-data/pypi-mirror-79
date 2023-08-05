from setuptools import setup,find_packages

setup(
    name='FNTwitchSetup',
    version='0.0.1',
    author="Bryna",
    author_email="nazimek.helfi@gmail.com",
    description='Private module',
    url='https://github.com/TwitchCousinYT-FN/fntruc',
    packages=find_packages(),
    install_requires=['fortnitepy==1.7.1','sanic','requests','aiofiles']
)