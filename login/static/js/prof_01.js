window.onload= e =>{
    var salle_input = document.getElementById("room");
    var lamba = e => {
        var content =""+e.target.innerText;
        salle_input.value=content;
        update();
    };

    var deroulant = document.getElementsByClassName("nav-1");
    for(let i =0;i< deroulant.length;++i){
        deroulant[i].addEventListener("click",lamba);
    }

    var matiere_input = document.getElementById("matiere");
    var lamba = e => {
        var content =""+e.target.innerText;
        matiere_input.value=content;
        update();
    };

    var deroulant = document.getElementsByClassName("nav-2");
    for(let i =0;i< deroulant.length;++i){
        deroulant[i].addEventListener("click",lamba);
    }
    
    var classe_input = document.getElementById("classe");
    var lamba = e => {
        var content =""+e.target.innerText;
        classe_input.value=content;
        update();
    };

    var deroulant = document.getElementsByClassName("nav-3");
    for(let i =0;i< deroulant.length;++i){
        deroulant[i].addEventListener("click",lamba);
    }
    var day_input = document.getElementById("day");
    var lamba = e => {
        var content =""+e.target.innerText;
        day_input.value=content;
        update();
    };

    var deroulant = document.getElementsByClassName("nav-4");
    for(let i =0;i< deroulant.length;++i){
        deroulant[i].addEventListener("click",lamba);
    }

    var hour_input = document.getElementById("hour");
    var lamba = e => {
        var content =""+e.target.innerText;
        hour_input.value=content;
        update();
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
    var specific_radio = getSpecificRadio();
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
    //Ajoute la mise a jour du bouton d'envoi au radios
    var radios = document.getElementsByClassName("cours-radio");
    for(let i =0;i<radios.length;++i){
        radios[i].addEventListener("click",lamba);
        radios[i].addEventListener("click",e=>{update()});
    }

    var submit = getSubmitButton();
    lamba = e => {
        if(!submit.classList.contains("submit")){
            e.preventDefault();
        }
    };
    
    submit.addEventListener("click",lamba);
    //Ajoute la mise a jour du bouton d'envoi au calendrier pour une semaine spécifique
    const specific_calendar = document.getElementById("specific-calendar");
    specific_calendar.addEventListener("change", e => {update()})
}
function update(){
    //Verifie si tout les champs sont remplis
    var modifiables = document.getElementsByTagName("input");
    var bool = true;
    for(let i =0;i<modifiables.length;++i){
        const element = modifiables[i];
        if(element.readOnly && element.type==="text"){
            bool =bool&& !(element.value==="");
        }
    }
    //Verifie pour la selection de la semaine spécifique si il y a lieu.
    const specific_radio = getSpecificRadio();
    if(specific_radio.checked){
        const specific_calendar = document.getElementById("specific-calendar");
        bool= bool && !(specific_calendar.value==="");
    }

    const submit = getSubmitButton();
    if(bool){
        submit.className="submit";
    }else{
        submit.className="";
    }
}
function getSubmitButton(){
    return document.getElementById("submit-button");
}
function getSpecificRadio(){
    return document.getElementById("specific");
}