from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash
import random
import string
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "flask_login_demo_2024"
DATABASE = "user.db"

# 全局变量：存储重置验证码（实验环境简化
reset_verification_codes = {}  # 格式：{username: (code, expire_time)}

# 数据库操作函数（无修改）
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    user = conn.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
    if not user:
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                    ('admin', '123456'))
    conn.commit()
    conn.close()

def generate_verify_code():
    return ''.join(random.sample(string.ascii_letters + string.digits, 4))

def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user


# 验证码只在GET请求时生成，POST失败不刷新
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_msg = ""
    verify_code = ""

    if request.method == 'GET':
        # 只有GET请求（首次访问/刷新）才生成新验证码
        verify_code = generate_verify_code()
        session['verify_code'] = verify_code.lower()
        # 读取Cookie中的账号密码
        saved_username = request.cookies.get('saved_username', '')
        saved_password = request.cookies.get('saved_password', '')
        return render_template('login.html',
                               verify_code=verify_code,
                               error_msg=error_msg,
                               saved_username=saved_username,
                               saved_password=saved_password)
    else:  # POST请求（提交登录表单）
        # 沿用之前生成的验证码（不重新生成）
        verify_code = session.get('verify_code', '')
        saved_username = request.cookies.get('saved_username', '')
        saved_password = request.cookies.get('saved_password', '')

        # 获取表单数据
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user_input_code = request.form.get('verifyCode', '').strip().lower()
        remember_pwd = request.form.get('rememberPwd')

        # 严格按“必填字段→验证码→账号密码”顺序验证
        if not username.strip():
            error_msg = "请输入用户名"
            print(f"【后端日志】用户名为空，触发error_msg：{error_msg}")  # 调试日志
        elif not password.strip():  # 严格判断密码为空（含全空格）
            error_msg = "请输入密码"
            print(f"触发密码为空验证，error_msg：{error_msg}")  # 调试用：打印error_msg
        elif not user_input_code.strip():
            error_msg = "请输入验证码"
        elif user_input_code != session['verify_code']:
            error_msg = "验证码错误，请重新输入"
        else:
            user = get_user_by_username(username)
            if not user:
                error_msg = "用户名或密码错误"
            elif user['password'] != password:
                error_msg = "用户名或密码错误"
            else:
                # 登录成功逻辑（无修改）
                response = make_response(redirect(url_for('index')))
                if remember_pwd:
                    response.set_cookie('saved_username', username, max_age=7*24*3600)
                    response.set_cookie('saved_password', password, max_age=7*24*3600)
                else:
                    response.set_cookie('saved_username', '', expires=0)
                    response.set_cookie('saved_password', '', expires=0)
                session['current_user'] = username
                return response

        # POST失败，返回原页面（验证码不变）
        return render_template('login.html',
                               verify_code=verify_code,
                               error_msg=error_msg or "",  # 确保不为None
                               saved_username=saved_username,
                               saved_password=saved_password)

# 其他路由（无修改）
@app.route('/index')
def index():
    current_user = session.get('current_user')
    if not current_user:
        return redirect(url_for('login'))
    return render_template('index.html', current_user=current_user)

@app.route('/logout')
def logout():
    session.pop('current_user', None)
    # 移除清除saved_username和saved_password的Cookie代码 之前错误清除了记住密码的Cookie，导致自动填充失效
    session.pop('verify_code', None)
    response = make_response(redirect(url_for('login')))
    # 保留记住密码的Cookie
    # response.set_cookie('saved_username', '', expires=0)
    # response.set_cookie('saved_password', '', expires=0)
    return response

# 新增：处理忘记密码页面（显示输入用户名表单）
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('reset_username').strip()
        # 验证用户是否存在
        user = get_user_by_username(username)
        if not user:
            flash("用户名不存在")
            return render_template('forgot_password.html')
        # 生成6位数字重置验证码（实验简化，实际需发邮件/短信）
        reset_code = ''.join(random.sample(string.digits, 6))
        # 存储验证码（有效期5分钟）
        reset_verification_codes[username] = (reset_code, datetime.now().timestamp() + 300)
        print(f"【重置验证码】用户{username}：{reset_code}（5分钟内有效）")
        # 跳转至验证码输入页面
        session['reset_username'] = username
        return redirect(url_for('verify_reset_code'))
    # GET请求：显示输入用户名的忘记密码页面
    return render_template('forgot_password.html')

# 新增：验证码验证页面
@app.route('/verify_reset_code', methods=['GET', 'POST'])
def verify_reset_code():
    username = session.get('reset_username')
    if not username:
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        input_code = request.form.get('reset_code').strip()
        # 验证验证码
        code_info = reset_verification_codes.get(username)
        if not code_info:
            flash("验证码已过期，请重新申请")
            return render_template('verify_reset_code.html')
        code, expire_time = code_info
        if datetime.now().timestamp() > expire_time:
            flash("验证码已过期，请重新申请")
            del reset_verification_codes[username]
            return render_template('verify_reset_code.html')
        if input_code != code:
            flash("验证码错误")
            return render_template('verify_reset_code.html')
        # 验证码通过，跳转至重置密码页面
        return redirect(url_for('reset_password'))
    # GET请求：显示验证码输入页面
    return render_template('verify_reset_code.html')

# 新增：密码重置页面（核心）
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    username = session.get('reset_username')
    if not username:
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        new_pwd = request.form.get('new_password').strip()
        confirm_pwd = request.form.get('confirm_password').strip()
        # 验证密码一致性
        if new_pwd != confirm_pwd:
            flash("两次密码输入不一致")
            return render_template('reset_password.html')
        if len(new_pwd) < 6:
            flash("密码长度不能少于6位")
            return render_template('reset_password.html')
        # 更新数据库密码
        conn = get_db_connection()
        conn.execute('UPDATE users SET password = ? WHERE username = ?', (new_pwd, username))
        conn.commit()
        conn.close()
        # 清除临时数据
        session.pop('reset_username', None)
        reset_verification_codes.pop(username, None)
        flash("密码重置成功，请用新密码登录")
        return redirect(url_for('login'))
    # GET请求：显示重置密码页面
    return render_template('reset_password.html')

if __name__ == '__main__':
    init_database()
    app.run(debug=True)