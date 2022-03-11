# 載入所需

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import requests

# 建立存放圖片資料夾

# 建立資料夾並確認是否重複 如有重複就換一種資料夾名稱
def makefolder(folername):
    a = 1   # 設定次數
    Paths = folername + str(a) # 設定資料夾名稱
    while True: 
        if not os.path.exists(Paths):   # 偵測是否有一樣的資料夾名稱 如果沒有一樣的資料夾名稱就建立
            os.mkdir(Paths) # 建立資料夾
            return Paths    # 回傳並跳出迴圈
        else:   # 如有資料夾名稱存在
            Paths = Paths.replace(str(a), str(a+1)) # 就把資料夾名稱後的數字加1
            a += 1  # 把變數加1

# 使用 Chrome 的 WebDriver

PATH = "chromedriver的路徑" # 將 chromedriver的路徑 換成driver所在的檔案位置 
driver = webdriver.Chrome(PATH) # 設定chromedriver為變數driver

# 開啟首頁

url = 'https://pic.sogou.com/'  # 開啟搜尋圖片網站（請不要換網址，因為是為該網站設計的）
driver.get(url) # 開啟網站

# 搜尋

sctpname = input("要搜尋的圖片是？")    # 詢問要搜尋的圖片
sctp = driver.find_element(by=By.NAME, value="query")   # 找到搜尋欄的位置
sctp.clear()    # 清空搜尋欄（怕上面有字）
sctp.send_keys(sctpname)    # 輸入搜尋
sctp.send_keys(Keys.RETURN) # 按下enter

# 建立資料夾和下載圖片

if Paths := makefolder(sctpname): # 執行建立資料夾並判斷是否成功
    bers = '//*[@id="picPc"]/div/div[2]/div/ul/li[nubers]/div/a[1]/img' # 這是xpath 用於定位每張圖片
    
    # 設定變數

    errorno = 0 # 偵測錯誤次數（底下有寫原因）
    numbera = 1 # 第幾張圖

    # 迴圈

    while True:
        
        try:
            mbers = bers.replace("nubers", str(numbera))    # 設定圖片xpath位置 nubers是放第幾張圖
            xpurl = driver.find_element(by=By.XPATH, value=mbers)   # 定義xpath
            url = xpurl.get_attribute("src")    # 取得該xpath的src變數中的網址
            
            # 印出資訊

            print("---" + str(numbera) + "---" )
            print(mbers)
            print(xpurl)
            print(url)
            print("---------")

            # 圖片存擋

            target = driver.find_element(by=By.XPATH, value=mbers)  # 設定圖片xpath位置 nubers是放第幾張圖
            r = requests.get(url)   # 取得網址中的圖片
            with open(Paths +"/"+ sctpname +" ("+ str(numbera) +").png", "wb") as f:    # 開啟資料夾（自動創建的）
                f.write(r.content)  # 儲存圖片
            driver.execute_script("arguments[0].scrollIntoView();", target) # 定位圖片（如果沒定位得話可能會沒載入到圖片 導致存到一半就退出）
            numbera += 1# 下一張
            errorno = 0    # 成功執行所以歸零錯誤次數
            
        # 發生錯誤

        except:
            
            if errorno > 30:    # 如果錯超過30次就退出
                break
            
            # 回報底幾個錯誤（通常是推薦搜尋的xpath格式一樣所以造成錯誤 和所有圖片都抓完後找不到了）

            # 印出錯誤

            print("---" + str(numbera) + "---" )
            print("發生錯誤")   
           
            numbera += 1    # 變數加1（直接下一張）
            errorno += 1    # 紀錄錯誤次數（超過30次就退出）

driver.quit()   # 關閉chromedriver