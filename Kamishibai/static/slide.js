var index = 0;
var images = document.getElementById('slideshow').getElementsByTagName('img');

function startSlideshow() {
    setInterval(nextImage, 3000);
}

function nextImage() {
    images[index].style.display = 'none';
    index = (index + 1) % images.length;
    images[index].style.display = 'block';
}

$(function() {
    // 画像がクリックされた時の処理
    $('.card-img-top').on('click', function() {
      // クリックされた画像のURLを取得
      var imageUrl = $(this).attr('src');
  
      // プレビュー表示部分に画像を表示
      $('#slide-preview').attr('src', imageUrl);
      $('#slide-preview').show();
    });
  });