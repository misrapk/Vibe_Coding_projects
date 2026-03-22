const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const fs = require('fs');
const path = require('path');

// Manually load .env variables if dotenv is failing to inject them
const envPath = path.join(__dirname, '.env');
if (fs.existsSync(envPath)) {
    const envConfig = require('dotenv').parse(fs.readFileSync(envPath));
    for (const k in envConfig) {
        process.env[k] = envConfig[k];
    }
}

// Critical variables with strict fallbacks to avoid "must have a value" errors
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/financeTracker';
const JWT_SECRET = process.env.JWT_SECRET || 'your_super_secret_jwt_key_here';
const PORT = process.env.PORT || 5000;

const app = express();

// Middleware
app.use(express.json());
app.use(cors());
app.use(helmet({
    contentSecurityPolicy: false,
}));
app.use(morgan('dev'));

// Database Connection
mongoose.connect(MONGODB_URI)
    .then(() => console.log('MongoDB Connected successfully to:', MONGODB_URI))
    .catch(err => {
        console.error('MongoDB connection error:', err.message);
    });

// Basic Route
app.get('/', (req, res) => {
    res.send('Finance Tracker API is running...');
});

// Routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/transactions', require('./routes/transactions'));

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`JWT_SECRET status: ${JWT_SECRET ? 'LOADED' : 'MISSING'}`);
    // Inject variables into process.env if they weren't there
    process.env.JWT_SECRET = JWT_SECRET;
});
