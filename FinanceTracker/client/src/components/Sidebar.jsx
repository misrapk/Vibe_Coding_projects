import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const Sidebar = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const handleSignOut = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <aside className="w-64 flex-shrink-0 bg-primary border-r border-border-dark hidden lg:flex flex-col">
            <div className="p-6 flex items-center gap-3">
                <div className="bg-white/10 rounded-lg p-2">
                    <span className="material-symbols-outlined text-white text-2xl">insights</span>
                </div>
                <div>
                    <h1 className="text-white text-lg font-bold leading-tight">Financial AI</h1>
                    <p className="text-slate-400 text-xs uppercase tracking-wider font-semibold">Premium</p>
                </div>
            </div>
            <nav className="flex-1 px-4 py-4 space-y-1">
                <SidebarLink
                    icon="dashboard"
                    label="Overview"
                    active={location.pathname === '/dashboard'}
                    onClick={() => navigate('/dashboard')}
                />
                <SidebarLink
                    icon="receipt_long"
                    label="Transactions"
                    active={location.pathname === '/transactions'}
                    onClick={() => navigate('/dashboard')}
                />
                <SidebarLink
                    icon="monitoring"
                    label="Investments"
                    onClick={() => navigate('/insights')}
                    active={location.pathname === '/insights'}
                />
                <SidebarLink
                    icon="account_balance_wallet"
                    label="Budgeting"
                    onClick={() => navigate('/dashboard')}
                />
                <SidebarLink
                    icon="settings"
                    label="Settings"
                    active={location.pathname === '/profile'}
                    onClick={() => navigate('/profile')}
                />
            </nav>
            <div className="p-4 mt-auto">
                <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                    <div className="flex items-center gap-3 mb-3">
                        <div className="w-10 h-10 rounded-full bg-cover bg-center overflow-hidden">
                            <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuAry_ktFG3vDaD12cPZDCfeEFyJLUjUI0AYV8BVN73nrWq9TtBSK3EZuBr6AoRiZ2VpttlCJnf9vT7-cOiMZR6vPWsMW6Zc_d_90P-ixT_WKXmKbLzq77j2G4hdtHuwj4G6nXKatBKbRcbf35pzCQXD6jYWgwc8cv2JmvCn1W7UepbYaWv1S9O2yZKERCdpNZjJNIe_7YUv94EEhMjvwIepo2GFf3Ok911YGsdJE64kijTsv40nIGhwMO_sr7f-VNKPrGKqdsIYUVw" alt="Alex Morgan" className="w-full h-full object-cover" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-semibold text-white truncate">Alex Morgan</p>
                            <p className="text-xs text-slate-400 truncate">alex@finai.io</p>
                        </div>
                    </div>
                    <button onClick={handleSignOut} className="w-full text-xs font-bold text-white bg-white/10 hover:bg-white/20 py-2 rounded-lg transition-colors uppercase tracking-widest">Sign Out</button>
                </div>
            </div>
        </aside>
    );
};

const SidebarLink = ({ icon, label, active = false, onClick }) => (
    <button
        onClick={onClick}
        className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg font-medium transition-colors ${active ? 'bg-white/10 text-white' : 'text-slate-400 hover:text-white hover:bg-white/5'}`}
    >
        <span className={`material-symbols-outlined ${active ? 'filled' : ''}`}>{icon}</span>
        <span>{label}</span>
    </button>
);

export default Sidebar;
