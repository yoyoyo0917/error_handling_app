const { app, BrowserWindow } = require('electron');  
const { spawn } = require('child_process');  
  
let mainWindow;  
let flask; // Flaskプロセスを保持する変数  
  
function createWindow() {  
    mainWindow = new BrowserWindow({  
        width: 800,  
        height: 600,  
        webPreferences: {  
            nodeIntegration: true,  
            contextIsolation: false,  
        },  
    });  
  
    mainWindow.loadURL('http://localhost:5002'); // FlaskサーバーのURL  
}  
  
app.whenReady().then(() => {  
    // Flaskサーバーを起動  
    flask = spawn('python', ['app.py']);  
  
    flask.stdout.on('data', (data) => {  
        console.log(`Flask: ${data}`);  
    });  
  
    flask.stderr.on('data', (data) => {  
        console.error(`Flask Error: ${data}`);  
    });  
  
    createWindow();  
  
    app.on('activate', () => {  
        if (BrowserWindow.getAllWindows().length === 0) createWindow();  
    });  
});  
  
app.on('window-all-closed', () => {  
    if (flask) {  
        flask.kill(); // Flaskプロセスを終了  
    }  
    if (process.platform !== 'darwin') app.quit();  
});