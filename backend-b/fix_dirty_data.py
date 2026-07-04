import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "data", "tree_adoption.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 先看当前脏数据
print("修改前 companyId=4:")
for row in cursor.execute("SELECT * FROM company WHERE companyId = 4"):
    print(row)

print("\n修改前 recordId=4:")
for row in cursor.execute("SELECT * FROM maintenance_record WHERE recordId = 4"):
    print(row)

# 修改 company 脏数据
cursor.execute("""
UPDATE company
SET
  companyName = '天子山示范果园',
  address = '四号果园 D 区',
  contactPhone = '0571-77778888',
  description = '用于课程演示的测试果园主体'
WHERE companyId = 4
""")

# 修改 maintenance_record 脏数据
cursor.execute("""
UPDATE maintenance_record
SET
  maintainType = '施肥',
  description = '完成夏季施肥，树体状态稳定'
WHERE recordId = 4
""")

conn.commit()

print("\n修改后 companyId=4:")
for row in cursor.execute("SELECT * FROM company WHERE companyId = 4"):
    print(row)

print("\n修改后 recordId=4:")
for row in cursor.execute("SELECT * FROM maintenance_record WHERE recordId = 4"):
    print(row)

conn.close()

print("\n数据库脏数据修复完成。")
