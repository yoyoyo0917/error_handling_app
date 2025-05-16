import fetch from 'node-fetch';
import { app, BrowserWindow, ipcMain } from 'electron';

function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: true,
      enableRemoteModule: true,
      preload: new URL('./preload.js', import.meta.url).pathname
    }
  })

  win.loadFile('templates/index.html')
}

// Pythonスクリプトを起動  
const pythonProcess = spawn('python3', ['app.py']);  
pythonProcess.stdout.on('data', (data) => {  
    console.log(`Python Output: ${data}`);  
});  
pythonProcess.stderr.on('data', (data) => {  
    console.error(`Python Error: ${data}`);  
});
app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})

ipcMain.handle('calculate', async (event, formula, params, vals) => {
    try {
        console.log("Received calculate request:", { formula, params, vals });
        const response = await fetch('http://localhost:5002/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                formula: formula,
                params: params,
                vals: vals
            })
        });
        const data = await response.json();
        console.log("Response from Flask:", data);
        return data;
    } catch (error) {
        console.error("Error in calculate handler:", error);
        throw error;
    }
});
import { spawn } from 'child_process';