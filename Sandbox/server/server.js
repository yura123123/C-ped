const config = require("./utility/config")

const http = require('http');
const express = require('express');

const port = config.get('Server', 'sandbox_port');

const app = express();

const clientPath = __dirname + '/../client';
console.log('Serving static from ' + clientPath);

app.use(express.static(clientPath));



const server = http.createServer(app);

server.on('error', (err) => {
  console.error('Sandbox server error: ', err);
});

server.listen(port, () => {
  console.log("Sandbox started on " + port);
});

/*
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.on('line', (input) => {
    Do command line processing here someday.
});
*/
