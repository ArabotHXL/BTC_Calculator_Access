# 安装必要的库
!pip install pandas numpy 
!pip install inquirer
!pip install ipywidgets --upgrade

import gspread
from google.colab import auth
from google.auth import default
import os

# Step 1: 授权 Google Drive 访问
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# Step 2: 打开 Google Sheets 读取 Token 和用户数据
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/15maOE_0HzWA5upDmlYAK61GPVKUrhX6NURbmQcB5N2w/edit?gid=0#gid=0'  # 替换为您的 Google Sheets 链接
info_sheet = gc.open_by_url(spreadsheet_url).worksheet('客户信息')
token_sheet = gc.open_by_url(spreadsheet_url).worksheet('Token')

# Step 3: 验证客户身份并获取 Unique ID
def verify_access(email):
    for subscriber in info_sheet.get_all_records():
        if subscriber['Email'] == email and subscriber['Access Granted'] == '✅':
            print(f"✅ 欢迎 {subscriber['Email']}！您已获得访问权限。")
            return subscriber['Unique ID']  # 返回 Unique ID 作为密钥
    print("❌ 抱歉，您尚未获得访问权限。请联系管理员。")
    return None

# Step 4: 匹配 Unique ID 并找到 Token
def get_token_by_unique_id(unique_id):
    token_data = token_sheet.get_all_records()
    for token_entry in token_data:
        if token_entry['Unique ID'] == unique_id:
            return token_entry['Token']
    print("❌ 未找到对应的 Token，请联系管理员。")
    return None

# Step 5: 用户输入邮箱并验证
user_email = input("请输入您的邮箱: ")
user_id = verify_access(user_email)

# Step 6: 使用 Token 克隆仓库并执行计算器
if user_id:
    GITHUB_TOKEN = get_token_by_unique_id(user_id)
    if GITHUB_TOKEN:
        os.environ['GITHUB_TOKEN'] = GITHUB_TOKEN
        !git clone https://$GITHUB_TOKEN@github.com/ArabotHXL/BTC.git BTC_Calculator

        # Step 7: 执行计算器
        %cd BTC_Calculator
        %run mining_profit_calculator.py

        # Step 8: 安全删除 Token
        del os.environ['GITHUB_TOKEN']
        print("✅ Token 已安全删除，访问已完成。")
    else:
        print("❌ 未找到对应的 Token，请联系管理员。")
else:
    print("❌ 无法访问，请联系管理员。")
