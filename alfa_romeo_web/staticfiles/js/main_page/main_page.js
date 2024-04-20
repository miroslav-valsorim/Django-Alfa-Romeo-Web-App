
// Top of page button >>
let upButton = document.getElementById("up-btn");
upButton.style.display = "none";

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    upButton.style.display = "block";
  } else {
    upButton.style.display = "none";
  }
}


function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}
// Top of page button <<

// Image slider >>
var i = 0;
var images = [];
var slideTime = 9000; // 9 seconds

images[0] = '/static/images/background.jpg';
images[1] = '/static/images/goodwood-47.jpg';
images[2] = '/static/images/cofani-aperti-3.jpg';

function changePicture() {
    var contentElement = document.querySelector('.background');
    contentElement.style.opacity = '0';
    setTimeout(function() {
        contentElement.style.backgroundImage = "linear-gradient(rgba(0,0,0,0.65),rgba(0,0,0,0.65)), url(" + images[i] + ")";
        setTimeout(function() {
            contentElement.style.opacity = '1';
        }, 20);
    }, 500);

    if (i < images.length - 1) {
        i++;
    } else {
        i = 0;
    }
    setTimeout(changePicture, slideTime);
}


window.onload = changePicture;
// Image slide <<