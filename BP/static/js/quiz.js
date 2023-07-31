document.addEventListener("mousemove", (e) => {
    const hint = document.querySelector(".hint");
    var element = document.querySelector('.pict_container');
    
    var topPos = -element.getBoundingClientRect().top;
    var leftPos = -element.getBoundingClientRect().left;

    const mouseX = e.clientX + leftPos;
    const mouseY = e.clientY + topPos;

    hint.style.left = mouseX + 'px';
    hint.style.top = mouseY + 'px';

    var width = hint.offsetWidth * 0.8535;

    hint.style.backgroundPositionX = width-mouseX + 'px';
    hint.style.backgroundPositionY = width-mouseY + 'px';
});


quest_imgs = [];
hint_imgs = [];
anss = [];
stage = 0;
winpoint = 0;

function show(){
    document.querySelector('.pict_container').style.opacity = "1";
    document.querySelector('.ans_container').style.opacity = "1";
}


function refresh(){
    document.querySelector('.pict_container').style.opacity = "0";
    document.querySelector('.ans_container').style.opacity = "0";
    setTimeout(() => show(), 200);

    document.querySelector('.pict_container>img').src = quest_imgs[stage]
    document.querySelector('.pict_container>div').style.backgroundImage = "url(" +hint_imgs[stage] + ")"

    var all_sticker = document.querySelectorAll('.ans_container>div');

    for(var i = 0 ; i < all_sticker.length ; i++){

        sticker = all_sticker[i].querySelectorAll('div');
        sticker[0].innerHTML = anss[stage][i][0];
        sticker[1].innerHTML = anss[stage][i][1];
        all_sticker[i].querySelector('.point').value = anss[stage][i][2];

    }

    stage += 1;
    text = stage + "번 문제";
    document.querySelector(".count").innerHTML = text;

}

function start(){
    var all_sticker = document.querySelectorAll('.from_db');
    for(var i = 0 ; i < all_sticker.length ; i++){
        sticker = all_sticker[i];

        quest_img = sticker.querySelector(".quest_img").value;
        hint_img = sticker.querySelector(".hint_img").value;

        ans = []
        ans_sticker = sticker.querySelectorAll(".anss")
        for(var j = 0 ; j < ans_sticker.length ; j++){
            an_sticker = ans_sticker[j].querySelectorAll(".ans")

            an = [
                an_sticker[0].value, 
                an_sticker[1].value, 
                an_sticker[2].value, 
            ]
            ans.push(an)
        }

        quest_imgs.push(quest_img)
        hint_imgs.push(hint_img)
        anss.push(ans)
    }
    refresh()
}

function select(num){
    num = num*1 - 1;
    sticker = document.querySelectorAll('.ans_container>div')[num];

    winpoint += sticker.querySelector(".point").value * 1;
    if(stage == 6){
        //암튼 넘겨주겠다는 내용

        document.querySelector('.win_total').value = stage;
        document.querySelector('.win_point').value = winpoint;
        document.querySelector('.next').submit();
        
    }else{
        refresh()
    }
}