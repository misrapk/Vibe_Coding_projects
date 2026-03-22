import React from 'react';
import { useNavigate } from 'react-router-dom';

const Landing = () => {
    const navigate = useNavigate();

    return (
        <div className="bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 antialiased font-display min-h-screen">
            {/* Top Navigation */}
            <header className="sticky top-0 z-50 w-full border-b border-border-dark bg-background-dark/80 backdrop-blur-md">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center gap-2">
                            <div className="bg-accent p-1.5 rounded-lg flex items-center justify-center">
                                <span className="material-symbols-outlined text-primary text-2xl font-bold">query_stats</span>
                            </div>
                            <span className="text-white text-xl font-extrabold tracking-tight">WealthAI</span>
                        </div>
                        <nav className="hidden md:flex items-center gap-8">
                            <a className="text-slate-300 hover:text-accent transition-colors text-sm font-medium" href="#features">Features</a>
                            <a className="text-slate-300 hover:text-accent transition-colors text-sm font-medium" href="#">Solutions</a>
                            <a className="text-slate-300 hover:text-accent transition-colors text-sm font-medium" href="#">Pricing</a>
                            <a className="text-slate-300 hover:text-accent transition-colors text-sm font-medium" href="#">Resources</a>
                        </nav>
                        <div className="flex items-center gap-4">
                            <button onClick={() => navigate('/login')} className="text-white hover:text-accent text-sm font-bold transition-colors px-4 py-2">Login</button>
                            <button onClick={() => navigate('/register')} className="bg-accent hover:bg-accent/90 text-primary px-5 py-2.5 rounded-lg text-sm font-bold transition-all shadow-lg shadow-accent/10">
                                Get Started
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            <main>
                {/* Hero Section */}
                <section className="relative overflow-hidden pt-16 pb-24 lg:pt-32 lg:pb-40">
                    {/* Background Radial Glow */}
                    <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-1/4 w-[600px] h-[600px] bg-accent/10 rounded-full blur-[120px] pointer-events-none"></div>
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
                        <div className="grid lg:grid-cols-2 gap-12 items-center">
                            <div className="space-y-8">
                                <div>
                                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold tracking-wider uppercase bg-accent/10 text-accent mb-4 border border-accent/20">
                                        <span className="material-symbols-outlined text-sm mr-1">bolt</span> Now in Beta
                                    </span>
                                    <h1 className="text-5xl lg:text-7xl font-black text-white leading-[1.1] tracking-tight">
                                        Master Your Wealth with <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent to-emerald-400">Intelligence</span>
                                    </h1>
                                    <p className="mt-6 text-xl text-slate-400 leading-relaxed max-w-xl">
                                        AI-driven insights that automate your tracking and optimize your investments. Trusted by 50,000+ investors worldwide.
                                    </p>
                                </div>
                                <div className="flex flex-col sm:flex-row gap-4">
                                    <button onClick={() => navigate('/register')} className="bg-accent hover:bg-accent/90 text-primary px-8 py-4 rounded-xl text-lg font-bold transition-all flex items-center justify-center gap-2 group">
                                        Start Your Free Trial
                                        <span className="material-symbols-outlined transition-transform group-hover:translate-x-1">arrow_forward</span>
                                    </button>
                                    <button className="bg-primary border border-border-dark hover:bg-primary/80 text-white px-8 py-4 rounded-xl text-lg font-bold transition-all">
                                        View Demo
                                    </button>
                                </div>
                                <div className="flex items-center gap-6 pt-4">
                                    <div className="flex -space-x-3">
                                        <img alt="User portrait" className="h-10 w-10 rounded-full border-2 border-background-dark object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuD6ICR57nemfUn44vzwKy-zUj1WWqP07fK3imbC42R6jneIZnifO3bbW1lk2ugqKhKe1ByjHb3COdehKEIKnb5V5QqSAom298_6YebTgs3iQ3E4QYJAacDelBiz14plb4Mxp65CTGx2h-J3PNHmzleuFqc4fdtvP34w_U8xynuXO2vuf0A7aTF_yj0VyC4kYIsSFkp_43GkZ6SerTN6xy_PvPDJKDFR1UNJ-Ty9Pm9cCxXELR6d9ecshHewa8HGf00Y18vfynSeqMk" />
                                        <img alt="User portrait" className="h-10 w-10 rounded-full border-2 border-background-dark object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCwkvAInHQ2IYm836suPOnYteoZXL9kDYa1T4lV7KFyJTI9W4XCXkE_uW_dBcbizRqvCgozc1s8haWUiahUbks6Q1Zbjoqdj8RU5TunB4si9a3KmsO9lZBXRn4KR2g0nEP2GF0l6o6gcieNF3BvLxlvTExz-6RZY9CpEhK-vh18LNoDkLkkkIc29rNcD_biqonqUOMeRsr3Jj8v5J3yBm_AAsd3Oi3KG0rB1quzTwf4kDoxIp_prhLJVCf-HudDvWSFh68ZbpeVtp0" />
                                        <img alt="User portrait" className="h-10 w-10 rounded-full border-2 border-background-dark object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBa4w_ksXbKeol-PyDsP6oHSXKci3mLbUohtS7cehPzquq7Kx7mnxufHrTjGHy75P5E2aid1MvAPqRnMRgrlSr83v5U5eZCMs_cX6WUNFH0Jy6muLtXVtAcEAme1bAjSoopO-NLS7wJ7S6ddQpZ3y_lihkKT4RLOxyOxA0HTH46z59SHnwu-3CjWcO5PAG8lB2KeWqnSKDTmZeAGKMU3VfN7v6Phw1-pJIWtrr2ZQ8KU-eizOlN7RcEpl9r9a-3lyJPa_4fwiXl0Uo" />
                                    </div>
                                    <div className="text-sm">
                                        <p className="text-white font-bold">4.9/5 Rating</p>
                                        <p className="text-slate-500">from 2,000+ verified reviews</p>
                                    </div>
                                </div>
                            </div>
                            <div className="relative">
                                <div className="glass-card rounded-2xl p-6 shadow-2xl relative z-20 overflow-hidden">
                                    <div className="flex justify-between items-center mb-6">
                                        <div>
                                            <h3 className="text-white font-bold text-lg">Portfolio Overview</h3>
                                            <p className="text-slate-400 text-xs">AI Predicted Projection</p>
                                        </div>
                                        <div className="bg-accent/20 text-accent px-2 py-1 rounded text-xs font-bold">
                                            +18.4% YoY
                                        </div>
                                    </div>
                                    {/* Large Abstract Graph (SVG) */}
                                    <div className="h-64 w-full relative">
                                        <svg className="w-full h-full" preserveAspectRatio="none" viewBox="0 0 400 200">
                                            <defs>
                                                <linearGradient id="chartGradient" x1="0%" x2="0%" y1="0%" y2="100%">
                                                    <stop offset="0%" stopColor="#0bda5b" stopOpacity="0.3"></stop>
                                                    <stop offset="100%" stopColor="#0bda5b" stopOpacity="0"></stop>
                                                </linearGradient>
                                            </defs>
                                            <path d="M0,180 C50,160 80,190 120,140 S200,80 250,110 S350,20 400,40 L400,200 L0,200 Z" fill="url(#chartGradient)"></path>
                                            <path d="M0,180 C50,160 80,190 120,140 S200,80 250,110 S350,20 400,40" fill="none" stroke="#0bda5b" strokeLinecap="round" strokeWidth="4"></path>
                                            {/* Data Points */}
                                            <circle cx="120" cy="140" fill="#0bda5b" r="4"></circle>
                                            <circle cx="250" cy="110" fill="#0bda5b" r="4"></circle>
                                            <circle cx="400" cy="40" fill="#0bda5b" r="6"></circle>
                                        </svg>
                                        <div className="absolute top-4 right-10 bg-white/10 border border-white/20 p-2 rounded-lg backdrop-blur-sm text-[10px] text-white">
                                            <p className="font-bold">Next Quarter</p>
                                            <p className="text-accent">+$14,200 Est.</p>
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-3 gap-4 mt-6 pt-6 border-t border-white/10">
                                        <div>
                                            <p className="text-slate-500 text-[10px] uppercase font-bold tracking-wider">Net Worth</p>
                                            <p className="text-white text-lg font-black">$428,500</p>
                                        </div>
                                        <div>
                                            <p className="text-slate-500 text-[10px] uppercase font-bold tracking-wider">Active Assets</p>
                                            <p className="text-white text-lg font-black">12</p>
                                        </div>
                                        <div>
                                            <p className="text-slate-500 text-[10px] uppercase font-bold tracking-wider">Risk Score</p>
                                            <p className="text-accent text-lg font-black">Low</p>
                                        </div>
                                    </div>
                                </div>
                                {/* Decorative elements behind the card */}
                                <div className="absolute -bottom-6 -left-6 w-32 h-32 bg-accent/20 rounded-full blur-2xl"></div>
                                <div className="absolute -top-10 right-1/4 w-48 h-48 bg-blue-500/10 rounded-full blur-3xl"></div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Stats Section */}
                <section className="py-12 bg-primary/30 border-y border-border-dark">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">
                            <div>
                                <p className="text-slate-500 text-sm font-medium mb-1">Assets Managed</p>
                                <p className="text-white text-3xl font-black">$2.4B+</p>
                            </div>
                            <div>
                                <p className="text-slate-500 text-sm font-medium mb-1">Active Users</p>
                                <p className="text-white text-3xl font-black">50k+</p>
                            </div>
                            <div>
                                <p className="text-slate-500 text-sm font-medium mb-1">Financial Partners</p>
                                <p className="text-white text-3xl font-black">10,000+</p>
                            </div>
                            <div>
                                <p className="text-slate-500 text-sm font-medium mb-1">Security Rating</p>
                                <p className="text-accent text-3xl font-black">AAA</p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Features Section */}
                <section className="py-24 lg:py-32" id="features">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="max-w-3xl mb-16">
                            <h2 className="text-accent text-sm font-bold tracking-widest uppercase mb-4">Intelligent Capabilities</h2>
                            <h3 className="text-4xl lg:text-5xl font-black text-white leading-tight">
                                Our AI works around the clock to ensure your capital is always optimized.
                            </h3>
                            <p className="mt-6 text-lg text-slate-400">
                                Stop manually updating spreadsheets. Let our advanced algorithms handle the complexity while you enjoy the growth.
                            </p>
                        </div>
                        <div className="grid md:grid-cols-3 gap-8">
                            {/* Feature 1 */}
                            <div className="group bg-card-dark border border-border-dark p-8 rounded-2xl hover:border-accent/50 transition-all duration-300">
                                <div className="w-14 h-14 bg-accent/10 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                                    <span className="material-symbols-outlined text-accent text-3xl">receipt_long</span>
                                </div>
                                <h4 className="text-xl font-bold text-white mb-3">Automated Expense Tracking</h4>
                                <p className="text-slate-400 leading-relaxed mb-6">
                                    Real-time categorization of every transaction across all your accounts. Our AI learns your spending patterns to provide hyper-accurate budgeting.
                                </p>
                                <ul className="space-y-3">
                                    <li className="flex items-center gap-2 text-sm text-slate-300">
                                        <span className="material-symbols-outlined text-accent text-lg">check_circle</span> Auto-reconciliation
                                    </li>
                                    <li className="flex items-center gap-2 text-sm text-slate-300">
                                        <span className="material-symbols-outlined text-accent text-lg">check_circle</span> Smart tax tagging
                                    </li>
                                </ul>
                            </div>
                            {/* Feature 2 */}
                            <div className="group bg-card-dark border border-border-dark p-8 rounded-2xl hover:border-accent/50 transition-all duration-300">
                                <div className="w-14 h-14 bg-accent/10 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                                    <span className="material-symbols-outlined text-accent text-3xl">psychology</span>
                                </div>
                                <h4 className="text-xl font-bold text-white mb-3">Investment Insights</h4>
                                <p className="text-slate-400 leading-relaxed mb-6">
                                    Predictive modeling and AI-driven strategies to grow your portfolio. Get alerts on market trends and personalized diversification advice.
                                </p>
                                <ul className="space-y-3">
                                    <li className="flex items-center gap-2 text-sm text-slate-300">
                                        <span className="material-symbols-outlined text-accent text-lg">check_circle</span> Risk-profile balancing
                                    </li>
                                    <li className="flex items-center gap-2 text-sm text-slate-300">
                                        <span className="material-symbols-outlined text-accent text-lg">check_circle</span> Opportunity detection
                                    </li>
                                </ul>
                            </div>
                            {/* Feature 3 */}
                            <div className="group bg-card-dark border border-border-dark p-8 rounded-2xl hover:border-accent/50 transition-all duration-300">
                                <div className="w-14 h-14 bg-accent/10 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                                    <span className="material-symbols-outlined text-accent text-3xl">shield_locked</span>
                                </div>
                                <h4 className="text-xl font-bold text-white mb-3">Secure Banking</h4>
                                <p className="text-slate-400 leading-relaxed mb-6">
                                    AES-256 encrypted connections to 10,000+ financial institutions. Bank-level security protocols ensure your data remains your own.
                                </p>
                                <ul className="space-y-3">
                                    <li className="flex items-center gap-2 text-sm text-slate-300">
                                        <span className="material-symbols-outlined text-accent text-lg">check_circle</span> SOC2 Type II Certified
                                    </li>
                                    <li className="flex items-center gap-2 text-sm text-slate-300">
                                        <span className="material-symbols-outlined text-accent text-lg">check_circle</span> Multi-factor protection
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Trust / Social Proof */}
                <section className="py-20 bg-primary overflow-hidden relative">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="flex flex-col lg:flex-row items-center justify-between gap-12">
                            <div className="lg:w-1/2">
                                <h2 className="text-3xl font-black text-white mb-6">Trusted by world-class financial partners</h2>
                                <div className="flex flex-wrap gap-8 opacity-40">
                                    <div className="flex items-center gap-2">
                                        <span className="material-symbols-outlined text-white text-3xl">verified_user</span>
                                        <span className="text-white font-bold text-xl uppercase tracking-widest">SecureBank</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <span className="material-symbols-outlined text-white text-3xl">token</span>
                                        <span className="text-white font-bold text-xl uppercase tracking-widest">Ethos</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <span className="material-symbols-outlined text-white text-3xl">corporate_fare</span>
                                        <span className="text-white font-bold text-xl uppercase tracking-widest">GlobalFin</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <span className="material-symbols-outlined text-white text-3xl">assured_workload</span>
                                        <span className="text-white font-bold text-xl uppercase tracking-widest">VaultX</span>
                                    </div>
                                </div>
                            </div>
                            <div className="lg:w-1/2 bg-accent p-12 rounded-3xl relative overflow-hidden">
                                <div className="absolute -right-10 -top-10">
                                    <span className="material-symbols-outlined text-primary/10 text-[200px] font-black rotate-12">format_quote</span>
                                </div>
                                <p className="text-primary text-2xl font-bold relative z-10 italic">
                                    "WealthAI transformed how I manage my family's future. The AI insights caught an investment opportunity I would have otherwise missed. Highly recommended."
                                </p>
                                <div className="mt-8 flex items-center gap-4 relative z-10">
                                    <img alt="Sarah Johnson" className="w-14 h-14 rounded-full border-4 border-white/20 object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBBMwj5Ymq_tquBKUFKhahjEMnr9xa0_fWWPHWo7Ao7lDRTggRtFNTCoXfEK9gJEvBpdwss-lAZz-PCdcA-UKxq5yA60RBCKFrKdtLxEGBA-gGfOI-xKW3OcJinm8G8JDDnnAt5MuBCWV28huCZjfVjexvkEZTKLloGHlNuEgc4wIXy6kaDITgm5zzV3jrBEsra1KGTdRNdlkU4lHOgy4wWk_bkJwuUeSCVAehNj1ByuWK2qxthktIxJ8mr-dpGEgnWeEtKjo_NRIQ" />
                                    <div>
                                        <p className="text-primary font-black">Marcus Chen</p>
                                        <p className="text-primary/70 font-medium">Managing Director, Venture Solutions</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* CTA Section */}
                <section className="py-24 lg:py-40 relative">
                    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                        <h2 className="text-4xl lg:text-6xl font-black text-white mb-8 tracking-tight">
                            Ready to take control of your financial destiny?
                        </h2>
                        <p className="text-xl text-slate-400 mb-12 max-w-2xl mx-auto leading-relaxed">
                            Join over 50,000 users who are already using WealthAI to automate their savings, investments, and financial future.
                        </p>
                        <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
                            <button onClick={() => navigate('/register')} className="w-full sm:w-auto bg-accent hover:bg-accent/90 text-primary px-10 py-5 rounded-2xl text-xl font-black transition-all shadow-xl shadow-accent/20">
                                Start Growing Today
                            </button>
                            <button className="w-full sm:w-auto border border-border-dark bg-background-dark/50 hover:bg-background-dark text-white px-10 py-5 rounded-2xl text-xl font-bold transition-all">
                                Talk to an Advisor
                            </button>
                        </div>
                        <p className="mt-8 text-slate-500 text-sm">
                            No credit card required. Cancel anytime.
                        </p>
                    </div>
                </section>
            </main>

            {/* Footer */}
            <footer className="bg-background-dark border-t border-border-dark pt-20 pb-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-2 lg:grid-cols-5 gap-12 mb-20">
                        <div className="col-span-2">
                            <div className="flex items-center gap-2 mb-6">
                                <div className="bg-accent p-1 rounded flex items-center justify-center">
                                    <span className="material-symbols-outlined text-primary text-xl font-bold">query_stats</span>
                                </div>
                                <span className="text-white text-xl font-extrabold tracking-tight">WealthAI</span>
                            </div>
                            <p className="text-slate-400 max-w-sm mb-8">
                                The world's most advanced AI-powered wealth management platform. Built for the modern investor who values intelligence and security.
                            </p>
                            <div className="flex gap-4">
                                <a className="w-10 h-10 rounded-full bg-card-dark border border-border-dark flex items-center justify-center text-slate-400 hover:text-accent hover:border-accent transition-all" href="#">
                                    <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"></path></svg>
                                </a>
                                <a className="w-10 h-10 rounded-full bg-card-dark border border-border-dark flex items-center justify-center text-slate-400 hover:text-accent hover:border-accent transition-all" href="#">
                                    <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"></path></svg>
                                </a>
                            </div>
                        </div>
                        <div>
                            <h5 className="text-white font-bold mb-6">Product</h5>
                            <ul className="space-y-4 text-sm text-slate-400">
                                <li><a className="hover:text-accent transition-colors" href="#">Wealth Tracking</a></li>
                                <li><a className="hover:text-accent transition-colors" href="#">AI Analysis</a></li>
                                <li><a className="hover:text-accent transition-colors" href="#">Tax Optimizer</a></li>
                                <li><a className="hover:text-accent transition-colors" href="#">Connections</a></li>
                            </ul>
                        </div>
                        <div>
                            <h5 className="text-white font-bold mb-6">Company</h5>
                            <ul className="space-y-4 text-sm text-slate-400">
                                <li><a className="hover:text-accent transition-colors" href="#">About Us</a></li>
                                <li><a className="hover:text-accent transition-colors" href="#">Careers</a></li>
                                <li><a className="hover:text-accent transition-colors" href="#">Newsroom</a></li>
                                <li><a className="hover:text-accent transition-colors" href="#">Contact</a></li>
                            </ul>
                        </div>
                        <div>
                            <h5 className="text-white font-bold mb-6">Legal</h5>
                            <ul className="space-y-4 text-sm text-slate-400">
                                <li><a className="hover:text-accent transition-colors" href="#">Privacy Policy</a></li>
                                <li><a className="hover:text-accent transition-colors" href="#">Terms of Service</a></li>
                                <li><a className="hover:text-accent transition-colors" href="#">Cookie Policy</a></li>
                                <li><a className="hover:text-accent transition-colors" href="#">Security</a></li>
                            </ul>
                        </div>
                    </div>
                    <div className="border-t border-border-dark pt-10 flex flex-col md:flex-row justify-between items-center gap-6">
                        <p className="text-slate-500 text-xs text-center md:text-left">
                            © 2024 WealthAI Technologies Inc. All rights reserved. WealthAI is a financial technology platform, not a bank. Banking services are provided by our partner banks.
                        </p>
                        <div className="flex gap-6 text-xs text-slate-500">
                            <a className="hover:text-accent" href="#">Disclosure</a>
                            <a className="hover:text-accent" href="#">Accessibility</a>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Landing;
