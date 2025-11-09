# -*- coding: utf-8 -*-

import sqlite3

def query_by_product_name(product_name):
    # 連接 SQLite 資料庫
    conn = sqlite3.connect('SportsEquipment.db')
    cursor = conn.cursor()

    # 使用 SQL 查詢依名稱查找商品。'%'符號允許部分匹配。
    cursor.execute("SELECT * FROM products WHERE product_name LIKE ?", ('%' + product_name + '%',))

    # 取得所有查詢到的資料
    rows = cursor.fetchall()

    # 關閉連線
    conn.close()

    return rows

def create_and_populate_database():
    # 連接到本地資料庫檔案
    conn = sqlite3.connect('SportsEquipment.db')  # 指定檔名以儲存資料庫
    cursor = conn.cursor()

    # 檢查是否存在名為 'products' 的資料表，若不存在則建立
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products';")
    if cursor.fetchone() is None:
        # 建立資料表
        cursor.execute('''
        CREATE TABLE products (
            product_id TEXT,
            product_name TEXT,
            description TEXT,
            specifications TEXT,
            usage TEXT,
            brand TEXT,
            price REAL,
            stock_quantity INTEGER
        )
        ''')
        # 商品資料清單，用於插入資料表
        products = [
            (
            '001', '足球', '高品質職業比賽用球，符合國際標準', '圓形，直徑22 cm', '職業比賽、學校體育課', '耐克', 120, 50),
            ('002', '羽毛球拍', '輕量級，適合初中級選手，提供優秀的擊球感受', '碳纖維材質，重量85 g', '業餘比賽、家庭娛樂',
             '尤尼克斯', 300, 30),
            ('003', '籃球', '室內外皆可用，耐磨耐用，適合各種天氣條件', '皮質，標準7號球', '學校、社區運動場', '斯伯丁', 200,
             40),
            ('004', '跑步鞋', '適合長距離跑步，舒適透氣，提供良好的足弓支撐', '多種尺寸，透氣網布', '長跑、日常訓練',
             '阿迪達斯', 500, 20),
            ('005', '瑜伽墊', '防滑材質，厚度適中，易於攜帶和清洗', '長180cm，寬60cm，厚5mm', '瑜伽、皮拉提斯', '曼達卡', 150,
             25),
            ('006', '速乾運動衫', '吸汗快乾，適合各種戶外運動，持久舒適', 'S/M/L/XL，多色可選', '運動、健行、旅遊', '諾斯臉',
             180, 60),
            ('007', '電子計步器', '精確計步，帶心率監測功能，藍牙連接手機應用', '可充電，續航7天', '日常健康管理、運動',
             'Fitbit', 250, 15),
            ('008', '乒乓球拍套裝', '包含兩支拍子和三顆球，適合家庭娛樂和業餘訓練', '標準尺寸，拍面防滑處理', '家庭、社區',
             '雙魚', 160, 35),
            ('009', '健身手套', '防滑耐磨，保護手部，適合各種健身活動', '多種尺寸，通風設計', '健身房、戶外運動',
             'Under Armour', 120, 50),
            ('010', '護膝', '減少運動傷害，提供良好支撐與保護，適合籃球和足球運動', '彈性織物，可調整鬆緊',
             '籃球、足球及其他運動', '麥克戴維', 220, 40)
        ]

        # 插入資料到資料表
        cursor.executemany('''
        INSERT INTO products (product_id, product_name, description, specifications, usage, brand, price, stock_quantity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', products)

        # 提交變更以確保資料被儲存
        conn.commit()

    # 檢索並列印所有紀錄以驗證插入
    cursor.execute('SELECT * FROM products')
    all_rows = cursor.fetchall()

    conn.close()  # 關閉連線以釋放資源

    return all_rows

if __name__ == '__main__':
    # # 建立模擬的商品後台資料庫資訊
    create_and_populate_database()
    print('ok')