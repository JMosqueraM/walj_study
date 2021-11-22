document.getElementById("dificultad").style.visibility = "hidden";
document.getElementById("respuesta").style.visibility = "hidden";

function toggleText(){
var dificultades = document.getElementById("dificultad");
if (dificultades.style.visibility === "hidden") {
    dificultades.style.visibility = "visible";
} else {
    dificultades.style.visibility = "hidden";
}
var respuesta = document.getElementById("respuesta");
if (respuesta.style.visibility === "hidden") {
    respuesta.style.visibility = "visible";
} else {
    respuesta.style.visibility = "hidden";
}

}

let decreaseBtn1 = document.getElementById("muy_dificil")
let decreaseBtn2 = document.getElementById("dificil")
let decreaseBtn3 = document.getElementById("facil")
let decreaseBtn4 = document.getElementById("muy_facil")
let counter = 0;

decreaseBtn1.addEventListener('click', ()=>{
    counter ++;
    console.log(counter)
})

decreaseBtn2.addEventListener('click', ()=>{
    counter ++;
    document.getElementById('contador').innerHTML = "<p id='counter' value='"+ counter +"'></p>"
    console.log(counter)
})

decreaseBtn3.addEventListener('click', ()=>{
    counter ++;
    document.getElementById('contador').innerHTML = "<p id='counter' value='"+ counter +"'></p>"
    console.log(counter)
})

decreaseBtn4.addEventListener('click', ()=>{
    counter ++;
    document.getElementById('contador').innerHTML = "<p id='counter' value='"+ counter +"'>"+ counter +"</p>"
    console.log(counter)
})

async function getData() {
    const response = await fetch('/api');
    const data = await response.js 
}






