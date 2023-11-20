## 步骤：

### 1. 设计搭建 Flask 蓝图的 Web 框架实例
项目中已经包含了蓝图（Blueprint）的结构，`user` 和 `home` 蓝图用于区分应用程序的不同组件。`user` 蓝图处理用户相关的视图，`home` 蓝图处理通用的站点导航。

### 2. 设置 `/user/*` 专属用户访问目录，做好权限校验 session
在 `views/user.py` 文件中，已经开始设置 `/user/*` 路由，并在 `befor_request` 函数中进行了 session 验证。这个函数会检查用户是否已登录，如果没有，会重定向到登录页面。

### 3. 使用模板继承，设置一个母模板
创建一个基础模板（命名为 `base.html`），其中包含所有页面共享的元素，如头部、导航栏和页脚。其他模板（如 `home.html`、`login.html` 等）将继承自这个母模板并填充特定的内容块。

### 4. 完善用户登录页面及功能
在 `views/user.py` 的 `login` 函数中，已经定义了处理 GET 和 POST 请求的逻辑。需要确保表单提交的数据与 `USER_LIST` 中的数据进行比对，如果匹配，则在 session 中记录用户状态，并重定向到用户中心页面。

### 5. 用户初始进入用户中心页面，通过闪现功能实现欢迎信息的展示
在 `views/user.py` 的 `login` 函数中，登录成功后使用 `flash` 函数发送欢迎消息。在用户中心的视图函数中（`home` 函数），从 `get_flashed_messages` 获取并显示这些消息。

### 6. 完善用户中心列表页面，用户信息展示页面
在用户中心列表页面，可以使用 `render_template` 渲染用户列表。用户信息展示页面可以是一个新的路由，用于展示单个用户的详细信息。

### 7. 对用户信息进行增加，删除，修改等操作
为这些操作创建新的视图函数。增加用户可以是一个表单页面，删除和修改可以在用户列表页面旁边添加按钮，触发相应的视图函数。

### 8. 基于 MySQL，设计用户表等，将上述操作基于数据库实现
我常用sql server，所以这里使用 pymssql 模块连接 sql server 数据库。在现有的蓝图中添加视图函数来处理用户信息的增加、删除和修改。所有的用户数据都将存储在数据库中，而不是 `USER_LIST` 字典。

### 9. 数据库表单、字段，系统中主要参数命名规则，以"自己姓名拼音首字母_变量名"来进行命名，例如范冰冰的项目中来定义name，以fbb_name来定义。
这里使用hyn_

## 文件说明

### 目录和文件结构

1. **db**:
   - `__init__.py`: 空文件，使 Python 将此目录视为包。
   - `sql_helper.py`: 包含 `SQLHelper` 类，用于处理与数据库的所有交互，如连接数据库、执行查询等。
   - `user.py`: 包含 `USER_LIST` 字典，最初用于存储用户信息（现在您的应用已连接到数据库，可能不再使用此字典）。

2. **static**:
   - 用于存储静态文件，如图片、CSS 和 JavaScript 文件。`favicon.ico` 是网站的图标。

3. **templates**:
   - 存储 HTML 模板文件，用于渲染页面。包括登录页面、用户列表、用户详情、添加和编辑用户等页面的模板。

4. **views**:
   - `__init__.py`: 同上，使其成为一个包。
   - `home.py`: 包含主页相关的视图函数。
   - `user.py`: 包含用户管理相关的视图函数，如登录、注销、显示用户列表、用户详情、添加和编辑用户等。

5. **app.py**:
   - Flask 应用的主入口。初始化 Flask 应用，注册蓝图，设置配置信息等。

6. **config.py** 和 **settings.py**:
   - 包含应用的配置设置，如调试模式、测试模式和密钥设置。

## 功能和作用

- **用户管理**: 应用支持创建新用户、编辑现有用户、删除用户和查看用户列表。
- **数据库交互**: 使用 `SQLHelper` 类与数据库进行交互，从而存储和检索用户数据。
- **模板渲染**: 使用 Flask 的模板引擎渲染 HTML 页面，提供用户界面。
- **登录和注销**: 支持用户登录和注销功能。
- **路由处理**: Flask 蓝图 (`Blueprint`) 用于组织和管理路由，处理不同的 URL 请求。
- **配置管理**: 应用配置文件用于设置不同环境下（开发、测试、生产）的配置参数。

## 使用说明
1. **登录界面**:
   - 输入账户和密码，会提示错误类型。
   ![Alt text](image-12.png)
   ![Alt text](image-13.png)

2. **用户主界面**:
   - 欢迎用户登录
    ![Alt text](image-14.png)


   - 提供三个功能界面
        - 用户列表：对用户信息进行删改查(查详细信息)
        ![Alt text](image-22.png)
            - 查看详情
            ![Alt text](image-23.png)
            - 编辑
            ![Alt text](image-17.png)
            - 删除：无界面，但会有二次提示：
            ![Alt text](image-18.png)

        - 添加用户：添加新用户，用户名不能重复
        ![Alt text](image-19.png)
        ![Alt text](image-20.png)
        添加成功后会自动跳转：
        ![Alt text](image-24.png)

        - 注销：注销当前登录
        ![Alt text](image-25.png)

## 数据库代码补充：

### 创建数据库
```python
CREATE TABLE dbo.hyn_usertable (
    hyn_id INT IDENTITY(1,1) PRIMARY KEY, -- 自动编号，主键
    hyn_username VARCHAR(50) NOT NULL, -- 用户名
    hyn_password VARCHAR(50) NOT NULL, -- 密码
    hyn_name NVARCHAR(100), -- 姓名
    hyn_gender NVARCHAR(10), -- 性别
    hyn_class NVARCHAR(100), -- 班级
    hyn_address NVARCHAR(100), -- 地址
    hyn_phone VARCHAR(20) -- 电话号码
);
```
