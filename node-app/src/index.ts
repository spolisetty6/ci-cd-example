import express, { Express, Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import pino from 'pino';

dotenv.config();

const logger = pino();
const app: Express = express();
const port = process.env.PORT || 8080;

// Middleware
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req: Request, res: Response) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version,
  });
});

// Ready probe
app.get('/ready', (req: Request, res: Response) => {
  res.status(200).json({ ready: true });
});

// API endpoint
app.get('/api/status', (req: Request, res: Response) => {
  res.status(200).json({
    message: 'API is working',
    environment: process.env.NODE_ENV,
  });
});

// Error handling
app.use((err: any, req: Request, res: Response) => {
  logger.error(err);
  res.status(500).json({ error: 'Internal Server Error' });
});

// Start server
app.listen(port, () => {
  logger.info(`Server running on port ${port}`);
});

export default app;
