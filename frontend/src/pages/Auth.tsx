import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signIn, signUp } from '../api/auth';

export function AuthPage() {
    const navigate = useNavigate();

    // Form state
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');

    // Feedback state
    const [error, setError] = useState<string | null>(null);
    const [successMsg, setSuccessMsg] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setSuccessMsg(null);
        setLoading(true);

        try {
            if (isLogin) {
                // Sign In
                await signIn(email, password);
                // On success, redirect to profile
                navigate('/profile');
            } else {
                // Sign Up
                await signUp(email, password, username);
                setSuccessMsg("Sign up successful! Please check your email for verification.");
                // Optionally switch to login mode or clear form
                setIsLogin(true);
            }
        } catch (err: any) {
            // Extract error message/code
            const msg = err.message || "An unexpected error occurred";
            setError(msg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: '2rem auto', textAlign: 'center' }}>
            <h2>{isLogin ? 'Sign In' : 'Create Account'}</h2>

            {error && (
                <div style={{ padding: '1rem', background: '#ffebee', color: '#c62828', marginBottom: '1rem', borderRadius: '4px' }}>
                    <strong>Error:</strong> {error}
                </div>
            )}

            {successMsg && (
                <div style={{ padding: '1rem', background: '#e8f5e9', color: '#2e7d32', marginBottom: '1rem', borderRadius: '4px' }}>
                    {successMsg}
                </div>
            )}

            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {!isLogin && (
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required={!isLogin}
                        style={{ padding: '0.8rem', fontSize: '1rem' }}
                    />
                )}

                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    style={{ padding: '0.8rem', fontSize: '1rem' }}
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    style={{ padding: '0.8rem', fontSize: '1rem' }}
                />

                <button
                    type="submit"
                    disabled={loading}
                    style={{ padding: '0.8rem', fontSize: '1rem', cursor: 'pointer', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}
                >
                    {loading ? 'Processing...' : (isLogin ? 'Sign In' : 'Sign Up')}
                </button>
            </form>

            <p style={{ marginTop: '1rem', fontSize: '0.9rem' }}>
                {isLogin ? "Don't have an account? " : "Already have an account? "}
                <button
                    onClick={() => {
                        setIsLogin(!isLogin);
                        setError(null);
                        setSuccessMsg(null);
                    }}
                    style={{ background: 'none', border: 'none', color: '#007bff', textDecoration: 'underline', cursor: 'pointer' }}
                >
                    {isLogin ? 'Sign Up' : 'Sign In'}
                </button>
            </p>
        </div>
    );
}
