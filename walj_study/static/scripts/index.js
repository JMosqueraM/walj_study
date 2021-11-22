
function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/notas";
  });
}

function cambiarDificultad(cartaId) {
  fetch("/cambiar-dificultad", {
    method: "GET",
    body: JSON.stringify({ cartaId: cartaId }),
  }).then((_res) => {
    window.location.href = "/pagina_repaso";
  });
}


function deleteCarta(cartaId) {
  fetch("/delete-carta", {
    method: "POST",
    body: JSON.stringify({ cartaId: cartaId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
