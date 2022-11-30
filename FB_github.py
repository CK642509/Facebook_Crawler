#!/usr/bin/env python
# coding: utf-8

# # 1. 開啟瀏覽器，進到FB首頁

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd


# 關閉通知
options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values':
        {
            'notifications': 2
        }
}
options.add_experimental_option('prefs', prefs)
options.add_argument("disable-infobars")


# 打啟動selenium 務必確認driver 檔案跟python 檔案要在同個資料夾中
# 在這邊下載: https://chromedriver.chromium.org/downloads
driver = webdriver.Chrome(options=options)
driver.get("https://www.facebook.com/")
time.sleep(4)


email = "your_email"
password = "your_password"

#輸入 email 
context = driver.find_element(By.ID, 'email')
context.send_keys(email)
time.sleep(0.5)

#輸入 password
context = driver.find_element(By.ID, 'pass')
context.send_keys(password)
time.sleep(0.5)

# 登入
commit = driver.find_element(By.NAME, 'login')
commit.click()
time.sleep(7)
print("已登入")


# # 2. 進入台大交流版
# ## 2.1 手動選擇「最新貼文」

"""
# 進入交流版
driver.get("https://www.facebook.com/groups/NTU.Head")

# 選擇最新貼文 (預設是熱門貼文)
# 點開選項
commit = driver.find_element(By.XPATH, "//div[@class='j83agx80']//span[@class='a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7']")
commit.click()

# 三個選項，依序是「最新動態」、「最近貼文」、「最相關貼文」，選第二個
commit = driver.find_elements(By.XPATH, "//div[@class='bp9cbjyn j83agx80 btwxx1t3 buofh1pr i1fnvgqd hpfvmrgz']")
commit[1].click()
"""

# ## 2.2 自動以「最新貼文」排序
# 進入交流版 (以最新貼文排序) (取代上兩格)
driver.get("https://www.facebook.com/groups/NTU.Head?sorting_setting=CHRONOLOGICAL")


# # 3. 展開頁面
# ## 3.1 往下滑以顯示更多篇文章

# 往下滑
for i in range(0,5):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
print("滑好了")


# ## 3.2 點開「顯示更多」

# 點「顯示更多」 (要設兩層條件，因為貼文者那邊 其他6人也是div後面這個class) (要多執行幾次 直到數字不便)
commit = driver.find_elements(By.XPATH, "//div[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p' and @role='button']")
print(len(commit))

for c in commit:
    try:
        c.click()
    except:
        print(c)

commit = driver.find_elements(By.XPATH, "//div[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p' and @role='button']")
if len(commit) == 0:
    print("都點開了")
else:
    print("點開了")


# ## 3.3 將游標移至「時間」上，以方便後續獲取貼文連結
urls = driver.find_elements(By.XPATH, "//div[@class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']//span[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']//a[@role='link']")
print(len(urls))

action = ActionChains(driver)
for url in urls:
    action.move_to_element(url).perform()
print("OK")


# # 4. 擷取網頁資料
# ## 4.1 擷取並解析 HTML

html = etree.HTML(driver.page_source)
soup = BeautifulSoup(driver.page_source, "html.parser")


# ## 4.2 選擇貼文區

# 貼文區是 role=feed，只會有一個
all_ = soup.find_all("div", role="feed")
print(len(all_))


# ## 4.3 獲取文章資訊
# ### 4.3.1 以一篇文章為單位，獲取「作者」、「時間」、「連結」、「內容」

# 一篇PO文
# div class_="du4w35lb k4urcfbm l9j0dhe7 sjgh65i0"
# 文字的部分
# div class_="ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a" (比"qzhwtbm6 knvmm38d"層級高)
# div class_="dati1w0a ihqw7lf3 hv4rvrfc ecm0bbzt"
# 每篇PO文的重要訊息們 (一般是3個)
# div class_="qzhwtbm6 knvmm38d"


all_2 = all_[0].find_all("div", class_="du4w35lb k4urcfbm l9j0dhe7 sjgh65i0")
print(len(all_2))

name_list = []
time_list = []
url_list = []
content_list = []

for i in range(len(all_2)):
    # inform 前2個固定是名字和時間，但後面數量不一定，依貼文形式而定
    inform = all_2[i].find_all("div", class_="qzhwtbm6 knvmm38d")
    print(i)
    #print("inform", len(inform))

    
    # 名字 name
    n = inform[0].find_all("h2")
    name = n[0].find("span").text
    print(name)
    name_list.append(name)

    # 時間 time
    t = inform[1].find_all("a", class_ = "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw")
    time = t[0].find("span").text.strip("=")
    print(time)
    time_list.append(time)
    
    # 文章連結 url (滑鼠游標移到上面之後 HTML裡才會有，不然都是#)
    url = t[0].get("href")
    print(url)
    url_list.append(url)
    
    # 內容 content
    try:
        c = inform[2].find_all("div", dir="auto")
        
        # 如果貼文的是一群人分享文章就會進到這邊
        if len(c) == 0:
            words = all_2[i].find_all("div", class_="dati1w0a ihqw7lf3 hv4rvrfc ecm0bbzt")
            w = words[0]
            # print(w.text)
            content_list.append(w.text)
        
        # 一般文章走這邊
        else:
            txt = ""
            for t in c:
                # print(t.text)
                txt += t.text     # 把不同行的內容結合在一起
            content_list.append(txt)

    except:
        # 如果貼文的是一群人單純 PO 文章就會進到這邊
        try:
            words = all_2[i].find_all("div", class_="dati1w0a ihqw7lf3 hv4rvrfc ecm0bbzt")
            w = words[0]
            # print(w.text)
            content_list.append(w.text)
        
        except:
            print("Ooops")
            content_list.append("No content")

    print("\n")

print(len(name_list))
print(len(time_list))
print(len(url_list))
print(len(content_list))


# ### 4.3.2 列印出前3組資料

for i in range(3):
    try:
        print(name_list[i])
        print(time_list[i])
        print(url_list[i])
        print(content_list[i])
        print("\n")
    except:
        pass


# ### 4.3.3 檢查社團內PO文是否有關鍵字

keywords = ["免費", "便當", "剩下", "飲料"]
count = 0

# 依序添加「姓名」「時間」
dict = {"name":name_list, "time":time_list}

# 若「內容」含有關鍵字，則打勾，反之則留空 (不含分享的文章內容)
for keyword in keywords:
    has_keyword = []
    for i in range(len(content_list)):
        if keyword in content_list[i]:
            count += 1
            has_keyword.append("V")
        else:
            has_keyword.append(" ")
    dict[keyword] = has_keyword

# 把「內容」、「連結」加在最後
dict["content"] = content_list
dict["url"] = url_list

print("在 " +str(len(content_list))+" 篇文中")
print("共發現 "+str(count)+" 篇文中含有關鍵字")
print("關鍵字:", keywords)

data = pd.DataFrame(dict)


# 建立一個清單，含有各個關鍵字的清單
data_list = [data.loc[data[keyword] == "V"] for keyword in keywords]

all_data = pd.concat(data_list)
all_data = all_data.sort_index()    # 這樣就會依照時間排序
print(all_data)
