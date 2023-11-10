const { app, BrowserWindow, screen } = require('electron');

const path = require('path');
const ffmpeg = require('fluent-ffmpeg');

require('@electron/remote/main').initialize()

//ipc
const { ipcMain } = require('electron')
ipcMain.on('asynchronous-message', (event, arg) => {
    let arr = ["bad apple", "Renai Circulation"]
    arg = arr[Math.floor(Math.random() * 2)]

    ffmpeg.ffprobe(`video/videos/${arg}.mp4`, function (err, metadata) {
        if (err) {
            console.error(err)
        } else {
            // metadata should contain 'width', 'height' and 'display_aspect_ratio'
            let width = metadata.streams[0].width
            let height = metadata.streams[0].height

            let scaling = (width * height) / (360 * 480)

            width /= Math.sqrt(scaling)
            height /= Math.sqrt(scaling)


            let x = Math.round((Math.random()) * 1000)
            let y = Math.round((Math.random()) * 750)

            const newWindow = new BrowserWindow({
                width: Math.round(width),
                height: Math.round(height) + 17,
                fullscreenable: false,
                fullscreen: false,
                maximizable: false,
                alwaysOnTop: true,
                webPreferences: {
                    preload: path.join(__dirname, 'video_preload.js'),
                    nodeIntegration: true,
                    contextIsolation: false,
                    enableRemoteModule: true
                },
                x: x,
                y: y
            });
            require('@electron/remote/main').enable(newWindow.webContents)
            newWindow.loadFile(`video/${arg}.html`)
            newWindow.setMenu(null)


            const displays = screen.getAllDisplays()
            const externalDisplay = displays.find((display) => {
                return display.bounds.x !== 0 || display.bounds.y !== 0
            })
            console.log(externalDisplay)
            // console.log(externalDisplay?.bounds)
        }
    });
})

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: true,
            enableRemoteModule: true,
        },

    });

    win.loadFile('index.html');
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    })
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
})

