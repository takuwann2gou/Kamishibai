from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 画像が保存されるディレクトリを指定
UPLOAD_FOLDER = os.path.join(app.static_folder, 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # 画像ファイルの一覧を取得
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('home.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    # アップロードされたファイルを保存
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        message = '無効なファイル形式です。'
        return f'''
        <script>
        alert("{message}");
        window.location.href = "/"; // リダイレクト先のURL
        </script>
        '''

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
