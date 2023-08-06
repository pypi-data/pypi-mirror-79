# -*- coding:utf8 -*-
# @author：X.
# @time：2020/9/18:10:33


from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sktest",   # 包名字
    version="0.0.1",
    url="https://github.com/cxyboy/sktest",  # 包连接, 通常是github上的连接或readthedocs连接
    description="A library of tools to quickly expand UI testing",
    long_description=long_description,  # 将说明文件设置为README.md
    long_description_content_type="text/markdown",
    packages=find_packages(),   # 默认从当前目录下搜索包
    author="xuluocan",
    author_email="hijackx@163.com",
    classifiers=[   # 只适用于python3，若构建python2包，请移除
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)