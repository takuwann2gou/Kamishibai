from flask import Flask, render_template, request, redirect, url_for
import mimetypes
import os

app = Flask(__name__, template_folder='templates')

# 画像が保存されるディレクトリを指定
UPLOAD_FOLDER_IMG = 'Kamishibai/static/images'
UPLOAD_FOLDER_AUD = 'Kamishibai/static/audios'
app.config['UPLOAD_FOLDER_IMG'] = UPLOAD_FOLDER_IMG
app.config['UPLOAD_FOLDER_AUD'] = UPLOAD_FOLDER_AUD

#Index
@app.route('/')
def index():
    # 画像ファイルの一覧を取得
    images = os.listdir(app.config['UPLOAD_FOLDER_IMG'])
    # 画像ファイルの一覧を取得
    audios = os.listdir(app.config['UPLOAD_FOLDER_AUD'])
    return render_template('home.html', images=images,audios=audios)



@app.route('/upload', methods=['POST'])
def upload():
        
### イメージ ###

        # アップロードされたファイルを保存
        img_file = request.files['file']
        filename = img_file.filename
        img_file.save(os.path.join(app.config['UPLOAD_FOLDER_IMG'], filename))# ファイルを保存する

# ### オーディオ　###

#         # アップロードされたファイルを保存
#         audio_file = request.files['audio_file']
#         filename = audio_file.filename
#         audio_file.save(os.path.join(app.config['UPLOAD_FOLDER_AUD'],filename))# ファイルを保存する
#         return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

