from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)

# 画像ファイルが保存されるディレクトリを指定
UPLOAD_IMAGES_FOLDER = 'Kamishibai/static/images'
app.config['UPLOAD_IMAGES_FOLDER'] = UPLOAD_IMAGES_FOLDER

# 音声ファイルが保存されるディレクトリを指定
UPLOAD_AUDIOS_FOLDER = 'Kamishibai/static/audios'
app.config['UPLOAD_AUDIOS_FOLDER'] = UPLOAD_AUDIOS_FOLDER

# アップロードを許可するファイルの拡張子を指定
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'wav', 'mp3'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_images():
    # 画像ファイルの一覧を取得
    images = [f for f in os.listdir(app.config['UPLOAD_IMAGES_FOLDER']) if allowed_file(f)]
    # 音声ファイルの一覧を取得
    audios = [f for f in os.listdir(app.config['UPLOAD_AUDIOS_FOLDER']) if allowed_file(f)]
    return images, audios

@app.route('/')
def index():
    images, _ = get_images()
    return render_template('home.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    # アップロードされたファイルを保存
    file = request.files['file']
    if not file or not allowed_file(file.filename):
        flash('無効なファイル形式です。')
        return '''
        <script>
        alert("無効なファイル形式です。");
        window.location.href = "/";
        </script>
        '''
    filename = file.filename
    if filename.endswith(('mp4', 'wav', 'mp3')):
        file.save(os.path.join(app.config['UPLOAD_AUDIOS_FOLDER'], filename))
    else:
        file.save(os.path.join(app.config['UPLOAD_IMAGES_FOLDER'], filename))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)