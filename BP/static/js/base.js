function call_sidenav(){
    document.querySelector('.sidenav_caller').style.marginLeft = '-100px';
    document.querySelector('.sidenav').style.marginLeft = '0px';
}
function kill_sidenav(){
    document.querySelector('.sidenav').style.marginLeft = '-300px';
    document.querySelector('.sidenav_caller').style.marginLeft = '20px';
}

var prev = 0

function scroll_event(now){
    kill_sidenav()
    if(now<=200.0){
        document.querySelector('.topnav').style.marginTop = '0px';
    }else if(now<prev){
        document.querySelector('.topnav').style.marginTop = '0px';
    }else{
        document.querySelector('.topnav').style.marginTop = '-75px';
    }
    prev = now;
}

function showscroller(num){
    // 페이지를 조금이라도 내리면 스크롤 버튼 보이기
    var scrollButton_main = document.getElementById('scrollButton_main');

    if (num > 0) {
        scrollButton_main.style.opacity = "1.0";
    } else {
        scrollButton_main.style.opacity = "0.0";
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

window.onscroll = function(){
    var now = window.scrollY;
    scroll_event(now);
    showscroller(now);
}