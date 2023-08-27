function deleteNote(lista) {
  noteId = lista[1];
  fetch('/delete-note', {
    method: 'POST',
    body: JSON.stringify({ noteId: noteId}),
  }).then((_res) => {
    s = "/note/" + lista[0];
    window.location.href = s;
  });
}

function on() {
  document.getElementById("overlay").style.display = "block";
}

function off() {
  document.getElementById("overlay").style.display = "none";
}

function Alert() {
  alert("Nothing to delete!");
}

function searchRedirect(s) {
  redirect = "/note/" + s[0];
  window.location.href = redirect;
}

function search(buttonID) {
  if(event.keyCode == 13 && !event.shiftKey) {
      document.getElementById(buttonID).click();
  }
}