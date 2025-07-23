import pymysql

def test_connection():
    try:
        # 连接到数据库
        connection = pymysql.connect(
            host='43.160.205.48',
            user='root',
            password='CP3407',
            port=3306,
            database='jcu_gym_ms'
        )
        
        with connection.cursor() as cursor:
            # 获取所有表名
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("数据库连接成功！")
            print("\n现有的表：")
            for table in tables:
                print(f"- {table[0]}")
            
        connection.close()
        
    except Exception as e:
        print(f"连接数据库时出错：{str(e)}")
        raise

if __name__ == '__main__':
    test_connection() 