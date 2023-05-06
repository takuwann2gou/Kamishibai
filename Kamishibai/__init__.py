from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# 画像が保存されるディレクトリを指定
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # 画像ファイルの一覧を取得
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('home.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    # アップロードされたファイルを保存
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
