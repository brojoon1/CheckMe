paths = [];
names = [];
keywords = [];
isbns = [];
stage = 0;

function shuffle(array) {
    array.sort(() => Math.random() - 0.5);
}

function refresh(){
    document.querySelector('.ganre_container').style.opacity = "0";
    setTimeout(() => document.querySelector('.ganre_container').style.opacity = "1", 200);

    var all_sticker = document.querySelectorAll('.ganre_container>div');

    for(var i = 0 ; i < all_sticker.length ; i++){
        sticker = all_sticker[i];
        sticker.querySelector(".name").value = names[i + stage * 4];
        sticker.querySelector(".keyword").value = keywords[i + stage * 4];
        sticker.querySelector(".isbn").value = isbns[i + stage * 4];
        sticker.querySelector("img").src = paths[i + stage * 4];

    }

    stage += 1;
    text = stage + "번 선택지";
    document.querySelector(".current").style.width = stage * 100 / 17 + "%"
    document.querySelector(".count").innerHTML = text;

}

function start(){
    var all_sticker = document.querySelectorAll('.from_db');
    for(var i = 0 ; i < all_sticker.length ; i++){
        sticker = all_sticker[i];

        genre_path = sticker.querySelector(".img").value;
        genre_name = sticker.querySelector(".name").value;
        genre_keyword = sticker.querySelector(".keyword").value;
        genre_isbn = sticker.querySelector(".isbn").value;
        
        paths.push(genre_path)
        names.push(genre_name)
        keywords.push(genre_keyword)
        isbns.push(genre_isbn)
    }
    refresh()
}

function select(num){
    num = num*1 - 1;
    sticker = document.querySelectorAll('.ganre_container>div')[num];

    winner_path = sticker.querySelector(".img").src;
    winner_name = sticker.querySelector(".name").value;
    winner_keyword = sticker.querySelector(".keyword").value;
    winner_isbn = sticker.querySelector(".isbn").value;
    
    if(stage < 17){

        names.push([winner_name])
        keywords.push([winner_keyword])
        isbns.push([winner_isbn])
        paths.push([winner_path])

        refresh()
    }else if(stage == 17){
        //암튼 넘겨주겠다는 내용
        stage += 1;

        document.querySelector('.selected_name').value = winner_name;
        document.querySelector('.selected_keyword').value = winner_keyword;
        document.querySelector('.selected_isbn').value = winner_isbn;
        document.querySelector('.ganre_container form').submit();
        
    } 
}