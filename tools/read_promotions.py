def read_store_promotions(product_name):
    # 指定優惠政策文件的檔案路徑
    file_path = 'store_promotions.txt'

    try:
        # 開啟檔案並逐行讀取內容
        with open(file_path, 'r', encoding='utf-8') as file:
            promotions_content = file.readlines()

        # 搜尋包含商品名稱的行
        filtered_content = [line for line in promotions_content if product_name in line]

        # 回傳符合條件的行，若未找到則回傳預設訊息
        if filtered_content:
            return ''.join(filtered_content)
        else:
            return "沒有找到關於該商品的優惠政策。"
    except FileNotFoundError:
        # 檔案不存在的錯誤處理
        return "優惠政策文件未找到，請檢查檔案路徑是否正確。"
    except Exception as e:
        # 其他潛在錯誤的處理
        return f"讀取優惠政策文件時發生錯誤: {str(e)}"


if __name__ == '__main__':

    # 重新建立一個包含店鋪優惠政策的文字檔
    promotions_content = """
    店鋪優惠政策：
    1. 足球 - 購買足球即可享受9折優惠。
    2. 羽毛球拍 - 任意購買羽毛球拍兩支以上，享8折優惠。
    3. 籃球 - 單筆訂單滿300元，籃球半價。
    4. 跑步鞋 - 第一次購買跑步鞋的顧客可享受滿500元折100元優惠。
    5. 瑜伽墊 - 每購買一張瑜伽墊，贈送價值50元的瑜伽指南影片一套。
    6. 速乾運動衫 - 買三送一，贈送的為最低價商品。
    7. 電子計步器 - 購買任意電子計步器，贈送配套手機APP永久會員資格。
    8. 乒乓球拍套裝 - 乒乓球拍套裝每套95折。
    9. 健身手套 - 滿200元免運費。
    10. 護膝 - 每件商品附贈運動護膝一個。
    
    注意：
    - 所有優惠活動不可與其他優惠同享。
    - 優惠詳情以實際到店或下單時為準。
    """

    # 將優惠政策寫入檔案
    file_path = './store_promotions.txt'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(promotions_content)

    print(file_path)