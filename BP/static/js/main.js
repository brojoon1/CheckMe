function topbar_op(num){
    // 페이지를 조금이라도 내리면 스크롤 버튼 보이기
    var topnav = document.querySelector('.topnav');

    if (num > 0) {
        topnav.style.boxShadow = "0px 5px rgba(192, 192, 192, 1)";
        topnav.style.backgroundColor = "rgba(235, 228, 205, 1)";
    } else {
        topnav.style.boxShadow = "0px 5px rgba(192, 192, 192, 0)";
        topnav.style.backgroundColor = "rgba(235, 228, 205, 0)";
    }
}


window.onscroll = function(){
    var now = window.scrollY;
    scroll_event(now);
    showscroller(now);
    topbar_op(now);
}