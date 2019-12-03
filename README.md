# flask框架main模板
flask框架用户管理模板，在flask-login的基础上添加了用户管理功能。

## Features
**1、初始化：**
 - [x] 配置文件
 - [x] 脚本启动
 - [x] 数据模型
 - [x] 蓝图

**2、登录注册功能**
 - [x] 用户登录
 - [x] 用户注册
 - [x] 用户数据模型
 - [x] 密码校验

**3、用户管理功能** 
 - [x] 用户信息管理
 - [x] 用户头像管理
 - [x] 用户密码管理
 
**4、主面板功能**
 - [x] 主页
 - [x] 导航栏
 - [x] 资讯
## 使用
**1、依赖** 

一键安装依赖：
```pip install -r requirements.txt```

 - flask_script
 - flask_migrate
 - flask_login
 - pymysql

**2、数据库初始化**
 - `python manage.py db init`:初始化一个迁移脚本的环境，只需要执行一次。  
 - `python manage.py db migrate`:将模型生成迁移文件，只要模型更改了，就需要执行一遍这个命令。
 - `python manage.py db upgrade`:将迁移文件真正的映射导数据库中，每次运行了`migrate`命令后，就记得要运行这个命令。


## 更新
 - 19-11-29
    - 创建项目
 - 19-12-02
    - 添加用户管理功能

## 截图
### 登录
![登录](https://github.com/ZhuangleiScut/flask-login/blob/master/app/static/image/%E7%99%BB%E5%BD%95.png)

### 注册
![注册](https://github.com/ZhuangleiScut/flask-login/blob/master/app/static/image/%E6%B3%A8%E5%86%8C.png)
