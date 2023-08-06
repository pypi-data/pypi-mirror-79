
# 本项目介绍如何把项目封装成一个依赖包，使其可通
过pip install 安装

### 1、根目录创建setup.py
格式参考 https://packaging.python.org/tutorials/packaging-projects/#uploading-your-project-to-pypi

pip install test-zingfront-pypi --index-url https://pypi.python.org/pypi 
#### 2、根目录下创建__init__.py 维护可被导入的信息
比如该依赖包为test_zingfront_pypi
控制其可被 from test_zingfront_pypi import 的内容和 import的内容

### 3、保证根目录下生成requirements.txt依赖文件

>其中包含依赖包需要的依赖

>在别的项目pip安装该依赖包时，可把依赖包的依赖自动安装

### 安装

>pip install git+https://github.com/xx/xx.git