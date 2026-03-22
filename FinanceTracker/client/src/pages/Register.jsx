import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';

const Register = () => {
    const [formData, setFormData] = useState({ name: '', email: '', password: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const onSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('/auth/register', formData);
            navigate('/login');
        } catch (err) {
            setError(err.response?.data?.msg || 'Registration failed');
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
                        <span className="material-symbols-outlined text-accent text-4xl font-bold">person_add</span>
                    </div>
                    <h1 className="text-4xl font-black text-white tracking-tight mb-2">Create Account</h1>
                    <p className="text-slate-400 font-medium">Join 50,000+ investors using WealthAI</p>
                </div>

                <div className="glass-card p-10 rounded-[2.5rem] shadow-2xl">
                    {error && (
                        <div className="mb-6 p-4 bg-accent-error/10 border border-accent-error/20 rounded-2xl text-accent-error text-sm font-bold flex items-center gap-3 animate-shake">
                            <span className="material-symbols-outlined">error</span>
                            {error}
                        </div>
                    )}

                    <form onSubmit={onSubmit} className="space-y-5">
                        <div className="space-y-2">
                            <label className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] px-1">Full Name</label>
                            <div className="relative group">
                                <span className="absolute left-5 top-1/2 -translate-y-1/2 material-symbols-outlined text-slate-500 group-focus-within:text-accent transition-colors">badge</span>
                                <input
                                    type="text"
                                    required
                                    className="w-full bg-background-dark/40 border border-border-dark focus:border-accent text-white pl-14 pr-6 py-3.5 rounded-2xl transition-all focus:ring-4 focus:ring-accent/10 outline-none placeholder:text-slate-600"
                                    placeholder="Alex Morgan"
                                    onChange={e => setFormData({ ...formData, name: e.target.value })}
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] px-1">Email Address</label>
                            <div className="relative group">
                                <span className="absolute left-5 top-1/2 -translate-y-1/2 material-symbols-outlined text-slate-500 group-focus-within:text-accent transition-colors">alternate_email</span>
                                <input
                                    type="email"
                                    required
                                    className="w-full bg-background-dark/40 border border-border-dark focus:border-accent text-white pl-14 pr-6 py-3.5 rounded-2xl transition-all focus:ring-4 focus:ring-accent/10 outline-none placeholder:text-slate-600"
                                    placeholder="alex@finai.io"
                                    onChange={e => setFormData({ ...formData, email: e.target.value })}
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] px-1">Access Key (Password)</label>
                            <div className="relative group">
                                <span className="absolute left-5 top-1/2 -translate-y-1/2 material-symbols-outlined text-slate-500 group-focus-within:text-accent transition-colors">encrypted</span>
                                <input
                                    type="password"
                                    required
                                    className="w-full bg-background-dark/40 border border-border-dark focus:border-accent text-white pl-14 pr-6 py-3.5 rounded-2xl transition-all focus:ring-4 focus:ring-accent/10 outline-none placeholder:text-slate-600"
                                    placeholder="••••••••••••"
                                    onChange={e => setFormData({ ...formData, password: e.target.value })}
                                />
                            </div>
                        </div>

                        <button type="submit" className="w-full bg-accent hover:bg-emerald-400 text-primary font-black py-5 rounded-2xl transition-all shadow-2xl shadow-accent/20 active:scale-[0.98] flex items-center justify-center gap-3 text-lg mt-4 group">
                            Experience WealthAI
                            <span className="material-symbols-outlined group-hover:translate-x-1 transition-transform">rocket_launch</span>
                        </button>
                    </form>

                    <div className="mt-10 pt-8 border-t border-white/5 text-center">
                        <p className="text-slate-400 font-medium">
                            Already an investor? <Link to="/login" className="text-accent font-black hover:underline ml-1">Sign In</Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Register;
