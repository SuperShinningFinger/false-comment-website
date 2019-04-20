# false-comment-website

分辨评论中的虚假评论与真实评论的测试网站，前端真的丑。

示例的测试文件为`true.xlsx`

上传文件直接上传至根目录才能读取，需要修改`view.py`的路径

网址: http://47.95.196.246:8007/

## 环境配置

### 运行系统环境

Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-93-generic x86_64)

### Python版本

Python3.6.5

### Python依赖包

#### 依赖包文件：requirement.txt

```python
Django==2.2
jieba==0.39
nltk==3.4.1
pytz==2019.1
six==1.12.0
sqlparse==0.3.0
xlrd==1.2.0
```

#### 生成依赖包文件方法

```python
pip freeze > requirements.txt
```

#### 安装依赖方法

在项目根目录打开Python终端，运行

```python
pip install -r requirements.txt
```

## 运行项目方法

1. 在IDE(如Pycharm)中运行

2. 进入`manage.py`文件目录下,然后运行：

   ```python
   python3 manage.py runserver 0.0.0.0:8007
   nohup python -u manage.py runserver 0.0.0.0:8007 > out.log 2>&1 &    # 后台运行
   ```

