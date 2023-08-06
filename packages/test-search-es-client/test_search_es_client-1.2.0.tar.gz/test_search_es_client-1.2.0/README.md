
## 建包流程

### 1、根目录创建setup.py
格式参考 https://packaging.python.org/tutorials/packaging-projects/#uploading-your-project-to-pypi


#### 2、包文件目录下的__init__
维护可以被引入使用的内容

#### 3、 打包
```
python setup.py sdist
```

#### 4、上次
```
twine upload dist/*
```

### 发送到pypi
```
twine upload dist/*
```
账号 zhaojianwei
密码 1q2w3e@zinf0917

### 别的项目安装改依赖包

>pip install package_name --index-url https://pypi.python.org/pypi 







>pip install git+https://github.com/xx/xx.git