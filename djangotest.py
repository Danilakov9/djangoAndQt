import json
import mysql.connector

# 连接MySQL数据库
db = mysql.connector.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    password="88888888",  # 数据库密码
    database="qtdata",  # 数据库名称
)

cursor = db.cursor()

# 创建表格（如果不存在）
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp VARCHAR(20),
    temperature VARCHAR(10),
    humidity VARCHAR(10),
    gas VARCHAR(10),
    sensor_id VARCHAR(20)
)
"""
)

# 打开并读取JSON文件
with open("data.json", "r") as file:
    data = json.load(file)

# 遍历JSON数组并将数据插入到数据库中
for entry in data:
    timestamp = entry.get("Timestamp", "")
    temperature = entry.get("Temperature", "")
    humidity = entry.get("Humidity", "")
    gas = entry.get("Gas", "")
    sensor_id = entry.get("ID", "")

    cursor.execute(
        """
    INSERT INTO sensor_data (timestamp, temperature, humidity, gas, sensor_id)
    VALUES (%s, %s, %s, %s, %s)
    """,
        (timestamp, temperature, humidity, gas, sensor_id),
    )

# 提交事务
db.commit()

# 关闭数据库连接
db.close()

print("Data has been inserted successfully.")
