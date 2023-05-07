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