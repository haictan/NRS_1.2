const { app, BrowserWindow } = require('electron');
const { execFile } = require('child_process');
const path = require('path');

let dashProcess;
let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1300,
        height: 1000,
        webPreferences: {
            nodeIntegration: false
        },
        autoHideMenuBar: true,
        icon: path.join(__dirname, 'assets', 'icon.png')
    });

    mainWindow.loadURL('http://127.0.0.1:8050');

    mainWindow.on('closed', () => {
        mainWindow = null;
        if (dashProcess) {
            dashProcess.kill();
        }
    });
}

function startDashProcess() {
    let exePath;
    if (process.platform === 'win32') {
        exePath = path.join(__dirname, 'NRSexc', 'NRS.exe');
    } else if (process.platform === 'darwin') {
        exePath = path.join(__dirname, 'NRSexc', 'NRS');
    }

    dashProcess = execFile(exePath, (error, stdout, stderr) => {
        if (error) {
            console.error(`execFile error: ${error.message}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
        console.error(`stderr: ${stderr}`);
    });
}

app.on('ready', () => {
    startDashProcess();
    setTimeout(createWindow, 1000);
});

app.on('window-all-closed', () => {
    if (dashProcess) {
        dashProcess.kill();
    }
    app.quit();
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

app.on('before-quit', () => {
    if (dashProcess) {
        dashProcess.kill();
    }
});

process.on('SIGTERM', () => {
    if (dashProcess) {
        dashProcess.kill();
    }
    app.quit();
});

process.on('SIGINT', () => {
    if (dashProcess) {
        dashProcess.kill();
    }
    app.quit();
});

process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
    if (dashProcess) {
        dashProcess.kill();
    }
    app.quit();
});
