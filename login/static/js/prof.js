window.onload= e =>{
    var loaded_possibilities = [];
    var datalist_children = document.getElementById("rooms").children;
    for(let i =0;i<datalist_children.length;++i){
        loaded_possibilities.push(datalist_children[i].value);
    }
    console.log(loaded_possibilities);
    var element = document.getElementById("salle-input");
    var lamba = e =>{
        var content = ""+e.target.value;
        var bar = document.getElementById("bar");
        var messager = document.getElementById("room-input-message");
        if(in_array(content,loaded_possibilities) === true){
            bar.className="bar active";
            messager.innerText="";
        }else{
            bar.className="bar non-active";
            messager.innerText="Salle Invalide";
        }
    };
    element.addEventListener("change",lamba);
    element.addEventListener("click",lamba);
}
function in_array(string, in_array){
    for(let i =0;i<in_array.length;++i){
        if(string===in_array[i]){
            return true;
        }
    }
    return false;
}