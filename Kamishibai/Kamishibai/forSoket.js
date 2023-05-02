
// スライドが変更された場合、他のユーザーに通知する
slideshow.on('afterChange', function (event, slick, currentSlide, nextSlide) {
    socket.emit('slide-change', { index: currentSlide });
});
// BGMの再生状態が変更された場合、他のユーザーに通知する
bgm.on('play', function () {
    socket.emit('bgm-play');
});
bgm.on('pause', function () {
    socket.emit('bgm-pause');
});
bgm.on('stop', function () {
    socket.emit('bgm-stop');
});
// 効果音を再生する
$("#play-sound-effect-button").on('click', function () {
    socket.emit('play-sound-effect');
});