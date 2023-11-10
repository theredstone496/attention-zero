window.addEventListener('DOMContentLoaded', () => {
    const video = document.querySelector('video')
    video.addEventListener('ended', () => {
        const { BrowserWindow } = require('@electron/remote')
        let win = BrowserWindow.getFocusedWindow()
        win.close();
    })
})