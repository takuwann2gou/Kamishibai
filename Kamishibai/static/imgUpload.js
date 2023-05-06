$(function() {
    var dropArea = $('.drop-area');
    
// ドラッグ&ドロップされたときの処理
dropArea.on('dragover', function(e) {
    // デフォルト処理を停止
    e.stopPropagation();
    e.preventDefault();
    $(this).css('border-color', '#333');
});
dropArea.on('dragleave', function(e) {
    // デフォルト処理を停止
    e.stopPropagation();
    e.preventDefault();
    $(this).css('border-color', '#ccc');
});
dropArea.on('drop', function(e) {
    // デフォルト処理を停止
    e.stopPropagation();
    e.preventDefault();
    $(this).css('border-color', '#ccc');

    //保存
    var files = e.originalEvent.dataTransfer.files;
    var formData = new FormData();
    formData.append('file', files[0]);

    console.log('formData:', formData);
    console.log('files:', files);


    $.ajax({
        url: '/upload_audio',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function() {
            location.reload();
        },
        error: function() {
            alert('アップロードに失敗しました。');
        }
    });

    $.ajax({
        url: '/upload_image',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function() {
            location.reload();
        },
        error: function() {
            alert('アップロードに失敗しました。');
        }
    });
});
});

// ファイル選択されたときの処理
var fileInput = $('#file-input');
fileInput.on('change', function() {
    var formData = new FormData($('#upload-form')[0]);

    $.ajax({
        url: '/upload_audio',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function() {
            location.reload();
        },
        error: function() {
            alert('アップロードに失敗しました。');
        }
    });
});

window.onload = function() {
	// ul要素を取得する
	var audioList = document.getElementById("audioList");

	// audiosフォルダ内の音声ファイルを取得する
	fetch("audios/")
	.then(response => response.text())
	.then(data => {
		// 取得したデータをHTMLに変換する
		var parser = new DOMParser();
		var html = parser.parseFromString(data, "text/html");

		// HTMLからリンク要素を取得する
		var links = html.getElementsByTagName("a");

		// リンク要素を順に処理する
		for(var i = 0; i < links.length; i++) {
			var link = links[i];

			// 音声ファイルのみを処理する
			if(link.href.endsWith(".mp3") || link.href.endsWith(".wav")) {
				// li要素を作成する
				var li = document.createElement("li");

				// a要素を作成する
				var a = document.createElement("a");
				a.href = link.href;
				a.innerHTML = link.innerHTML;
				a.onclick = function() {
					// 音声ファイルを再生する
					var audio = new Audio(this.href);
					audio.play();
					return false;
				}

				// li要素にa要素を追加する
				li.appendChild(a);

				// ul要素にli要素を追加する
				audioList.appendChild(li);
			}
		}
	})
	.catch(error => {
		console.error("Error:", error);
	});
};

