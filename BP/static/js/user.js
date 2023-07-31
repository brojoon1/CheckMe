function validateForm() {
    var id = document.forms["registerForm"]["username"].value;
    var password1 = document.forms["registerForm"]["password1"].value;
    var password2 = document.forms["registerForm"]["password2"].value;
    var email_front = document.forms["registerForm"]["email_front"].value
    var email_back = document.forms["registerForm"]["custom_domain"].value;
    var nickname = document.forms["registerForm"]["nickname"].value;
    var name = document.forms["registerForm"]["name"].value;
    var phone = document.forms["registerForm"]["phone"].value;
    var term_agree = document.querySelector('#agreed').checked * 1



    var id_message = document.querySelector(".id_message").innerHTML;
    if(id_message != '사용 가능한 아이디입니다.'){
        alert("아이디를 확인해주십시오.");
    }else if(passwd_check() == 0){
        alert("비밀번호를 확인해주십시오.");
    }else if(term_agree == false){
        alert("개인정보처리방침에 동의하셔야 합니다.");
    }else if (id == "" || password1 == "" || password2 == "" || email_front == "" || email_back == "" || nickname == "" || name == "" || phone == "") {
        alert("필수 항목을 모두 작성해야 합니다.");
    }else{
        document.querySelector(".form_container").querySelector("form").submit()
    }
}

// 도메인 선택 시 custom_domain 필드 업데이트
function email_select(){
    var domainChoice = document.getElementById("id_domain_choice").value;
    if (domainChoice === "custom") {
        document.getElementById("id_custom_domain").disabled = false;
    } else {
        document.getElementById("id_custom_domain").disabled = true;
        document.getElementById("id_custom_domain").value = domainChoice;
    }
}

function activate(num){
    sticker = document.querySelectorAll('.ganre_selecter')[num - 1];
    total = document.querySelector('#total').value*1;
    value = sticker.querySelector('input').value;

    if(value == 1){// 1, 이미 선택된 걸 누른 경우. 선택해제
        sticker.style = "";

        sticker.querySelector('input').value = "0";
        document.querySelector('#total').value = total*1 - 1 ;
        total -= 1;

    }else if(total<4){// 0, 선택된 적 없는것을 누른 경우 이면서, 4개 미만 선택했을 때.
        sticker.style.backgroundColor = '#38362f';
        sticker.style.color = '#fff';
        sticker.style.width = '145px';
        sticker.style.height = '46px';
        sticker.style.margin = '6px';
        sticker.style.paddingTop = '26px';

        sticker.querySelector('input').value = "1";
        document.querySelector('#total').value = total*1 + 1 ;
        total += 1;
    }

    innerhtml = "";
    if(total>=4){
        innerhtml = "전부 다 고르셨어요!";
    }else if(total<=0){
        innerhtml = "좋아하시는 장르를 4종류 골라주세요!";
    }else{
        innerhtml = "앞으로 " + (4 - total) + "종류 남았어요!";
    }
    document.querySelector('.content_div>h3').innerHTML = innerhtml;
}

function check_submit(){
    total = document.querySelector('#total').value*1;
    if(total>=4){

        all_sticker = document.querySelectorAll('.ganre_selecter')
        selected = ""
        for (var i = 0; i < all_sticker.length; i++) {
            sticker = all_sticker[i];
            value = sticker.querySelector('input').value*1;
            html = sticker.querySelector('input').name;
    
            if(value>=1){
                selected += html +"|||";
            }
        }
        document.querySelector('#summary').value = selected;
        document.querySelector('#select').submit();
    }

}
function id_check(){
    var username = document.getElementById('username-input').value;
    var xhr = new XMLHttpRequest();
    xhr.open('get', 'check-username/?username='+username);
    xhr.setRequestHeader('Content-Type', 'application/json');
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    var message = document.querySelector(".id_message")

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) { 
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                console.log(response)
                if (response.exists) {
                    message.innerHTML = '중복된 아이디입니다.';
                }else if (response.error) {
                    message.innerHTML = '오류가 발생했습니다.';
                }else {
                    message.innerHTML = '사용 가능한 아이디입니다.';
                }
            } else {
                message.innerHTML = '오류가 발생했습니다.';
            }
        }
    };
    xhr.send(JSON.stringify({ 'username': username }));
}

var tm = null;
function timed_check(time){
    clearTimeout(tm); 
    var message = document.querySelector(".id_message")
    message.innerHTML = '';
    tm=setTimeout(function(){id_check()},time);
}

function passwd_check(){
    var pw = document.getElementById('pw').value;
    var pwck = document.getElementById('pw2').value;
    var message = document.querySelector(".pw_message")

    var numtest = /[0-9]/;
    var alphabettest = /[a-zA-Z]/;
    var specialtest = /[^a-zA-Z0-9]/;

    var condition = numtest.test(pw);
    condition *= alphabettest.test(pw);
    condition *= specialtest.test(pw);

    if(condition == 0){
        message.innerHTML = "알파벳, 숫자, 특수문자가 포함되어야 합니다"    ;
        return 0;
    }else if(pw.length <= 7){
        message.innerHTML = "길이가 8글자 이상 이어야 합니다"    ;
        return 0;
    }else if (pw==pwck){
        message.innerHTML = "사용 가능합니다"    ;
        return 1;
    }else{
        message.innerHTML = "비밀번호와 동일하지 않습니다";
        return 0;
    }
}

function show_term(){
    document.querySelector(".term_div").style.height = "200px";
    document.querySelector('#is_shown').value = "1";
}
function hide_term(){
    document.querySelector(".term_div").style.height = "0px";
    document.querySelector('#is_shown').value = "0";
}

function see_more(){
    value = document.querySelector('#is_shown').value * 1

    if(value){
        hide_term()
    }else{
        show_term()
    }
}
function agree(){
    value = document.querySelector('#agreed').checked * 1

    if(value){
        hide_term()
    }else{
        show_term()
    }
}