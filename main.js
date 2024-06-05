const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
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
            dashProcess.kill('SIGTERM');
        }
    });
}

function startDashProcess() {
    let exePath;
    if (process.platform === 'win32') {
        exePath = path.join(__dirname, 'NRSexc', 'NRS.exe');
    } else if (process.platform === 'darwin') {
        exePath = path.join(__dirname, 'NRSexc', 'NRS');
    } else {
        exePath = path.join(__dirname, 'NRSexc', 'NRS'); // Linux or other platforms
    }

    dashProcess = spawn(exePath);

    dashProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    dashProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    dashProcess.on('close', (code) => {
        console.log(`Dash process exited with code ${code}`);
    });
}

app.on('ready', () => {
    startDashProcess();
    setTimeout(createWindow, 1000); // Delay to ensure Dash server is up
});

app.on('window-all-closed', () => {
    if (dashProcess) {
        dashProcess.kill('SIGTERM');
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
        dashProcess.kill('SIGTERM');
    }
});

process.on('SIGTERM', () => {
    if (dashProcess) {
        dashProcess.kill('SIGTERM');
    }
    app.quit();
});

process.on('SIGINT', () => {
    if (dashProcess) {
        dashProcess.kill('SIGTERM');
    }
    app.quit();
});

process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
    if (dashProcess) {
        dashProcess.kill('SIGTERM');
    }
    app.quit();
});
