from flask import Flask, render_template, request, redirect, url_for, flash
from IPython.display import Audio, display
import os,json

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

### 汎用関数定義 ###

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
# スライドショー用のJSONオブジェクトを取得する関数を定義
def get_slideshow():
    images = get_image_list()
    slideshow = []
    for i, image in enumerate(images):
        slide = {
            'id': i,
            'filename': image,
            'order': i
        }
        slideshow.append(slide)
    return slideshow


### ページ定義 ###

# トップページのエンドポイントを定義
@app.route('/')
def index():
    images = get_image_list()
    audios = get_audio_list()
    #display_audio_list()
    # HTMLに変数として要素を渡す。
    return render_template('home.html', images=images, audios=audios,get_audio_type=get_audio_type)

#　スライドショーのエンドポイントを定義
@app.route('/slide', methods=['GET', 'POST'])
def slide():
    images = get_image_list()
    #JSONの格納
    with open('Kamishibai\static\slides.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
    slides = data['senkanosousou']
    return render_template('slide.html', images=images,slides=slides)



### アップロード ###

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

# スライドショーの順番を変更するエンドポイントを定義
@app.route('/slideshow/update_order', methods=['POST'])
def update_slideshow_order():
    data = request.json
    slideshow = data['slideshow']
    for slide in slideshow:
        filename = slide['filename']
        order = slide['order']
        src = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename)
        dst = os.path


##　音声用の追加関数　##

def get_audio_type(filename):
    _, ext = os.path.splitext(filename)
    if ext.lower()[1:] in ALLOWED_AUDIO_EXTENSIONS:
        return ext.lower()[1:]
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)