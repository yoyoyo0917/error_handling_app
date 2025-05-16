const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  calculate: (formula, params, vals) => ipcRenderer.invoke('calculate', formula, params, vals)
});