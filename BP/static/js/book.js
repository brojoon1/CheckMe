count = 0;
function hard_copy(num){
    res = 0
    for(res = 0;res<num;res++){

    }
    return res
}


function extend(num){
    //전부 다 줄임
    var all_sticker = document.querySelectorAll('.book_sticker');
    var is_extend = 1;

    var width = all_sticker[num - 1].offsetWidth;
    if (width > 500){
        is_extend = 0;  
    }

    for (var i = 0; i < all_sticker.length; i++) {
        var sticker = all_sticker[i];

        sticker.style.width = '230px';
    
        sticker.querySelector(".book_contents").style.marginTop = '0px';

        sticker.querySelector(".book_desc").style.height = '0px';
        sticker.querySelector(".book_desc").style.display = 'none';
    
        sticker.querySelector(".book_pict").style.height = '320px';
        sticker.querySelector(".book_pict").style.width = '230px';
    }

    //그 후 선택한 거 하나 늘림
    if(is_extend){
        selector(all_sticker[num - 1]);
    }
}

function selector(sticker){
    sticker.style.width = 'calc(100% - 60px)';

    sticker.querySelector(".book_contents").style.marginTop = '20px';
    
    sticker.querySelector(".book_desc").style.height = '300px';
    sticker.querySelector(".book_desc").style.display = 'block';

    sticker.querySelector(".book_pict").style.height = '430px';
    sticker.querySelector(".book_pict").style.width = '305px';
    
    setTimeout(() => scroll(sticker), 150);
}
function scroll(object){
    var yvalue = window.pageYOffset + object.getBoundingClientRect().top - 200
    var xvalue = window.pageYOffset + object.getBoundingClientRect().left
    window.scrollTo({ left: xvalue, top: yvalue, behavior: "smooth" })
}

function add_sticker(cover, title, author, desc, url, num){
    count = count * 1 + 1;
    document.querySelector(".count").value = count;
    book_sticker = document.createElement('div');
    book_sticker.className = 'book_sticker';
    book_sticker.onclick = function(){
        extend(num);
    }

        book_pict = document.createElement('div');
        book_pict.className = 'book_pict';
            book_pict_img = document.createElement('img');
            book_pict_img.alt = "이미지";
            book_pict_img.src = cover;
        book_pict.appendChild(book_pict_img)
    book_sticker.appendChild(book_pict)

        book_contents = document.createElement('div');
        book_contents.className = 'book_contents';

            book_name = document.createElement('div');
            book_name.className = 'book_name';
                book_name_text = document.createTextNode(title);
            book_name.appendChild(book_name_text)
        book_contents.appendChild(book_name)

            book_auth = document.createElement('div');
            book_auth.className = 'book_auth';
                book_auth_text = document.createTextNode(author);

            book_auth.appendChild(book_auth_text)
        book_contents.appendChild(book_auth)

            book_desc = document.createElement('div');
            book_desc.className = 'book_desc';
                book_desc_text = document.createTextNode(desc);
                    book_desc_a = document.createElement('a');
                    book_desc_a.href = url;
                        book_desc_a_button = document.createElement('button');
                        book_desc_a_button.style.width = "120px";
                        book_desc_a_button.style.margin = "40px 200px 0px 200px";
                        book_desc_a_button.className = "button_1";
                            button_text = document.createTextNode("자세히 보기")
                        book_desc_a_button.appendChild(button_text)

                    book_desc_a.appendChild(book_desc_a_button)
                book_desc.appendChild(book_desc_text)
            book_desc.appendChild(book_desc_a)
        book_contents.appendChild(book_desc)

    book_sticker.appendChild(book_contents)
    document.querySelector(".books").appendChild(book_sticker)
}

window.addEventListener('message', function(event){
    console.log(event)
    if(event.data[0] == 'add'){
        cover = event.data[1];
        title = event.data[2];
        author = event.data[3];
        desc = event.data[4];
        url = event.data[5];
        num = event.data[6];
        add_sticker(cover, title, author, desc, url, num);
    }else if(event.data[0] == 'kill'){
        document.querySelector("iframe").remove()
        is_loading = 0
        hideLoading()
    }
});
  
  

function loading(){
    is_loading = 1
    showLoading()
    count = document.querySelector(".count").value
    iframe = document.createElement('iframe');
    iframe.style.visibility = 'hidden';
    iframe.src = document.querySelector('.urls').value + count;

    document.querySelector("body").appendChild(iframe)
}

function book_scroll(now){
    var window_h = window.innerHeight;
    var max = document.documentElement.clientHeight;
    if (now + window_h + 500 > max && is_loading == 0) {
        is_loading = 1
        loading()
    }
}

function startLoading(){
    var loadingText = document.getElementById('loadingText');
    var dotCount = 0;
    var loadingInterval = setInterval(function() {
        dotCount++;
        var dots = '';
        for (var i = 0; i < dotCount % 4; i++) {
            dots += '.';
        }
        loadingText.textContent = 'Loading' + dots;

        if (dotCount === 3) {
            dotCount = 0;
        }
    }, 300);
}

function showLoading() {
    var loadingText = document.getElementById('loadingText');
    loadingText.style.display = 'block';
}

function hideLoading(){
    var loadingText = document.getElementById('loadingText');
    loadingText.style.display = 'none';
}


window.onscroll = function(){
    var now = window.scrollY;
    scroll_event(now);
    book_scroll(now);
    showscroller(now);
}

function search(){
    form = document.querySelector('#search');
    form.submit();
}