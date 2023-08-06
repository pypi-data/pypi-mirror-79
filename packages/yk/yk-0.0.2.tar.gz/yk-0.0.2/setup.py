import setuptools
import os
import io

# pipreqs ./ --encoding=utf8 --force 生成requirements依赖文件
with io.open('requirements.txt') as f:
    requirements = f.readlines()

path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(path, 'README.md'), "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="yk",
    version="0.0.2",
    author="yiane",
    author_email="yiane@qq.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    # py_modules=[],#打包的.py文件
    packages=setuptools.find_packages(),  # 打包的python文件夹
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,  # 当前package所依赖的其他python类库
    entry_points={
        'console_scripts': [  # 用来支持自动生成cli命令
            'yk-comps=yk.comparison:main'
        ]
    }
)
