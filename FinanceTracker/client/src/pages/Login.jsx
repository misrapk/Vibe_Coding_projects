import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';

const Login = () => {
    const [loginData, setLoginData] = useState({ email: '', password: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const onSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await api.post('/auth/login', loginData);
            localStorage.setItem('token', res.data.token);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.msg || 'Invalid credentials');
        }
    };

    return (
        <div className="min-h-screen bg-background-dark flex items-center justify-center p-4 font-display relative overflow-hidden">
            {/* Background Glows */}
            <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-1/4 w-[600px] h-[600px] bg-accent/10 rounded-full blur-[120px] pointer-events-none"></div>
            <div className="absolute bottom-0 left-0 translate-y-1/2 -translate-x-1/4 w-[500px] h-[500px] bg-blue-500/10 rounded-full blur-[120px] pointer-events-none"></div>

            <div className="w-full max-w-md relative z-10">
                <div className="text-center mb-10">
                    <div onClick={() => navigate('/')} className="inline-flex items-center justify-center p-4 bg-accent/20 rounded-2xl mb-6 border border-accent/20 cursor-pointer hover:scale-105 transition-transform">
                        <span className="material-symbols-outlined text-accent text-4xl font-bold">query_stats</span>
                    </div>
                    <h1 className="text-4xl font-black text-white tracking-tight mb-2">Welcome Back</h1>
                    <p className="text-slate-400 font-medium">Log in to your financial intelligence engine</p>
                </div>

                <div className="glass-card p-10 rounded-[2.5rem] shadow-2xl">
                    {error && (
                        <div className="mb-6 p-4 bg-accent-error/10 border border-accent-error/20 rounded-2xl text-accent-error text-sm font-bold flex items-center gap-3 animate-shake">
                            <span className="material-symbols-outlined">error</span>
                            {error}
                        </div>
                    )}

                    <form onSubmit={onSubmit} className="space-y-6">
                        <div className="space-y-2">
                            <label className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] px-1">Institutional Email</label>
                            <div className="relative group">
                                <span className="absolute left-5 top-1/2 -translate-y-1/2 material-symbols-outlined text-slate-500 group-focus-within:text-accent transition-colors">alternate_email</span>
                                <input
                                    type="email"
                                    required
                                    className="w-full bg-background-dark/40 border border-border-dark focus:border-accent text-white pl-14 pr-6 py-4 rounded-2xl transition-all focus:ring-4 focus:ring-accent/10 outline-none placeholder:text-slate-600"
                                    placeholder="name@company.com"
                                    onChange={e => setLoginData({ ...loginData, email: e.target.value })}
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <div className="flex justify-between items-center px-1">
                                <label className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Secure Password</label>
                                <a href="#" className="text-[10px] font-black text-accent hover:text-white transition-colors uppercase tracking-widest">Forgot Access?</a>
                            </div>
                            <div className="relative group">
                                <span className="absolute left-5 top-1/2 -translate-y-1/2 material-symbols-outlined text-slate-500 group-focus-within:text-accent transition-colors">encrypted</span>
                                <input
                                    type="password"
                                    required
                                    className="w-full bg-background-dark/40 border border-border-dark focus:border-accent text-white pl-14 pr-6 py-4 rounded-2xl transition-all focus:ring-4 focus:ring-accent/10 outline-none placeholder:text-slate-600"
                                    placeholder="••••••••••••"
                                    onChange={e => setLoginData({ ...loginData, password: e.target.value })}
                                />
                            </div>
                        </div>

                        <button type="submit" className="w-full bg-accent hover:bg-emerald-400 text-primary font-black py-5 rounded-2xl transition-all shadow-2xl shadow-accent/20 active:scale-[0.98] flex items-center justify-center gap-3 text-lg mt-4 group">
                            Unlock Dashboard
                            <span className="material-symbols-outlined group-hover:translate-x-1 transition-transform">arrow_forward_ios</span>
                        </button>
                    </form>

                    <div className="mt-10 pt-8 border-t border-white/5 text-center">
                        <p className="text-slate-400 font-medium">
                            New to WealthAI? <Link to="/register" className="text-accent font-black hover:underline ml-1">Establish Account</Link>
                        </p>
                    </div>
                </div>

                <p className="mt-8 text-center text-slate-600 text-xs font-bold uppercase tracking-[0.2em]">
                    Bank-Level 256-bit Encryption
                </p>
            </div>
        </div>
    );
};

export default Login;
