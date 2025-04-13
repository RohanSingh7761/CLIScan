const http = require('http');
const fs = require('fs');
const url = require('url');
const { exec } = require('child_process');

const PORT = 3000;

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const query = parsedUrl.query;

  if (parsedUrl.pathname === '/ping') {
    const ip = query.ip; 
    exec(`ping -c 1 ${ip}`, (err, stdout, stderr) => {
      if (err) {
        res.writeHead(500);
        return res.end('Error occurred');
      }
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end(stdout);
    });
    return;
  }

  if (parsedUrl.pathname === '/read') {
    const fileName = query.file;
    fs.readFile(`./public/${fileName}`, 'utf8', (err, data) => {
      if (err) {
        res.writeHead(404);
        return res.end('File not found');
      }
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end(data);
    });
    return;
  }

  if (parsedUrl.pathname === '/greet') {
    const name = query.name || 'Guest';
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`<h1>Hello, ${name}</h1>`);
    return;
  }

  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Welcome to the vulnerable server!');
});

server.listen(PORT, () => {
  console.log(`Vulnerable server running at http://localhost:${PORT}`);
});
