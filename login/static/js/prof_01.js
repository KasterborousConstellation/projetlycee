window.onload= e =>{
    var salle_input = document.getElementById("room");
    var lamba = e => {
        var content =""+e.target.innerText;
        salle_input.value=content;
    };

    var deroulant = document.getElementsByClassName("nav-1");
    for(let i =0;i< deroulant.length;++i){
        deroulant[i].addEventListener("click",lamba);

    }

    var matiere_input = document.getElementById("matiere");
    var lamba = e => {
        var content =""+e.target.innerText;
        matiere_input.value=content;
    };

    var deroulant = document.getElementsByClassName("nav-2");
    for(let i =0;i< deroulant.length;++i){
        deroulant[i].addEventListener("click",lamba);
    }
    
    var classe_input = document.getElementById("classe");
    var lamba = e => {
        var content =""+e.target.innerText;
        classe_input.value=content;
    };

    var deroulant = document.getElementsByClassName("nav-3");
    for(let i =0;i< deroulant.length;++i){
        deroulant[i].addEventListener("click",lamba);

    }
    var day_input = document.getElementById("day");
    var lamba = e => {
        var content =""+e.target.innerText;
        day_input.value=content;
    };

    var deroulant = document.getElementsByClassName("nav-4");
    for(let i =0;i< deroulant.length;++i){
        deroulant[i].addEventListener("click",lamba);
    }

    var hour_input = document.getElementById("hour");
    var lamba = e => {
        var content =""+e.target.innerText;
        hour_input.value=content;
    };

    var deroulant = document.getElementsByClassName("nav-5");
    for(let i =0;i< deroulant.length;++i){
        deroulant[i].addEventListener("click",lamba);
    }

    var range = document.getElementById("size");
    lamba = e =>{
        var target = document.getElementById("direct-size");
        target.innerText="Nombre de places: "+e.target.value;
    };
    range.addEventListener("input",lamba);
    range.addEventListener("change",lamba);
    var specific_radio = document.getElementById("specific");
    var specific_label = document.getElementById("specific-label");
    var specific_div = document.getElementById("specific-div");

    lamba = e =>{
        var bool = specific_radio.checked;
        if(bool===true){
            specific_label.hidden=true;
            specific_div.hidden=false;
        }else{
            specific_label.hidden=false;
            specific_div.hidden=true;
        }
    };

    var radios = document.getElementsByClassName("cours-radio");
    for(let i =0;i<radios.length;++i){
        radios[i].addEventListener("click",lamba);
    }

}