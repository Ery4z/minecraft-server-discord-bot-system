// Express boilerplate

import express from 'express';
import bodyParser from 'body-parser';
import {getServiceLogs, isServiceRunning, restartService, stopService, startService} from './service.js';

//Env variables
import dotenv from 'dotenv';
dotenv.config();


const LOG_LINE_COUNT = process.env.LOG_LINE_COUNT || 10;
const SERVICE_NAME = process.env.SERVICE_NAME || 'minecraft-server.service';




const app = express();
app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.send('Hello World!');
}
);


app.get('/service/status', (req, res) => {
    isServiceRunning(SERVICE_NAME).then((isRunning) => {
        res.send({ isRunning });
    }).catch((err) => {
        res.statusCode(500).send(err);
    });

});
app.get('/service/logs', (req, res) => {
    getServiceLogs(SERVICE_NAME, LOG_LINE_COUNT).then((logs) => {
        res.send({logs});
    }).catch((err) => {
        res.statusCode(500).send(err);
    });
});

app.post('/service/restart', (req, res) => {
    restartService(SERVICE_NAME).then((message) => {
        res.send({ message });
    }).catch((err) => {
        res.statusCode(500).send(err);
    });
});

app.post('/service/stop', (req, res) => {
    stopService(SERVICE_NAME).then((message) => {
        res.send({ message });
    }).catch((err) => {
        res.statusCode(500).send(err);
    });
});

app.post('/service/start', (req, res) => {
    startService(SERVICE_NAME).then((message) => {
        res.send({ message });
    }).catch((err) => {
        res.statusCode(500).send(err);
    });
});


app.listen(8080, () => {
    console.log('Server started on http://localhost:8080');
}
);