from setuptools import setup

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name='vermanager',
    version='0.1.2',
    author='junruoyu-zheng',
    author_email='zhengjry@outlook.com',
    url='https://gitee.com/junruoyu-zheng/ver-manager',
    description=u'A manager for versions. Modules with version requirements can be written as `ModuleName(==|>=|<=)1.2.3`. The VerManager is aimed at version control. ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['vermanager'],
    install_requires=[],
    entry_points={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)