from flask import Flask, render_template, jsonify, url_for, send_from_directory
import pandas as pd
import random
import os
from datetime import datetime

app = Flask(__name__)

# 保存時間戳的全局變量，用於確保下載檔案名和伺服器上的檔案一致
draw_results = {}

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for the draw page, including second stage data
@app.route('/draw/<page_name>')
def draw_page(page_name):
    title = f"113年度臺北市國語文競賽-{page_name}抽籤作業"
    
    # 將名單的路徑改為 lists 資料夾中
    file_path = os.path.join('lists', f'{page_name}.xlsx')
    df = pd.read_excel(file_path)
    df['參加項目'] = page_name
    df.insert(0, '序位', range(1, len(df) + 1))  # 自動填入序位
    data = df.drop(columns=['編號']).to_dict(orient='records')
    
    # 加载第二階段名單
    second_stage_file_path = os.path.join('lists', f'{page_name}(第二階段).xlsx')
    if os.path.exists(second_stage_file_path):
        df_second_stage = pd.read_excel(second_stage_file_path)
        df_second_stage['參加項目'] = page_name
        second_stage_data = df_second_stage.drop(columns=['編號']).to_dict(orient='records')
    else:
        second_stage_data = []

    return render_template('draw_page.html', title=title, data=data, second_stage_data=second_stage_data, draw_button_text="第1次抽籤", page_name=page_name)

# Route to handle drawing
@app.route('/draw/<page_name>/<int:draw_count>')
def draw(page_name, draw_count):
    file_path = os.path.join('lists', f'{page_name}.xlsx')
    df = pd.read_excel(file_path)
    df['參加項目'] = page_name
    df = df.sample(frac=1).reset_index(drop=True)
    df.insert(0, '序位', range(1, len(df) + 1))
    data = df.drop(columns=['編號']).to_dict(orient='records')
    
    if draw_count == 3:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # 生成唯一的時間戳
        output_filename = f'{page_name}抽籤結果_{timestamp}.xlsx'
        output_path = os.path.join('results', output_filename)
        df.drop(columns=['編號']).to_excel(output_path, index=False)  # 生成的 Excel 刪除「編號」欄位
        draw_results[page_name] = output_filename  # 保存生成的檔案名

    return jsonify(data)

# Route to handle downloading after the third draw
@app.route('/download/<page_name>')
def download(page_name):
    # 從保存的字典中獲取檔案名，確保下載連結與實際檔案一致
    output_filename = draw_results.get(page_name, None)
    if output_filename:
        return jsonify({"download_url": url_for('download_file', filename=output_filename)})
    else:
        return jsonify({"error": "無法找到檔案"}), 404

# Serve the file from the results folder
@app.route('/results/<filename>')
def download_file(filename):
    return send_from_directory('results', filename)

if __name__ == '__main__':
    if not os.path.exists('results'):
        os.makedirs('results')
    app.run(debug=False)
