const express = require('express');
const path = require('path');
const client = require('prom-client');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = process.env.PORT || 80;
const METRICS_PORT = process.env.METRICS_PORT || 9091;

client.collectDefaultMetrics({ prefix: 'frontend_process_' });

const httpRequestsTotal = new client.Counter({
  name: 'frontend_server_http_requests_total',
  help: 'Total HTTP requests handled by the frontend server',
  labelNames: ['method', 'path', 'status'],
});

const httpRequestDuration = new client.Histogram({
  name: 'frontend_server_http_request_duration_seconds',
  help: 'HTTP request duration for the frontend server',
  labelNames: ['method', 'path'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
});

function normalizePath(url) {
  if (url === '/health' || url === '/metrics') {
    return url;
  }
  if (url.startsWith('/api/')) {
    return '/api/*';
  }
  if (url.startsWith('/static/')) {
    return '/static/*';
  }
  if (!url.includes('.')) {
    return '/*';
  }
  return url;
}

// Backend URL configuration
const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000';

console.log(`Starting frontend server...`);
console.log(`Backend URL: ${BACKEND_URL}`);
console.log(`Port: ${PORT}`);

// Log all requests for debugging
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
  next();
});

app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const routePath = normalizePath(req.path);
    const durationSeconds = (Date.now() - start) / 1000;
    httpRequestsTotal.labels(req.method, routePath, String(res.statusCode)).inc();
    httpRequestDuration.labels(req.method, routePath).observe(durationSeconds);
  });
  next();
});

// Proxy API requests to backend
app.use('/api', createProxyMiddleware({
  target: BACKEND_URL,
  changeOrigin: true,
  logLevel: 'debug',
  onProxyReq: (proxyReq, req, res) => {
    console.log(`Proxying ${req.method} ${req.url} to ${BACKEND_URL}${req.url}`);
  },
  onProxyRes: (proxyRes, req, res) => {
    console.log(`Received response ${proxyRes.statusCode} for ${req.url}`);
  },
  onError: (err, req, res) => {
    console.error('Proxy error:', err.message);
    console.error('Full error:', err);
    
    // Check if headers were already sent
    if (!res.headersSent) {
      res.status(500).json({
        error: 'Proxy error',
        message: err.message,
        backend: BACKEND_URL
      });
    }
  }
}));

// Health check endpoint
app.get('/health', (req, res) => {
  console.log('Health check requested');
  res.status(200).send('healthy');
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

// Serve static files
app.use(express.static(path.join(__dirname, 'build')));

// Catch all handler - send React app for any other route
app.get('*', (req, res) => {
  console.log(`Serving React app for route: ${req.url}`);
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Express error:', err);
  res.status(500).send('Internal Server Error');
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Frontend server running on http://0.0.0.0:${PORT}`);
  console.log(`API requests will be proxied to: ${BACKEND_URL}`);
});

const metricsApp = express();
metricsApp.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

metricsApp.listen(METRICS_PORT, '0.0.0.0', () => {
  console.log(`Metrics server running on http://0.0.0.0:${METRICS_PORT}/metrics`);
});