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

    $.ajax({
        url: '/upload',
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

// ファイル選択されたときの処理
var fileInput = $('#file-input');
fileInput.on('change', function() {
    var formData = new FormData($('#upload-form')[0]);

    $.ajax({
        url: '/upload',
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