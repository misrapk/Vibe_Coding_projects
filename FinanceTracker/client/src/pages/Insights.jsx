import React from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

const Insights = () => {
    return (
        <div className="flex h-screen overflow-hidden bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 font-display">
            <Sidebar />

            {/* Main Content Area */}
            <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
                <Header title="AI Insights" />

                <main className="flex flex-1 flex-col lg:flex-row gap-6 p-6 lg:p-10">
                    <div className="flex flex-col flex-1 gap-8">
                        <section className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                            <div className="flex flex-col gap-2 rounded-xl p-6 bg-white dark:bg-primary/40 border border-slate-200 dark:border-primary/60">
                                <div className="flex justify-between items-start">
                                    <p className="text-slate-500 dark:text-slate-400 text-sm font-medium">Projected Net Worth</p>
                                    <span className="px-2 py-0.5 rounded bg-accent-green/20 text-accent-green text-[10px] font-bold uppercase tracking-wider">98% Confidence</span>
                                </div>
                                <p className="text-3xl font-bold tracking-tight">$124,500</p>
                                <p className="text-accent-green text-sm font-semibold flex items-center gap-1">
                                    <span className="material-symbols-outlined text-sm">trending_up</span> +12% vs last month
                                </p>
                            </div>
                            <div className="flex flex-col gap-2 rounded-xl p-6 bg-white dark:bg-primary/40 border border-slate-200 dark:border-primary/60">
                                <p className="text-slate-500 dark:text-slate-400 text-sm font-medium">Safety Buffer Score</p>
                                <div className="flex items-baseline gap-2">
                                    <p className="text-3xl font-bold tracking-tight">85</p>
                                    <p className="text-slate-400 dark:text-slate-500 text-lg">/100</p>
                                </div>
                                <div className="w-full bg-slate-200 dark:bg-slate-700 h-2 rounded-full mt-2">
                                    <div className="bg-accent-blue h-2 rounded-full" style={{ width: '85%' }}></div>
                                </div>
                            </div>
                            <div className="flex flex-col gap-2 rounded-xl p-6 bg-white dark:bg-primary/40 border border-slate-200 dark:border-primary/60 md:col-span-2 xl:col-span-1">
                                <p className="text-slate-500 dark:text-slate-400 text-sm font-medium">AI Optimization Potential</p>
                                <p className="text-3xl font-bold tracking-tight text-accent-teal">+$420.50</p>
                                <p className="text-slate-500 dark:text-slate-400 text-sm">Identified monthly savings available</p>
                            </div>
                        </section>

                        <section className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                            <div className="flex flex-col gap-4 p-6 rounded-xl bg-white dark:bg-primary/30 border border-slate-200 dark:border-primary/60">
                                <div className="flex items-center justify-between">
                                    <h3 className="text-lg font-bold">Spending Analysis</h3>
                                    <select className="bg-transparent border-none text-sm text-slate-500 focus:ring-0">
                                        <option>Last 6 Months</option>
                                        <option>Last 12 Months</option>
                                    </select>
                                </div>
                                <div className="h-64 w-full">
                                    <svg className="w-full h-full" fill="none" preserveAspectRatio="none" viewBox="0 0 500 200" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M0 150C50 140 100 160 150 100C200 40 250 80 300 60C350 40 400 90 450 30C480 10 500 0 500 0V200H0V150Z" fill="url(#grad1)" opacity="0.2"></path>
                                        <path d="M0 150C50 140 100 160 150 100C200 40 250 80 300 60C350 40 400 90 450 30" stroke="#007aff" strokeLinecap="round" strokeWidth="3"></path>
                                        <path d="M0 160C50 155 100 170 150 110C200 55 250 95 300 75C350 55 400 105 450 45" opacity="0.5" stroke="#00d4ff" strokeDasharray="4 4" strokeWidth="2"></path>
                                        <defs>
                                            <linearGradient id="grad1" x1="0%" x2="0%" y1="0%" y2="100%">
                                                <stop offset="0%" style={{ stopColor: '#007aff', stopOpacity: 1 }}></stop>
                                                <stop offset="100%" style={{ stopColor: '#007aff', stopOpacity: 0 }}></stop>
                                            </linearGradient>
                                        </defs>
                                    </svg>
                                </div>
                                <div className="flex justify-between text-xs text-slate-400 font-medium px-2">
                                    <span>JAN</span><span>FEB</span><span>MAR</span><span>APR</span><span>MAY</span><span>JUN</span>
                                </div>
                                <div className="flex gap-4 mt-2">
                                    <div className="flex items-center gap-2">
                                        <span className="size-3 rounded-full bg-accent-blue"></span>
                                        <span className="text-xs text-slate-500">Actual Spending</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <span className="size-3 rounded-full border border-accent-teal border-dashed"></span>
                                        <span className="text-xs text-slate-500">Predicted Baseline</span>
                                    </div>
                                </div>
                            </div>

                            <div className="flex flex-col gap-4 p-6 rounded-xl bg-white dark:bg-primary/30 border border-slate-200 dark:border-primary/60">
                                <div className="flex items-center justify-between">
                                    <h3 className="text-lg font-bold">Projected Wealth (12mo)</h3>
                                    <span className="text-accent-green text-sm font-bold">+15% Predicted Growth</span>
                                </div>
                                <div className="grid grid-cols-4 gap-4 h-64 items-end px-4">
                                    <div className="relative group">
                                        <div className="bg-primary/40 dark:bg-primary/60 border-t-4 border-accent-blue w-full h-24 rounded-t-lg transition-all hover:bg-accent-blue/20"></div>
                                        <p className="text-center text-xs mt-2 text-slate-500">Q1</p>
                                    </div>
                                    <div className="relative group">
                                        <div className="bg-primary/40 dark:bg-primary/60 border-t-4 border-accent-blue w-full h-32 rounded-t-lg transition-all hover:bg-accent-blue/20"></div>
                                        <p className="text-center text-xs mt-2 text-slate-500">Q2</p>
                                    </div>
                                    <div className="relative group">
                                        <div className="bg-primary/40 dark:bg-primary/60 border-t-4 border-accent-blue w-full h-48 rounded-t-lg transition-all hover:bg-accent-blue/20"></div>
                                        <p className="text-center text-xs mt-2 text-slate-500">Q3</p>
                                    </div>
                                    <div className="relative group">
                                        <div className="bg-accent-blue/40 border-t-4 border-accent-teal w-full h-56 rounded-t-lg transition-all">
                                            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-accent-teal text-primary text-[10px] font-bold px-2 py-1 rounded shadow-lg whitespace-nowrap">GOAL HIT</div>
                                        </div>
                                        <p className="text-center text-xs mt-2 text-slate-500">Q4</p>
                                    </div>
                                </div>
                                <p className="text-sm text-slate-500 italic text-center">AI estimates based on current recurring income and average spending habits.</p>
                            </div>
                        </section>

                        <section>
                            <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-slate-900 dark:text-white">
                                <span className="material-symbols-outlined text-accent-teal">tips_and_updates</span>
                                Smart Recommendations
                            </h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <RecommendationCard
                                    icon="restaurant"
                                    color="accent-blue"
                                    title="Reduce dining out to save $200"
                                    desc="AI detected a 24% increase in food delivery services this month compared to your usual average."
                                />
                                <RecommendationCard
                                    icon="account_balance"
                                    color="accent-teal"
                                    title="Optimize your 401k allocation"
                                    desc="Current market trends suggest rebalancing toward tech-heavy index funds could yield an extra 2.4% annually."
                                />
                                <RecommendationCard
                                    icon="bolt"
                                    color="accent-green"
                                    title="Subscription Audit: Save $45/mo"
                                    desc="3 recurring payments identified with zero usage in the last 60 days. Cancel to increase savings."
                                />
                                <RecommendationCard
                                    icon="shield_moon"
                                    color="slate-400"
                                    title="Emergency Fund Threshold"
                                    desc="You are $1,200 away from your ideal 6-month safety net. Redirecting bonus pay is recommended."
                                />
                            </div>
                        </section>
                    </div>

                    <aside className="w-full lg:w-96 flex flex-col gap-4 h-[600px] lg:h-auto">
                        <div className="flex flex-col h-full rounded-2xl bg-white dark:bg-primary/60 border border-slate-200 dark:border-primary/80 overflow-hidden shadow-xl">
                            <div className="p-4 border-b border-slate-200 dark:border-primary/80 flex items-center justify-between bg-primary text-white">
                                <div className="flex items-center gap-2">
                                    <div className="size-2 rounded-full bg-accent-green"></div>
                                    <span className="font-bold text-sm tracking-wide">WealthAI Assistant</span>
                                </div>
                                <span className="material-symbols-outlined text-sm cursor-pointer opacity-70 hover:opacity-100">info</span>
                            </div>
                            <div className="flex-1 p-4 flex flex-col gap-4 overflow-y-auto bg-slate-50 dark:bg-primary/20">
                                <div className="flex gap-2 text-slate-900 dark:text-white">
                                    <div className="size-8 rounded-full bg-accent-blue flex items-center justify-center shrink-0">
                                        <span className="material-symbols-outlined text-white text-xs">smart_toy</span>
                                    </div>
                                    <div className="p-3 rounded-2xl rounded-tl-none bg-white dark:bg-primary text-xs shadow-sm border border-slate-100 dark:border-primary/40 leading-relaxed">
                                        Hello! I've analyzed your spending for June. Would you like to know if you're on track for your vacation goal?
                                    </div>
                                </div>
                                <div className="flex gap-2 justify-end">
                                    <div className="p-3 rounded-2xl rounded-tr-none bg-accent-blue text-white text-xs shadow-sm leading-relaxed">
                                        Yes, analyze my vacation fund progress.
                                    </div>
                                    <div className="size-8 rounded-full bg-slate-300 dark:bg-slate-700 flex items-center justify-center shrink-0 overflow-hidden border border-slate-200 dark:border-primary/40">
                                        <img className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDIZi-QVLJ4Q1fTiE1N55JvbZufi8Es6JS58y8dbyPHnCCRg6L4X9TzbT1U9eivFdGSVfWhEAyVYxaWjMvwyU0gHXJ_b7rDp52ztEhVzoQqFY-Vls7Fakvaa_Lq3dWwh8e-5DB57XOQ1EQN906VzKrcpiZXpEsHe3mJ3chx8rqHOL3yYWudtYOuHD8guWV-zWwqFyiJpCYs9go-l5PZECy9vfSqOeh-OVEY9I1NMfIsL72NZ4J04VceWxamveA8cYDsOZFdegdClmc" alt="User avatar" />
                                    </div>
                                </div>
                                <div className="flex gap-2 text-slate-900 dark:text-white">
                                    <div className="size-8 rounded-full bg-accent-blue flex items-center justify-center shrink-0">
                                        <span className="material-symbols-outlined text-white text-xs">smart_toy</span>
                                    </div>
                                    <div className="p-3 rounded-2xl rounded-tl-none bg-white dark:bg-primary text-xs shadow-sm border border-slate-100 dark:border-primary/40 leading-relaxed">
                                        Based on your current savings rate, you will reach your $5,000 goal by November 12th—two weeks earlier than planned!
                                        <div className="mt-2 p-2 rounded bg-accent-green/10 text-accent-green border border-accent-green/20">
                                            <span className="font-bold">Pro Tip:</span> Move your unused $150 gym budget this month to hit it by October 25th.
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="p-4 bg-white dark:bg-primary/80 flex flex-col gap-3">
                                <div className="flex flex-wrap gap-2">
                                    <AssistantTag text="Analyze groceries" />
                                    <AssistantTag text="Am I overspending?" />
                                    <AssistantTag text="Investment tips" />
                                </div>
                                <div className="relative">
                                    <input className="w-full rounded-xl border border-slate-200 dark:border-primary/80 bg-slate-50 dark:bg-primary/40 text-xs py-3 pr-10 focus:ring-accent-blue focus:border-accent-blue transition-all dark:text-white outline-none" placeholder="Ask anything about your finances..." type="text" />
                                    <button className="absolute right-2 top-1/2 -translate-y-1/2 text-accent-blue hover:text-accent-teal">
                                        <span className="material-symbols-outlined">send</span>
                                    </button>
                                </div>
                                <p className="text-[9px] text-slate-400 dark:text-slate-500 text-center uppercase tracking-widest font-bold">Bank-Level Encryption Active</p>
                            </div>
                        </div>
                    </aside>
                </main>

                <footer className="p-6 border-t border-slate-200 dark:border-primary/50 text-center text-slate-400 text-xs">
                    <p>© 2023 WealthAI Systems. Secure Data Processing Guaranteed.</p>
                </footer>
            </div>
        </div>
    );
};

const RecommendationCard = ({ icon, color, title, desc }) => (
    <div className="p-4 rounded-xl bg-white dark:bg-primary/20 border-l-4 border-l-current border border-slate-200 dark:border-primary/60 flex gap-4 glow-border transition-all cursor-pointer" style={{ color: `var(--${color}, ${color})` }}>
        <div className="size-12 rounded-full bg-current bg-opacity-10 flex items-center justify-center shrink-0">
            <span className="material-symbols-outlined">{icon}</span>
        </div>
        <div>
            <h4 className="font-bold text-sm text-slate-900 dark:text-white">{title}</h4>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">{desc}</p>
        </div>
    </div>
);

const AssistantTag = ({ text }) => (
    <button className="text-[10px] px-2 py-1 rounded-full border border-slate-200 dark:border-primary text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-primary transition-colors whitespace-nowrap">
        "{text}"
    </button>
);

export default Insights;
