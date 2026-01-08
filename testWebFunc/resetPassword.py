import sqlite3
import os
from sqlite3 import OperationalError

def reset_admin_password(db_path, target_password="88888888"):
    """
    重置admin用户密码为目标值
    :param db_path: SQLite数据库文件（user.db）路径
    :param target_password: 目标密码，默认88888888
    """
    # 1. 验证数据库文件是否存在
    if not os.path.exists(db_path):
        print(f"❌ 错误：未找到数据库文件 {db_path}")
        print(f"   请确认路径正确，当前目录：{os.getcwd()}")
        return

    conn = None
    cursor = None
    try:
        # 2. 连接数据库（SQLite文件级连接）
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(f"✅ 成功连接数据库：{db_path}")

        # 3. 执行更新密码SQL
        sql = f"UPDATE users SET password = ? WHERE username = 'admin';"
        cursor.execute(sql, (target_password,))  # 参数化查询，避免SQL注入风险
        conn.commit()

        # 4. 验证执行结果
        if cursor.rowcount > 0:
            print(f"🎉 密码重置成功！admin用户新密码：{target_password}")
        else:
            print(f"⚠️  未找到admin用户，执行以下操作：")
            # 若admin用户不存在，自动创建（适配极端场景）
            create_sql = "INSERT OR IGNORE INTO users (username, password) VALUES ('admin', ?);"
            cursor.execute(create_sql, (target_password,))
            conn.commit()
            print(f"✅ 已自动创建admin用户，密码：{target_password}")

    except OperationalError as e:
        print(f"❌ 执行失败：{str(e)}")
        print(f"   可能原因：1. users表不存在（需先启动Flask项目创建表）；2. 数据库被占用")
    except Exception as e:
        print(f"❌ 未知错误：{str(e)}")
    finally:
        # 5. 关闭资源
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("✅ 数据库连接已关闭")

if __name__ == "__main__":
    # -------------------------- 核心配置（仅需修改这部分） --------------------------
    # 数据库路径：若user.db在当前目录，直接写"user.db"；否则写绝对路径
    DB_FILE_PATH = "user.db"
    # 示例绝对路径（Windows）：DB_FILE_PATH = "C:/Users/Administrator/Desktop/testWebFunc/user.db"
    # -------------------------- 执行入口 --------------------------
    reset_admin_password(DB_FILE_PATH)