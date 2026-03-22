import React, { useState, useEffect } from 'react';
import api from '../api';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

const Dashboard = () => {
    const [data, setData] = useState({ transactions: [] });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await api.get('/transactions');
                setData({ transactions: res.data });
            } catch (err) {
                console.error('Error fetching data', err);
            }
        };
        fetchData();
    }, []);

    return (
        <div className="flex h-screen overflow-hidden bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 font-display">
            <Sidebar />

            {/* Main Content */}
            <main className="flex-1 flex flex-col min-w-0 overflow-y-auto">
                <Header title="Dashboard Overview" />

                <div className="p-8 space-y-8">
                    {/* KPI Metric Cards */}
                    <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="bg-white dark:bg-surface-dark border border-slate-200 dark:border-border-dark p-6 rounded-xl flex flex-col justify-between shadow-sm">
                            <div className="flex justify-between items-start mb-4">
                                <div>
                                    <p className="text-slate-500 dark:text-slate-400 text-sm font-medium mb-1 uppercase tracking-wider">Total Balance</p>
                                    <h3 className="text-3xl font-bold">$124,500.00</h3>
                                </div>
                                <div className="bg-accent-success/10 text-accent-success px-2 py-1 rounded text-xs font-bold flex items-center gap-1">
                                    <span className="material-symbols-outlined text-sm">trending_up</span>
                                    +2.4%
                                </div>
                            </div>
                            <div className="h-10 w-full bg-gradient-to-r from-accent-success/20 to-transparent rounded flex items-end">
                                <div className="w-full h-1 bg-accent-success/30 rounded-full"></div>
                            </div>
                        </div>
                        <div className="bg-white dark:bg-surface-dark border border-slate-200 dark:border-border-dark p-6 rounded-xl flex flex-col justify-between shadow-sm">
                            <div className="flex justify-between items-start mb-4">
                                <div>
                                    <p className="text-slate-500 dark:text-slate-400 text-sm font-medium mb-1 uppercase tracking-wider">Monthly Spending</p>
                                    <h3 className="text-3xl font-bold">$3,210.00</h3>
                                </div>
                                <div className="bg-primary/10 dark:bg-white/10 text-slate-600 dark:text-slate-300 px-2 py-1 rounded text-xs font-bold">
                                    75% Budget
                                </div>
                            </div>
                            <div className="space-y-2">
                                <div className="h-2 w-full bg-slate-200 dark:bg-border-dark rounded-full overflow-hidden">
                                    <div className="h-full bg-primary dark:bg-blue-500 w-3/4"></div>
                                </div>
                                <p className="text-xs text-slate-500 dark:text-slate-400">$1,090 remaining until goal</p>
                            </div>
                        </div>
                        <div className="bg-white dark:bg-surface-dark border border-slate-200 dark:border-border-dark p-6 rounded-xl flex flex-col justify-between shadow-sm">
                            <div className="flex justify-between items-start mb-4">
                                <div>
                                    <p className="text-slate-500 dark:text-slate-400 text-sm font-medium mb-1 uppercase tracking-wider">Investment ROI</p>
                                    <h3 className="text-3xl font-bold">+8.1%</h3>
                                </div>
                                <div className="bg-accent-success/10 text-accent-success px-2 py-1 rounded text-xs font-bold">
                                    Year-to-Date
                                </div>
                            </div>
                            <div className="flex items-center gap-4">
                                <div className="flex -space-x-2">
                                    <div className="w-8 h-8 rounded-full border-2 border-surface-dark bg-slate-300 flex items-center justify-center text-[10px] font-bold">TSLA</div>
                                    <div className="w-8 h-8 rounded-full border-2 border-surface-dark bg-slate-300 flex items-center justify-center text-[10px] font-bold">AAPL</div>
                                    <div className="w-8 h-8 rounded-full border-2 border-surface-dark bg-slate-300 flex items-center justify-center text-[10px] font-bold">BTC</div>
                                </div>
                                <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Top performing assets</p>
                            </div>
                        </div>
                    </section>

                    {/* AI Snapshot Widget */}
                    <section className="@container">
                        <div className="relative overflow-hidden bg-primary rounded-xl p-6 md:p-8 text-white shadow-xl border border-blue-400/20">
                            <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 bg-blue-500/20 rounded-full blur-3xl pointer-events-none"></div>
                            <div className="absolute bottom-0 left-0 -ml-16 -mb-16 w-48 h-48 bg-purple-500/10 rounded-full blur-3xl pointer-events-none"></div>
                            <div className="relative flex flex-col md:flex-row md:items-center justify-between gap-6">
                                <div className="flex gap-4">
                                    <div className="flex-shrink-0 w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center border border-white/20">
                                        <span className="material-symbols-outlined text-blue-300 text-2xl animate-pulse">psychology</span>
                                    </div>
                                    <div className="max-w-2xl">
                                        <div className="flex items-center gap-2 mb-2">
                                            <h4 className="text-lg font-bold">AI Snapshot</h4>
                                            <span className="px-2 py-0.5 bg-blue-500 text-[10px] font-bold uppercase rounded-full tracking-tighter">Live Insight</span>
                                        </div>
                                        <p className="text-slate-300 text-lg leading-relaxed">
                                            "Your savings rate is <span className="text-accent-success font-bold">15% higher</span> than last month. You could save an extra <span className="text-white font-bold">$200</span> by reducing 'Dining Out' expenses in the next 14 days."
                                        </p>
                                    </div>
                                </div>
                                <button onClick={() => window.location.href = '/insights'} className="flex-shrink-0 bg-white text-primary hover:bg-slate-100 px-6 py-3 rounded-lg font-bold text-sm transition-all shadow-lg active:scale-95">
                                    View Full Analysis
                                </button>
                            </div>
                        </div>
                    </section>

                    {/* Data Grid */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <div className="lg:col-span-2 bg-white dark:bg-surface-dark border border-slate-200 dark:border-border-dark rounded-xl shadow-sm overflow-hidden flex flex-col">
                            <div className="px-6 py-5 border-b border-slate-200 dark:border-border-dark flex items-center justify-between">
                                <h4 className="text-lg font-bold">Recent Transactions</h4>
                                <button className="text-primary dark:text-blue-400 text-sm font-bold hover:underline">View All</button>
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full text-left">
                                    <thead className="bg-slate-50 dark:bg-primary/20 text-slate-500 dark:text-slate-400 text-xs font-bold uppercase tracking-wider">
                                        <tr>
                                            <th className="px-6 py-3">Merchant</th>
                                            <th className="px-6 py-3">Category</th>
                                            <th className="px-6 py-3">Date</th>
                                            <th className="px-6 py-3 text-right">Amount</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-100 dark:divide-border-dark">
                                        {data.transactions.length > 0 ? data.transactions.map((tx, idx) => (
                                            <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-primary/10 transition-colors">
                                                <td className="px-6 py-4">
                                                    <div className="flex items-center gap-3">
                                                        <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${tx.category === 'Shopping' ? 'bg-orange-100 text-orange-600' :
                                                                tx.category === 'Food & Drink' ? 'bg-green-100 text-green-600' :
                                                                    tx.category === 'Subscription' ? 'bg-blue-100 text-blue-600' :
                                                                        'bg-purple-100 text-purple-600'
                                                            }`}>
                                                            <span className="material-symbols-outlined text-sm">{
                                                                tx.category === 'Shopping' ? 'shopping_cart' :
                                                                    tx.category === 'Food & Drink' ? 'coffee' :
                                                                        tx.category === 'Subscription' ? 'smartphone' :
                                                                            'electric_bolt'
                                                            }</span>
                                                        </div>
                                                        <span className="font-semibold text-sm">{tx.merchant}</span>
                                                    </div>
                                                </td>
                                                <td className="px-6 py-4">
                                                    <span className="px-2 py-1 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded text-[10px] font-bold uppercase">{tx.category}</span>
                                                </td>
                                                <td className="px-6 py-4 text-sm text-slate-500">{new Date(tx.date).toLocaleDateString()}</td>
                                                <td className={`px-6 py-4 text-right font-bold text-sm ${tx.type === 'expense' ? 'text-accent-error' : 'text-accent-success'}`}>
                                                    {tx.type === 'expense' ? '-' : '+'}${tx.amount}
                                                </td>
                                            </tr>
                                        )) : (
                                            <React.Fragment>
                                                <TransactionRow merchant="Amazon.com" category="Shopping" date="Oct 24, 2023" amount="-$124.50" icon="shopping_cart" color="bg-orange-100 text-orange-600" />
                                                <TransactionRow merchant="Starbucks" category="Food & Drink" date="Oct 23, 2023" amount="-$8.20" icon="coffee" color="bg-green-100 text-green-600" />
                                                <TransactionRow merchant="Apple Services" category="Subscription" date="Oct 22, 2023" amount="-$14.99" icon="smartphone" color="bg-blue-100 text-blue-600" />
                                                <TransactionRow merchant="PG&E Utility" category="Utilities" date="Oct 21, 2023" amount="-$185.00" icon="electric_bolt" color="bg-purple-100 text-purple-600" />
                                            </React.Fragment>
                                        )}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* Category Distribution */}
                        <div className="bg-white dark:bg-surface-dark border border-slate-200 dark:border-border-dark rounded-xl shadow-sm p-6 flex flex-col">
                            <div className="flex items-center justify-between mb-8">
                                <h4 className="text-lg font-bold">Spending Categories</h4>
                                <span className="material-symbols-outlined text-slate-400">more_horiz</span>
                            </div>
                            <div className="flex-1 flex flex-col justify-center items-center">
                                <div className="relative w-40 h-40 mb-8">
                                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                                        <circle className="text-slate-100 dark:text-slate-800" cx="18" cy="18" fill="none" r="16" stroke="currentColor" strokeWidth="3"></circle>
                                        <circle cx="18" cy="18" fill="none" r="16" stroke="#3b82f6" strokeDasharray="45, 100" strokeLinecap="round" strokeWidth="3"></circle>
                                        <circle cx="18" cy="18" fill="none" r="16" stroke="#10b981" strokeDasharray="25, 100" strokeDashoffset="-45" strokeLinecap="round" strokeWidth="3"></circle>
                                        <circle cx="18" cy="18" fill="none" r="16" stroke="#f59e0b" strokeDasharray="15, 100" strokeDashoffset="-70" strokeLinecap="round" strokeWidth="3"></circle>
                                    </svg>
                                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                                        <p className="text-xs text-slate-500 font-medium">Total</p>
                                        <p className="text-xl font-bold text-slate-900 dark:text-white">$3,210</p>
                                    </div>
                                </div>
                                <div className="w-full space-y-3">
                                    <SpendingRow color="bg-blue-500" label="Housing" percent="45%" />
                                    <SpendingRow color="bg-emerald-500" label="Food & Drink" percent="25%" />
                                    <SpendingRow color="bg-amber-500" label="Entertainment" percent="15%" />
                                    <SpendingRow color="bg-slate-400" label="Other" percent="15%" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

const TransactionRow = ({ merchant, category, date, amount, icon, color }) => (
    <tr className="hover:bg-slate-50 dark:hover:bg-primary/10 transition-colors">
        <td className="px-6 py-4">
            <div className="flex items-center gap-3">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${color}`}>
                    <span className="material-symbols-outlined text-sm">{icon}</span>
                </div>
                <span className="font-semibold text-sm">{merchant}</span>
            </div>
        </td>
        <td className="px-6 py-4">
            <span className="px-2 py-1 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded text-[10px] font-bold uppercase">{category}</span>
        </td>
        <td className="px-6 py-4 text-sm text-slate-500">{date}</td>
        <td className="px-6 py-4 text-right font-bold text-sm text-slate-900 dark:text-white">{amount}</td>
    </tr>
);

const SpendingRow = ({ color, label, percent }) => (
    <div className="flex items-center justify-between text-sm">
        <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${color}`}></div>
            <span className="text-slate-600 dark:text-slate-300">{label}</span>
        </div>
        <span className="font-bold text-slate-900 dark:text-white">{percent}</span>
    </div>
);

export default Dashboard;
