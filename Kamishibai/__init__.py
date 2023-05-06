from flask import Flask, render_template, request, redirect, url_for, flash
from IPython.display import Audio, display
import os

app = Flask(__name__)

# アップロードされた画像が保存されるディレクトリを指定
UPLOAD_IMAGE_FOLDER = 'Kamishibai/static/images'
app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER
# アップロードされた音声が保存されるディレクトリを指定
UPLOAD_AUDIO_FOLDER = 'Kamishibai/static/audios'
app.config['UPLOAD_AUDIO_FOLDER'] = UPLOAD_AUDIO_FOLDER

# アップロードを許可するファイルの拡張子を定義
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav'}


# 画像ファイルの一覧を取得する関数を定義
def get_image_list():
    images = []
    for file_name in os.listdir(UPLOAD_IMAGE_FOLDER):
        if file_name.endswith(tuple(ALLOWED_IMAGE_EXTENSIONS)):
            images.append(file_name)
    return images
# 音声ファイルの一覧を取得する関数を定義
def get_audio_list():
    audios = []
    for file_name in os.listdir(UPLOAD_AUDIO_FOLDER):
        if file_name.endswith(tuple(ALLOWED_AUDIO_EXTENSIONS)):
            audios.append(file_name)
    return audios


# トップページのエンドポイントを定義
@app.route('/')
def index():
    images = get_image_list()
    audios = get_audio_list()
    #display_audio_list()
    # HTMLに変数として要素を渡す。
    return render_template('home.html', images=images, audios=audios,get_audio_type=get_audio_type)


# 画像をアップロードするエンドポイントを定義
@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['file']
    filename = file.filename
    # ファイルが許可された拡張子であるか確認する
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS:
        file.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename))
    else:
        flash('無効なファイル形式です。')
    return redirect(url_for('index'))
# 音声ファイルをアップロードするエンドポイントを定義
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    file = request.files['file']
    filename = file.filename
    # ファイルが許可された拡張子であるか確認する
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS:
        file.save(os.path.join(app.config['UPLOAD_AUDIO_FOLDER'], filename))
    else:
        flash('無効なファイル形式です。')
    return redirect(url_for('index'))


##　音声用の追加関数　##

#　音声再生用
# def display_audio_list():
#     audio_list = get_audio_list()
#     for file_name in audio_list:
#         file_path = os.path.join(UPLOAD_AUDIO_FOLDER, file_name)
#         display(Audio(file_path, autoplay=False))
#         # autoplayで自動再生を防いでいます
#　音声拡張子フィルター
def get_audio_type(filename):
    _, ext = os.path.splitext(filename)
    if ext.lower()[1:] in ALLOWED_AUDIO_EXTENSIONS:
        return ext.lower()[1:]
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)