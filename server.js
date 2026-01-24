const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const requestHandler = (req, res) => {
  let filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('File not found');
      return;
    }
    // Determine Content-Type based on file extension
    const ext = path.extname(filePath);
    let contentType = 'text/html';
    switch (ext) {
      case '.css':
        contentType = 'text/css';
        break;
      case '.js':
        contentType = 'application/javascript';
        break;
      case '.json':
        contentType = 'application/json';
        break;
      case '.png':
        contentType = 'image/png';
        break;
      case '.jpg':
      case '.jpeg':
        contentType = 'image/jpeg';
        break;
      case '.webp':
        contentType = 'image/webp';
        break;
      case '.avif':
        contentType = 'image/avif';
        break;
      case '.svg':
        contentType = 'image/svg+xml';
        break;
      case '.woff':
        contentType = 'font/woff';
        break;
      case '.woff2':
        contentType = 'font/woff2';
        break;
      case '.ttf':
        contentType = 'font/ttf';
        break;
      case '.ico':
        contentType = 'image/x-icon';
        break;
      default:
        contentType = 'text/html';
    }
    // Security headers
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
    res.setHeader('Content-Security-Policy', "default-src 'self'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; report-uri /csp-report");
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(data);
  });
};

let server;
let protocol = 'http';
let port = 8000;

if (fs.existsSync('key.pem') && fs.existsSync('cert.pem')) {
  const options = {
    key: fs.readFileSync('key.pem'),
    cert: fs.readFileSync('cert.pem')
  };
  server = https.createServer(options, requestHandler);
  protocol = 'https';
} else {
  server = http.createServer(requestHandler);
server.listen(port, () => {
  console.log(`Server running at ${protocol}://localhost:${port}/`);
});