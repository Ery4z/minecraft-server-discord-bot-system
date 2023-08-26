import { exec } from 'child_process';

export  function getServiceLogs(serviceName,linecount) {
    return new Promise((resolve, reject) => {
        exec(`journalctl -u ${serviceName} | tail -n ${linecount}`, (error, stdout, stderr) => {
            if (error) {
                reject(`Error executing journalctl: ${error.message}`);
                return;
            }
            if (stderr) {
                reject(`Stderr from journalctl: ${stderr}`);
                return;
            }
            
            resolve(stdout);
        });
    });
}

export function isServiceRunning(serviceName) {
    return new Promise((resolve, reject) => {
        exec(`systemctl is-active ${serviceName}`, (error, stdout, stderr) => {
            if (error) {
                reject(`Error checking service status: ${error.message}`);
                return;
            }
            
            if (stderr) {
                reject(`Stderr from systemctl: ${stderr}`);
                return;
            }

            const status = stdout.trim();
            if (status === 'active') {
                resolve(true);
            } else {
                resolve(false);
            }
        });
    });
}

export function restartService(serviceName) {
    return new Promise((resolve, reject) => {
        exec(`sudo systemctl restart ${serviceName}`, (error, stdout, stderr) => {
            if (error) {
                reject(`Error restarting service: ${error.message}`);
                return;
            }
            
            if (stderr) {
                reject(`Stderr from systemctl: ${stderr}`);
                return;
            }

            resolve(`Service ${serviceName} restarted successfully.`);
        });
    });
}

export function stopService(serviceName) {
    return new Promise((resolve, reject) => {
        exec(`sudo systemctl stop ${serviceName}`, (error, stdout, stderr) => {
            if (error) {
                reject(`Error stopping service: ${error.message}`);
                return;
            }
            
            if (stderr) {
                reject(`Stderr from systemctl: ${stderr}`);
                return;
            }

            resolve(`Service ${serviceName} stopped successfully.`);
        });
    });
}

export function startService(serviceName) {
    return new Promise((resolve, reject) => {
        exec(`sudo systemctl start ${serviceName}`, (error, stdout, stderr) => {
            if (error) {
                reject(`Error starting service: ${error.message}`);
                return;
            }
            resolve(`Service ${serviceName} started successfully.`);
        });
    });
}

