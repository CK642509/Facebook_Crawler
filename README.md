# Facebook_Crawler

## 緣起

每逢寒暑假，學校都會舉辦營隊，因此有時候會有多出來的免費便當、飲料等，營隊人員會將此資訊PO在FB社團中，讓有需要的同學自行前往取用。
但這些免費便當通常數量不多，通常在PO出文章30分鐘內就沒有了，也不會有事先預告，因此我們在午餐或是晚餐時間就會一直關注是否有新的PO文，
也因此就想要設計一個程式，可以自動分析FB社團PO文，自動篩選出含有特定關鍵字的貼文，方便我們第一時間掌握消息，並立刻前往領取免費便當。

## 主要遇到困難以及解決辦法
### 1. 文章不會一次顯示出來 (需要往下滑)

給予 javascript 的指令

`driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")`

再搭配for迴圈多執行幾次，即可獲得足夠多的文章

### 2. 文章的預設順序不是依照PO文時間 (需要改順序)

有兩種方法，一開始我是使用 `find_element()` 搭配 `click()` 點選選項進行調整

後來發現第二種方法，直接改個網址就好了，也就是在網址後面添加 `?sorting_setting=CHRONOLOGICAL`

### 3. 貼文連結的網址一開始不會顯示出來 

標籤一開始給予的網址是 # 

`href=#` 

後來發現滑鼠游標移到「時間」上之後，就會呈現出網址 (取代#) 

因此使用 `find_elements()` 搭配 `move_to_element()` 後，才開始擷取和分析 HTML

### 4. 文章內容不會一次全部顯示出來 (要點「顯示更多」)

使用 `find_elements()` 搭配 `click()` 點開

比較麻煩的是，不同貼文類型 (一般貼文、分享貼文、與很多一起的貼文...等) 在 HTML 架構上有差異，
比較難用 class 定位，這邊我選擇多加一層條件 `role='button'` ，並且對於無法點選的 element 直接用 try except 避開

## 安裝
### 1. 下載專案
```
git clone https://github.com/CK642509/Facebook_Crawler.git
```

- 若沒有安裝 git，也可以直接下載壓縮檔下來解壓縮就好
    - 下載方法：
        - 右上點選 code
        - 選擇 Download ZIP

### 2. 安裝 python 套件
```
pip install -r requirements.txt
```

### 3. 安裝 ChromeDriver
1. 在[這裡](https://chromedriver.chromium.org/downloads)下載 
2. 依據你的 chrome 版本選擇適當的 ChromeDriver
3. 下載後解壓縮，把檔案(`chromedriver.exe`)放進專案資料夾 (跟 `FB_github.ipynb`同個資料夾)

> ### **在哪裡查看 Chrome 版本？**
> 
> 打開 Chrome -> 設定 -> 關於 Chrome

### 4. 修改 FB 帳號密碼
- 程式碼內有段地方需要設定帳號密碼，需要改成自己的
    ```
    email = "your_email"
    password = "your_password"
    ```
### 5. 執行程式
```
python FB_github.py
```

- 或是用 jupyter notebook 開啟 `FB_github.ipynb`