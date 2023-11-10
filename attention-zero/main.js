const { app, BrowserWindow } = require('electron');
const path = require('path');
const ffmpeg = require('fluent-ffmpeg');

//ipc
const { ipcMain } = require('electron')
ipcMain.on('asynchronous-message', (event, arg) => {

    console.log(arg)

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

            console.log(width)
            console.log(height)

            const newWindow = new BrowserWindow({
                width: Math.round(width),
                height: Math.round(height) + 17,
                fullscreenable: false,
                fullscreen: false,
                maximizable: false,
                alwaysOnTop: true,
                webPreferences: {
                    nodeIntegration: true
                }
            });

            newWindow.loadFile(`video/${arg}.html`)
        }
    });
})

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
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