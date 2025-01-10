from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import pooling
from flask_cors import CORS  # 导入 CORS

# 创建 Flask 应用
app = Flask(__name__)
CORS(app)  # 启用 CORS，允许所有来源的请求
# 配置数据库连接池
dbconfig = {
    "host": "123.57.246.2176",
    "user": "shenmi",
    "password": "FiEyF3AKRKBKtm7y",
    "database": "shenmi"
}

# 使用连接池优化数据库连接
db_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,  # 连接池大小
    **dbconfig
)

# 获取数据库连接的函数
def get_db_connection():
    return db_pool.get_connection()

# 测试数据库连接接口
@app.route('/test_db')
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM company")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except mysql.connector.Error as err:
        return jsonify({"error": f"数据库连接失败: {err}"}), 500

# 添加公司接口
@app.route('/add_company', methods=['POST'])
def add_company():
    company_name = request.json.get('name')
    company_address = request.json.get('address')
    company_phone = request.json.get('phone')
    company_email = request.json.get('email')

    if not company_name:
        return jsonify({"message": "公司名称不能为空"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO company (name, address, phone, email) VALUES (%s, %s, %s, %s)",
            (company_name, company_address, company_phone, company_email)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "公司已添加!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"message": f"添加公司失败: {err}"}), 500

# 获取公司信息接口
@app.route('/get_companies', methods=['GET'])
def get_companies():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM company")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except mysql.connector.Error as err:
        return jsonify({"message": f"查询公司失败: {err}"}), 500

# 添加用户接口
@app.route('/add_user', methods=['POST'])
def add_user():
    company_id = request.json.get('company_id')
    username = request.json.get('username')
    password = request.json.get('password')  # 明文密码，注意这里没有加密

    if not username or not password:
        return jsonify({"message": "用户名和密码不能为空"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user (company_id, username, password) VALUES (%s, %s, %s)",
            (company_id, username, password)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "用户已添加!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"message": f"添加用户失败: {err}"}), 500

# 添加登录验证接口
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')  # 用户输入的密码

    if not username or not password:
        return jsonify({"message": "用户名和密码不能为空"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user[3] == password:  # user[3] 应该是密码字段
            return jsonify({"message": "登录成功!"}), 200
        else:
            return jsonify({"message": "用户名或密码错误!"}), 401
    except mysql.connector.Error as err:
        return jsonify({"message": f"登录失败: {err}"}), 500

# 根路由
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)  # 启动 Flask 开发服务器
