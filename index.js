// index.js

const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

// Basic route to test
app.get('/', (req, res) => {
  res.send('Hello, World! This is my simple web app deployed on Vercel!');
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
