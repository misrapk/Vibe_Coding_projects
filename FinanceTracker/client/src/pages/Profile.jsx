import React from 'react';
import Sidebar from '../components/Sidebar';

const Profile = () => {
    return (
        <div className="flex h-screen overflow-hidden bg-background-light dark:bg-background-dark text-slate-200 font-display">
            <Sidebar />

            {/* Main Content Area */}
            <main className="flex-1 overflow-y-auto custom-scrollbar bg-background-dark">
                <div className="max-w-5xl mx-auto px-6 py-8">
                    {/* Header & Breadcrumbs */}
                    <div className="mb-8">
                        <nav className="flex text-sm text-slate-500 mb-2 gap-2 items-center">
                            <a className="hover:text-emerald-accent" href="/dashboard">Home</a>
                            <span className="material-symbols-outlined text-xs">chevron_right</span>
                            <span className="text-slate-300">Account Settings</span>
                        </nav>
                        <h2 className="text-3xl font-extrabold text-white tracking-tight">Account Settings</h2>
                        <p className="text-slate-400 mt-1">Manage your profile, security preferences, and subscription status.</p>
                    </div>

                    {/* Profile Summary Section */}
                    <div className="bg-card-dark border border-border-dark rounded-xl p-6 mb-8 flex flex-col md:flex-row md:items-center gap-6">
                        <div className="relative group">
                            <div className="w-24 h-24 rounded-full border-4 border-emerald-accent/20 bg-primary overflow-hidden">
                                <img alt="Profile" className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuA4uEBXI__1tMrp5L2IJr1XtICA-zX6GJKYhmE3RHuIuUfvdAWhqYXw4LFJ6iUzA38H5qYdFcUk8DptALlmRzPVsp1eXXfqMoa-v8ek8TKZKCaXLGbBBc6rBifsUYWt2Nkagu-8qpsCiytUDHKbFncDfUnWuyMbHPmcK6y7eya9s-MBWkF8rNvXqcO6mmbeMivXaL1NJ_JAfaPO9CPMddGhNkgRCZ5ym5TcjDK-4S6uBTgBfsvDVucPGMSIsM4Q1oWeriAhqANbwjI" />
                            </div>
                            <button className="absolute bottom-0 right-0 bg-emerald-accent text-white p-1.5 rounded-full shadow-lg hover:scale-105 transition-transform">
                                <span className="material-symbols-outlined text-sm">photo_camera</span>
                            </button>
                        </div>
                        <div className="flex-1">
                            <h3 className="text-xl font-bold text-white">Alex Thompson</h3>
                            <p className="text-slate-400 text-sm">Member since Oct 12, 2022</p>
                            <div className="mt-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-accent/10 text-emerald-accent border border-emerald-accent/20">
                                Premium Tier
                            </div>
                        </div>
                        <div>
                            <button className="px-5 py-2.5 bg-primary border border-border-dark text-white rounded-lg hover:bg-border-dark transition-colors text-sm font-semibold">
                                Save Changes
                            </button>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        {/* Left Column: Forms */}
                        <div className="lg:col-span-2 space-y-8">
                            {/* Profile Information */}
                            <section className="bg-card-dark border border-border-dark rounded-xl overflow-hidden">
                                <div className="px-6 py-4 border-b border-border-dark flex items-center gap-2">
                                    <span className="material-symbols-outlined text-emerald-accent">person</span>
                                    <h4 className="font-bold text-white uppercase tracking-wider text-xs">Profile Information</h4>
                                </div>
                                <div className="p-6 space-y-4">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div className="space-y-1.5">
                                            <label className="text-xs font-semibold text-slate-400 ml-1">Full Name</label>
                                            <input className="w-full bg-primary border border-border-dark rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-emerald-accent/50 focus:border-emerald-accent outline-none transition-all" type="text" defaultValue="Alex Thompson" />
                                        </div>
                                        <div className="space-y-1.5">
                                            <label className="text-xs font-semibold text-slate-400 ml-1">Phone Number</label>
                                            <input className="w-full bg-primary border border-border-dark rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-emerald-accent/50 focus:border-emerald-accent outline-none transition-all" type="tel" defaultValue="+1 (555) 000-1234" />
                                        </div>
                                    </div>
                                    <div className="space-y-1.5">
                                        <label className="text-xs font-semibold text-slate-400 ml-1">Email Address</label>
                                        <input className="w-full bg-primary border border-border-dark rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-emerald-accent/50 focus:border-emerald-accent outline-none transition-all" type="email" defaultValue="alex.thompson@wealthai.com" />
                                    </div>
                                    <div className="space-y-1.5">
                                        <label className="text-xs font-semibold text-slate-400 ml-1">Timezone</label>
                                        <select className="w-full bg-primary border border-border-dark rounded-lg px-4 py-2.5 text-white focus:ring-2 focus:ring-emerald-accent/50 focus:border-emerald-accent outline-none transition-all">
                                            <option>PST - Pacific Standard Time</option>
                                            <option defaultValue>EST - Eastern Standard Time</option>
                                            <option>GMT - Greenwich Mean Time</option>
                                        </select>
                                    </div>
                                </div>
                            </section>

                            {/* Account Security */}
                            <section className="bg-card-dark border border-border-dark rounded-xl overflow-hidden">
                                <div className="px-6 py-4 border-b border-border-dark flex items-center gap-2">
                                    <span className="material-symbols-outlined text-emerald-accent">shield</span>
                                    <h4 className="font-bold text-white uppercase tracking-wider text-xs">Account Security</h4>
                                </div>
                                <div className="p-6 space-y-6">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <p className="text-white font-medium">Password</p>
                                            <p className="text-slate-400 text-sm">Last changed 3 months ago</p>
                                        </div>
                                        <button className="px-4 py-2 bg-primary border border-border-dark text-slate-200 rounded-lg hover:text-white hover:border-slate-500 transition-all text-sm font-medium">
                                            Change Password
                                        </button>
                                    </div>
                                    <hr className="border-border-dark" />
                                    <div className="flex items-center justify-between">
                                        <div className="max-w-[70%]">
                                            <p className="text-white font-medium">Two-Factor Authentication (2FA)</p>
                                            <p className="text-slate-400 text-sm">Secure your account with an extra layer of protection using an authenticator app.</p>
                                        </div>
                                        {/* Toggle Switch */}
                                        <label className="relative inline-flex items-center cursor-pointer">
                                            <input defaultChecked className="sr-only peer" type="checkbox" />
                                            <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-accent"></div>
                                        </label>
                                    </div>
                                </div>
                            </section>
                        </div>

                        {/* Right Column: Sidebar Widgets */}
                        <div className="space-y-8">
                            {/* Subscription Card */}
                            <section className="bg-card-dark border border-border-dark rounded-xl overflow-hidden">
                                <div className="px-6 py-4 border-b border-border-dark flex items-center gap-2">
                                    <span className="material-symbols-outlined text-emerald-accent">workspace_premium</span>
                                    <h4 className="font-bold text-white uppercase tracking-wider text-xs">Subscription Details</h4>
                                </div>
                                <div className="p-6">
                                    <div className="mb-4">
                                        <p className="text-slate-400 text-xs font-semibold mb-1 uppercase tracking-tight">Current Plan</p>
                                        <p className="text-2xl font-black text-white">Premium</p>
                                    </div>
                                    <div className="space-y-3 mb-6">
                                        <div className="flex justify-between text-sm">
                                            <span className="text-slate-400">Monthly Billing</span>
                                            <span className="text-white font-medium">$49.00 / mo</span>
                                        </div>
                                        <div className="flex justify-between text-sm">
                                            <span className="text-slate-400">Next Billing Date</span>
                                            <span className="text-white font-medium">Oct 12, 2023</span>
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <button className="w-full py-2.5 bg-emerald-accent hover:bg-emerald-hover text-white font-bold rounded-lg transition-all text-sm">
                                            Manage Subscription
                                        </button>
                                        <button className="w-full py-2.5 bg-transparent text-slate-400 hover:text-white transition-all text-xs font-medium">
                                            View Billing History
                                        </button>
                                    </div>
                                </div>
                            </section>

                            {/* Connected Accounts */}
                            <section className="bg-card-dark border border-border-dark rounded-xl p-6">
                                <h4 className="font-bold text-white uppercase tracking-wider text-xs mb-4">Connected Institutions</h4>
                                <div className="space-y-4">
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 rounded bg-blue-600 flex items-center justify-center text-xs font-bold text-white">C</div>
                                        <div className="flex-1">
                                            <p className="text-sm font-medium text-white">Chase Bank</p>
                                            <p className="text-xs text-slate-500">Connected</p>
                                        </div>
                                        <span className="material-symbols-outlined text-emerald-accent text-sm">check_circle</span>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 rounded bg-red-600 flex items-center justify-center text-xs font-bold text-white">V</div>
                                        <div className="flex-1">
                                            <p className="text-sm font-medium text-white">Vanguard</p>
                                            <p className="text-xs text-slate-500">Syncing...</p>
                                        </div>
                                        <div className="w-3 h-3 border-2 border-slate-500 border-t-emerald-accent rounded-full animate-spin"></div>
                                    </div>
                                </div>
                                <button className="mt-6 w-full py-2 border border-border-dark hover:border-emerald-accent/50 text-slate-300 hover:text-emerald-accent transition-all rounded-lg text-xs font-semibold flex items-center justify-center gap-2">
                                    <span className="material-symbols-outlined text-sm">add</span>
                                    Add Account
                                </button>
                            </section>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Profile;
