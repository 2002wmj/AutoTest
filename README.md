# AutoTest
协议识别自动化测试工具，基于Python和Django开发。

# 安装说明

1 安装 Python3.6.1
$ wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
$ tar xvf Python-3.6.5.tar.xz  && cd Python-3.6.5
$ ./configure && make && make install

2 配置 py3 虚拟环境
$ python3 -m venv /opt/py3
$ source /opt/py3/bin/activate

3 安装Django 1.9环境
$ pip install Django==1.9.1
$ pip install pymysql paramiko bs4


4 下载AutoTest源码到home目录
$ cd /home
$ git clone git@github.com:2002wmj/AutoTest.git

5 按照你的环境修改配置文件
$ vim conf/at_config.py

6 初始化数据库
python manage.py migrate

7 设置root密码
python manage.py createsuperuser

8 导入目录下面的demo.sql到数据库中
