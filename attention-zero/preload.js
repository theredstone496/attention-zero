const { ipcRenderer } = require('electron')
const { dialog } = require('@electron/remote')
const { exec, spawn } = require("child_process");

let popUp = false

window.addEventListener('DOMContentLoaded', () => {

  //button and its event listener
  const b1 = document.getElementById('b1');
  const b2 = document.getElementById('b2');

  b1.addEventListener('click', () => {
    dialog.showOpenDialog({ properties: ['openFile'] }).then((response) => {
      if (response.canceled) return console.log("augh")
      const filePath = response.filePaths
      const out = document.getElementById("out")
      console.log(filePath[0])

      const python = spawn("py", ['../python stuff/pixel.py', '--vidPath', '../attention-zero/video/videos/Renai Circulation.mp4', '--percentile', '70', '--vid2height', '480', '--vid2width', '360', '--attentionSpan', '300'])

      out.innerText += "it is the working"

      python.stdout.on('data', (data) => {
        out.innerText += `stdout: ${data}`
      });

      python.stderr.on('data', (data) => {
        out.innerText += `stderr: ${data}`
      });

      python.on('close', (code) => {
        out.innerText += `child process exited with code ${code}`
      });
    })
  })
  b2.addEventListener('click', () => {
    popUp = !popUp;
    myCallback()
    const intervalID = setInterval(myCallback, 100 * 1000);
  })
})

function myCallback() {
  if (popUp) ipcRenderer.send('asynchronous-message')
}