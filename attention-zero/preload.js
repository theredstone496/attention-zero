const { ipcRenderer } = require('electron')
const { dialog } = require('@electron/remote')
const { exec, spawn } = require("child_process");

let popUp = false

window.addEventListener('DOMContentLoaded', () => {

  //button and its event listener
  const b1 = document.getElementById('b1');
  const b2 = document.getElementById('b2');

  b1.addEventListener('click', () => {
    const value = document.querySelector('input[name="mode"]:checked')?.value;
    let split = 'False';
    if (value == "Split-screen") {
      split = 'True';
    }
    else {
      split = 'False';
    }
    dialog.showOpenDialog({ properties: ['openFile'] }).then((response) => {
      if (response.canceled) return console.log("augh")
      const filePath = response.filePaths
      const out = document.getElementById("out")
      console.log(filePath[0])
      const extrafile = Math.floor(Math.random() * 4) + 1

      const python = spawn("py", ['../python stuff/videoedit.py', '--mainvid', filePath[0], '--extravid', '../attention-zero/video/videos/SS1.mp4,../attention-zero/video/videos/SS2.mp4,../attention-zero/video/videos/SS3.mp4,../attention-zero/video/videos/SS4.mp4', '--output', 'richard.mp4', '--percentile', '40', '--attentionSpan', '300', '--splitScreen', split])

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