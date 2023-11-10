const { ipcRenderer } = require('electron')

window.addEventListener('DOMContentLoaded', () => {
  ipcRenderer.on('asynchronous-reply', (event, arg) => {
    console.log(arg) // prints "pong"
  })
  //button and its event listener
  const b1 = document.getElementById('b1');
  const b2 = document.getElementById('b2');

  b1.addEventListener('click', () => {
    ipcRenderer.send('asynchronous-message', b1.innerText)
  })
  b2.addEventListener('click', () => {
    ipcRenderer.send('asynchronous-message', b2.innerText)
  })
})

const intervalID = setInterval(myCallback, 15 * 1000);
function myCallback() {
  ipcRenderer.send('asynchronous-message')
}
