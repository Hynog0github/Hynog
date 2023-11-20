from flask import Blueprint, render_template, redirect, session, request, flash, get_flashed_messages,url_for
from users import USER_LIST
from sql_helper import SQLHelper


# user_blueprint = Blueprint('user', __name__, url_prefix='/user')

us = Blueprint('user', __name__, url_prefix='/people')


@us.before_request
def befor_request():
    print("======befor_request======")
    print(request.path)
    if request.path == "%s/login" % us.url_prefix:
        return None
    if not session.get("user"):
        return redirect("/people/login")


@us.route("/")  # /people/
def home():
    print("user home... %s " %get_flashed_messages())
    welcome = get_flashed_messages()
    return render_template("home.html", welcome=welcome)


@us.route('/info')  # /people/info
def info():
    return "用户个人信息..."


@us.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        print("这是一个get请求")
        return render_template("login.html")

    print("这是一个post请求")
    hyn_username = request.form.get("hyn_username")
    hyn_password = request.form.get("hyn_password")
    print("username: %s, password: %s" % (hyn_username, hyn_password))

    # 从数据库获取用户信息
    user = SQLHelper.fetch_one("SELECT * FROM hyn_usertable WHERE hyn_username = %s", (hyn_username,))
    print(user)  # 检查这里是否包含完整的数据

    if not user:
        msg = "用户名错误"
        return render_template("login.html", msg=msg)

    if user['hyn_password'] != hyn_password:
        msg = "密码错误"
        return render_template("login.html", msg=msg)

    flash("%s 欢迎您的到来" % user['hyn_name'])
    session["user"] = user


    return redirect("/people")

# 用户列表视图
@us.route('/users')
def user_list():
    users = SQLHelper.fetch_all("SELECT * FROM hyn_usertable")
    return render_template('user_list.html', user_list=users)




# 用户详情视图
@us.route('/users/<int:user_id>')
def user_detail(user_id):
    user = SQLHelper.fetch_one("SELECT * FROM hyn_usertable WHERE hyn_id = %s", (user_id,))
    return render_template('user_detail.html', user=user)


@us.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':

        # 从表单中获取数据
        hyn_username = request.form['hyn_username']
        hyn_password = request.form['hyn_password']
        hyn_name = request.form['hyn_name']
        hyn_gender = request.form['hyn_gender']  # 假设您添加了性别字段
        hyn_class = request.form['hyn_class']    # 假设您添加了班级字段
        hyn_address = request.form['hyn_address'] # 假设您添加了地址字段
        hyn_phone = request.form['hyn_phone']  # 假设您添加了电话号码字段

        existing_user = SQLHelper.fetch_one("SELECT * FROM hyn_usertable WHERE hyn_username = %s", (hyn_username,))
        if existing_user:
            flash('用户名已存在，请选择其他用户名')
            return render_template('add_user.html', username=hyn_username)

        # 插入数据库
        SQLHelper.execute(
            "INSERT INTO hyn_usertable (hyn_username, hyn_password, hyn_name, hyn_gender, hyn_class, hyn_address, hyn_phone) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (hyn_username, hyn_password, hyn_name, hyn_gender, hyn_class, hyn_address, hyn_phone))

        return redirect(url_for('user.user_list'))

    return render_template('add_user.html')


@us.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    SQLHelper.execute("DELETE FROM hyn_usertable WHERE hyn_id = %s", (user_id, ))
    return redirect(url_for('user.user_list'))


@us.route('/logout')
def logout():
    # 清除会话信息
    session.clear()
    return redirect(url_for('user.login'))



@us.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        hyn_username = request.form['hyn_username']
        existing_user = SQLHelper.fetch_one("SELECT * FROM hyn_usertable WHERE hyn_username = %s AND hyn_id != %s", (hyn_username, user_id))
        if existing_user:
            flash('用户名已存在，请选择其他用户名')
            return redirect(url_for('user.edit_user', user_id=user_id))
        hyn_password = request.form.get('hyn_password')
        hyn_name = request.form.get('hyn_name')
        hyn_gender = request.form.get('hyn_gender')
        hyn_class = request.form.get('hyn_class')
        hyn_address = request.form.get('hyn_address')
        hyn_phone = request.form.get('hyn_phone')

        SQLHelper.execute("UPDATE hyn_usertable SET hyn_username=%s, hyn_password=%s, hyn_name=%s, hyn_gender=%s, hyn_class=%s, hyn_address=%s, hyn_phone=%s WHERE hyn_id=%s",
                          (hyn_username, hyn_password, hyn_name, hyn_gender, hyn_class, hyn_address, hyn_phone, user_id))
        return redirect(url_for('user.user_list'))
    else:  # 处理 GET 请求
        user = SQLHelper.fetch_one("SELECT * FROM hyn_usertable WHERE hyn_id = %s", (user_id,))
        return render_template('edit_user.html', user=user)




