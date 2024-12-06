import express from 'express';

const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  // Get the real IP from X-Forwarded-For header
  const ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
  res.send(`<h1>Your IP Address is: ${ip}</h1>`);
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
