# 國語文競賽第一階段抽籤系統 
開發者：臺北市立建國高級中學 圖書館潘威歷主任

本專案是一個基於 Flask 的網頁應用，能夠為113年度及114年度臺北市國語文競賽的第一階段決賽選手進行公平的抽籤排序，並可下載結果 Excel。

## 功能特色
- 讀取 `lists/` 資料夾中的 Excel 選手名單
- 進行 3 次隨機抽籤
- 生成 Excel 檔案並存放於 `results/`
- 提供 PDF 列印功能，隱藏部分姓名以保護隱私（如「王鈞」變為「王O」，「諸葛孔明」變為「諸OO明」）

## 安裝與運行

### 1. 克隆此專案
```bash
git clone https://github.com/weilipan/chinese-language-competition-firstround.git
cd your-repo-name
```

### 2. 創建虛擬環境並安裝依賴

本專案需要以下 Python 套件：
- Flask
- pandas
- openpyxl

請依照以下步驟安裝：

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 3. 運行 Flask 伺服器
```bash
python app.py
```
在瀏覽器中打開 `http://127.0.0.1:5000/` 來使用應用程式。

## 檔案結構
```
國語文競賽抽籤系統/
│── lists/                  # 存放 Excel 名單
│── results/                # 存放抽籤結果
│── static/                 # 存放靜態文件 (CSS, JS, 圖片)
│── templates/               # 存放 HTML 模板
│── app.py                   # Flask 主程式
│── requirements.txt         # 依賴套件清單
│── README.md                # GitHub 專案說明文件
│── .gitignore               # 忽略不需要提交的文件
```

## 主要功能說明

### **首頁 (`index.html`)**
- 提供組別以list資料夾內的Excel檔（檔案內容請依照欄位自行更新）來製作的抽籤連結。
- 點擊對應連結後，進入該組別的抽籤頁面

### **抽籤頁面 (`draw_page.html`)**
- 顯示該組別的選手名單
- 點擊「第 1 次抽籤」按鈕進行第一次抽籤，結果隨機排列
- 進行第 2、3 次抽籤，每次都重新排序
- 第 3 次抽籤完成後，允許下載 Excel 或列印 PDF
- PDF 下載時，將姓名部分遮蔽以保護隱私
- 請注意有部份競賽有逕入第二階段的選手，請程式也會一併呈現出來，以免在場學校代表以為沒有抽到籤。

### **後端 (`app.py`)**
- 讀取 `lists/` 目錄內的 Excel 檔案
- 執行 3 次抽籤（隨機排序）
- 產生抽籤結果並存入 `results/` 目錄
- 提供下載結果 Excel 的 API

## 貢獻指南
歡迎提交 Issue 或 Pull Request，以改進本專案。

## License
本專案採用 MIT License，詳見 `LICENSE` 文件。
