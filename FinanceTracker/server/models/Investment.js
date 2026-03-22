const mongoose = require('mongoose');

const InvestmentSchema = new mongoose.Schema({
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    assetName: { type: String, required: true },
    symbol: { type: String },
    amount: { type: Number, required: true },
    currentValue: { type: Number },
    type: { type: String, required: true }, // e.g., 'Stock', 'Crypto', 'Real Estate'
    purchaseDate: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Investment', InvestmentSchema);
