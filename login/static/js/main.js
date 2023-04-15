window.onload = function() {
    if(!!window.chrome){
        var buttons = document.getElementsByClassName("headcol");
        for(var i=0; i<buttons.length;++i){
            buttons[i].classList.add("chromefix");
        }
        var buttons = document.getElementsByClassName("event");
        for(var i=0; i<buttons.length;++i){
            buttons[i].classList.add("chromefix-2");
        }
    }
}