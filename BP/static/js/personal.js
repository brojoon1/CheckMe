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