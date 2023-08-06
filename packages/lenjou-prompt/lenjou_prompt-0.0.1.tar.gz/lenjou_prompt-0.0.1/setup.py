"""
    @Author hlj

    @Date 2020/9/11 10:39

    @Describe  

"""
import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# 允许setup.py在任何路径下执行
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name="lenjou_prompt",
    version="0.0.1",
    author="lenjou",
    author_email="helijie9966@163.com",
    description="Window prompt and voice prompt for crawler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/lenjou/lenjou_prompt.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)