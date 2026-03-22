import React from 'react';

const Header = ({ title }) => {
    return (
        <header className="sticky top-0 z-10 flex items-center justify-between px-8 py-4 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-md border-b border-slate-200 dark:border-border-dark">
            <div className="flex items-center gap-4">
                <h2 className="text-xl font-bold tracking-tight text-slate-900 dark:text-white">{title}</h2>
                <div className="hidden md:flex items-center bg-slate-100 dark:bg-primary/40 px-3 py-1.5 rounded-lg border border-slate-200 dark:border-border-dark ml-4 w-80">
                    <span className="material-symbols-outlined text-slate-400 text-xl">search</span>
                    <input className="bg-transparent border-none focus:ring-0 text-sm w-full placeholder:text-slate-500 text-slate-900 dark:text-white" placeholder="Search data or transactions..." type="text" />
                </div>
            </div>
            <div className="flex items-center gap-3">
                <button className="p-2 text-slate-500 hover:text-primary dark:hover:text-white transition-colors relative">
                    <span className="material-symbols-outlined">notifications</span>
                    <span className="absolute top-2 right-2 w-2 h-2 bg-accent-error rounded-full"></span>
                </button>
                <button className="p-2 text-slate-500 hover:text-primary dark:hover:text-white transition-colors">
                    <span className="material-symbols-outlined">help_outline</span>
                </button>
                <div className="h-8 w-[1px] bg-slate-200 dark:bg-border-dark mx-2"></div>
                <div className="flex items-center gap-2 px-1 py-1 rounded-full border border-slate-200 dark:border-border-dark">
                    <div className="w-8 h-8 rounded-full bg-cover bg-center overflow-hidden">
                        <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuDTTjQlpokCfwmlmCaCowseJQVnPWD1zowJ_PlqsD5B_fbd9nDKsa63noZKHr4w5yw9hQmNTJd23SdhqBZrQ5S7nCJPpb1nmvPKC1VYCgN9rT4OQmjUSUBKna3lTpxzPjDD33zHQTI9_DEN2nreeU57dTRAkLfG4ThncTVIQmK-gNh6zAxERII277ohi4bMKn_KJv9UCBw2L9EsxAQRMkhz310IGKDjcg8a4lUntfIyAFf6mM8BRuFZQYSmgEBcyoxSu6kY6VxN-lE" alt="User" className="w-full h-full object-cover" />
                    </div>
                    <span className="material-symbols-outlined text-slate-400">expand_more</span>
                </div>
            </div>
        </header>
    );
};

export default Header;
