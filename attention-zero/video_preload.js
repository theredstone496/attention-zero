const { BrowserWindow, getCurrentWindow } = require('@electron/remote')
window.addEventListener('DOMContentLoaded', () => {
    const video = document.querySelector('video')
    video.addEventListener('ended', () => {
        let id = getCurrentWindow().id
        let win = BrowserWindow.fromId(id)
        win.close();
    })
})