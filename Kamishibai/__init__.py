from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
    # JSON文字列に変換して、テンプレートに渡す前にエスケープを回避
    slides = json.dumps(data['senkanosousou'])
    slides = json.loads(slides)
    return render_template('slide.html', images=images,slides=slides)



### 画像&音声のアップロード ###

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


##　スライドショーの更新　##

# @app.route('/save_slide', methods=['POST'])
# def save_slide():
#     data = request.get_json()
#     selected_image_url = request.form['selected_image_url']
#     for slide in data['senkanosousou']:
#         if slide['image_url'] == selected_image_url:
#             slide['image_url'] = selected_image_url
#     with open('slides.json', 'w') as f:
#         json.dump(data, f)
#     return jsonify(success=True)

# @app.route('/save_slide', methods=['POST'])
# def save_slide():
#     #データの展開と上書き
#     data = request.get_json() # POSTされたJSONを取得
#     print(data)  # 取得したJSONを確認
#     try:
#         order = data['order']
#         image_url = data['image_url']
#         with open('Kamishibai/static/slides.json', 'r') as f:
#             slides = json.load(f) # 既存のJSONファイルを読み込み
#         for slide in slides.values():
#             for s in slide:
#                 if s['order'] == order:
#                     s['image_url'] = image_url
#                     break
#         with open('Kamishibai/static/slides.json', 'w') as f:
#             json.dump(slides, f, indent=4, ensure_ascii=False) # JSONファイルを上書き
#         return jsonify({'success': True})
#     except:
#         return jsonify({'success': False})

@app.route('/save_slide', methods=['POST'])
def save_slide():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json.'}), 415

    request_data = request.get_json() # JSONを取得
    slides = request_data['data'] # JSONからリストを取得
    order = slides[0]['order']
    image_url = slides[0]['image_url']
    
    # slides.jsonの内容を読み込む
    with open('Kamishibai/static/slides.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 指定されたorderに対応する要素を検索してimage_urlを更新
    for i, slide in enumerate(data['senkanosousou']):
        if slide['order'] == order:
            data['senkanosousou'][i]['image_url'] = image_url
            break

    # 更新した内容をファイルに書き込む
    with open('Kamishibai/static/slides.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    return redirect(url_for('slide'))


# @app.route('/save_slide', methods=['POST'])
# def save_slide():
#     slides = request.get_json()#Json型をlistにして取得
#     with open('Kamishibai/static/slides.json', 'w') as f:
#         json.dump(slides, f)#List型をJson型にしてファイルを作成上書き
#     return jsonify({'success': True})


##　音声用の追加関数　##

def get_audio_type(filename):
    _, ext = os.path.splitext(filename)
    if ext.lower()[1:] in ALLOWED_AUDIO_EXTENSIONS:
        return ext.lower()[1:]
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)