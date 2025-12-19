import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { MessageSquare, Info, FileText, Bot } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export default function NavBar() {
    const location = useLocation();

    const NavLink = ({ to, icon: Icon, children }) => {
        const isActive = location.pathname === to;
        return (
            <Link
                to={to}
                className={twMerge(
                    clsx(
                        "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200",
                        isActive
                            ? "bg-primary-50 text-primary-700"
                            : "text-surface-600 hover:text-surface-900 hover:bg-surface-100"
                    )
                )}
            >
                <Icon className={clsx("w-4 h-4", isActive ? "text-primary-600" : "text-surface-500")} />
                {children}
            </Link>
        );
    };

    return (
        <nav className="sticky top-0 z-50 w-full bg-white/80 backdrop-blur-xl border-b border-surface-200 px-6 py-3 flex items-center justify-between shadow-sm">
            <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-slate-900 shadow-xl shadow-slate-200">
                    <Bot className="w-5 h-5 text-white" />
                </div>
                <div className="flex flex-col">
                    <span className="text-sm font-black text-slate-900 tracking-tighter uppercase leading-none">Clinical Trial</span>
                    <span className="text-[10px] font-medium text-slate-400 tracking-[0.3em] uppercase leading-none mt-1">Intelligence</span>
                </div>
            </div>

            <div className="flex items-center gap-1 bg-surface-50/50 p-1 rounded-xl border border-surface-100">
                <NavLink to="/" icon={MessageSquare}>Chat</NavLink>
                <NavLink to="/about" icon={Info}>About</NavLink>
                <NavLink to="/logs" icon={FileText}>Logs</NavLink>
            </div>
        </nav>
    );
}
