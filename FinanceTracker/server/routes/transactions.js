const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const Transaction = require('../models/Transaction');

// @route   GET api/transactions
// @desc    Get all transactions for a user
router.get('/', auth, async (req, res) => {
    try {
        const transactions = await Transaction.find({ userId: req.user.id }).sort({ date: -1 });
        res.json(transactions);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});

// @route   POST api/transactions
// @desc    Add new transaction
router.post('/', auth, async (req, res) => {
    const { merchant, category, amount, type, date, description } = req.body;
    try {
        const newTransaction = new Transaction({
            userId: req.user.id,
            merchant,
            category,
            amount,
            type,
            date,
            description
        });
        const transaction = await newTransaction.save();
        res.json(transaction);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});

module.exports = router;
