const { app, BrowserWindow } = require('electron')

const createWindow = (file) => {
    const win = new BrowserWindow({
      width: 480,
      height: 397,
      frame: true
    })
  
    win.loadFile(file)
    win.setAlwaysOnTop(true)
    win.setMenu(null)
}

app.whenReady().then(() => {
    createWindow('index.html')

    app.on('activate', () => {
        // On macOS it's common to re-create a window in the app when the
        // dock icon is clicked and there are no other windows open.
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})



// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
})