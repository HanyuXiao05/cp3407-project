import pymysql
from tabulate import tabulate

def view_members():
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
            # 获取会员表的所有数据
            cursor.execute("SELECT * FROM member")
            members = cursor.fetchall()
            
            # 获取列名
            cursor.execute("DESCRIBE member")
            columns = [column[0] for column in cursor.fetchall()]
            
            if members:
                print("\n会员表内容：")
                print(tabulate(members, headers=columns, tablefmt='grid'))
            else:
                print("\n会员表目前没有数据")
            
        connection.close()
        
    except Exception as e:
        print(f"查询数据时出错：{str(e)}")
        raise

if __name__ == '__main__':
    view_members() 