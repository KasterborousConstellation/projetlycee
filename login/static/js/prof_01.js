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
    
    var range = document.getElementById("size");
    lamba = e =>{
        var target = document.getElementById("direct-size");
        target.innerText="Nombre de places: "+e.target.value;
    };
    range.addEventListener("input",lamba);
    range.addEventListener("change",lamba);
}