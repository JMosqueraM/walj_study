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