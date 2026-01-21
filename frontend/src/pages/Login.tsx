import { useState } from 'react';
import '../styles/Login.css';

interface LoginProps {
    onSignIn: (email: string, pass: string) => Promise<void>;
    onSignUp: (email: string, pass: string) => Promise<void>;
}

export function Login({ onSignIn, onSignUp }: LoginProps) {
    const [activeTab, setActiveTab] = useState<'login' | 'register'>('login');

    // Login State
    const [loginEmail, setLoginEmail] = useState('');
    const [loginPassword, setLoginPassword] = useState('');

    // Register State
    const [regEmail, setRegEmail] = useState('');
    const [regPassword, setRegPassword] = useState('');

    const handleLoginSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSignIn(loginEmail, loginPassword);
    };

    const handleRegisterSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSignUp(regEmail, regPassword);
    };

    return (
        <div className="login-page">
            {/* Background Elements */}
            <div className="decorative-blob-1"></div>
            <div className="decorative-blob-2"></div>

            <main className="auth-main">
                <div className="auth-header">
                    <h1 className="auth-title">GrantAid</h1>
                </div>

                <div className="auth-card">
                    {/* Tabs */}
                    <div className="auth-tabs">
                        <button
                            className={`tab-button ${activeTab === 'login' ? 'active' : ''}`}
                            onClick={() => setActiveTab('login')}
                        >
                            Login
                        </button>
                        <button
                            className={`tab-button ${activeTab === 'register' ? 'active' : ''}`}
                            onClick={() => setActiveTab('register')}
                        >
                            Create Account
                        </button>
                    </div>

                    <div className="auth-content">
                        {activeTab === 'login' && (
                            <form className="auth-form" onSubmit={handleLoginSubmit}>
                                <div className="input-group">
                                    <label className="input-label" htmlFor="login-email">Institutional Email</label>
                                    <div className="input-wrapper">
                                        <input
                                            id="login-email"
                                            className="auth-input"
                                            type="email"
                                            placeholder="student@university.edu"
                                            value={loginEmail}
                                            onChange={(e) => setLoginEmail(e.target.value)}
                                            required
                                        />
                                    </div>
                                </div>

                                <div className="input-group">
                                    <label className="input-label" htmlFor="login-password">Password</label>
                                    <div className="input-wrapper">
                                        <input
                                            id="login-password"
                                            className="auth-input"
                                            type="password"
                                            value={loginPassword}
                                            onChange={(e) => setLoginPassword(e.target.value)}
                                            required
                                        />
                                    </div>
                                </div>

                                <button type="submit" className="auth-button">
                                    <span>Login</span>
                                </button>
                            </form>
                        )}

                        {activeTab === 'register' && (
                            <form className="auth-form" onSubmit={handleRegisterSubmit}>
                                {/* First/Last name removed as they were not processed */}

                                <div className="input-group">
                                    <label className="input-label" htmlFor="reg-email">Institutional Email</label>
                                    <div className="input-wrapper">
                                        <input
                                            id="reg-email"
                                            className="auth-input"
                                            type="email"
                                            placeholder="student@university.edu"
                                            value={regEmail}
                                            onChange={(e) => setRegEmail(e.target.value)}
                                            required
                                        />
                                    </div>
                                </div>

                                <div className="input-group">
                                    <label className="input-label" htmlFor="reg-password">Password</label>
                                    <input
                                        id="reg-password"
                                        className="auth-input"
                                        type="password"
                                        placeholder="Min. 8 characters"
                                        value={regPassword}
                                        onChange={(e) => setRegPassword(e.target.value)}
                                        required
                                    />
                                </div>

                                <button type="submit" className="auth-button">
                                    Create Account
                                </button>
                            </form>
                        )}
                    </div>
                </div>

                <footer className="page-footer">
                    <p>© 2026 GrantAid. Built for Academia. Montembeault Lab.</p>
                </footer>
            </main>
        </div>
    );
}
