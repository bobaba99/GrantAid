
import { useState, useEffect } from 'react';

interface SuccessModalProps {
    onClose: () => void;
    email?: string;
}

export function SuccessModal({ onClose, email }: SuccessModalProps) {
    const [timeLeft, setTimeLeft] = useState(5);

    useEffect(() => {
        if (timeLeft <= 0) {
            onClose();
            return;
        }
        const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
        return () => clearTimeout(timer);
    }, [timeLeft, onClose]);

    return (
        <div className="modal-overlay" style={{ zIndex: 1100 }}>
            <div className="modal-content" style={{ textAlign: 'center', maxWidth: '400px', padding: '2.5rem' }}>
                <div style={{
                    width: '4rem', height: '4rem', backgroundColor: '#dcfce7', color: '#166534',
                    borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                    margin: '0 auto 1.5rem auto', fontSize: '2rem'
                }}>
                    ✓
                </div>
                <h2 style={{ fontSize: '1.5rem', fontWeight: '700', color: '#0e181b', marginBottom: '1rem' }}>
                    Welcome to GrantAid!
                </h2>
                <p style={{ color: '#508995', marginBottom: '2rem', lineHeight: '1.6' }}>
                    Your account has been successfully created. {email && <span>(<strong>{email}</strong>)</span>}
                    <br /><br />
                    Email confirmation is currently disabled. You will be redirected to your profile in <strong>{timeLeft} seconds</strong>...
                </p>
                <button
                    style={{
                        padding: '0.75rem 1.5rem',
                        backgroundColor: '#0e4e5d',
                        color: 'white',
                        border: 'none',
                        borderRadius: '0.5rem',
                        fontWeight: 600,
                        cursor: 'pointer',
                        width: '100%',
                        fontSize: '1rem',
                        transition: 'background-color 0.2s'
                    }}
                    onClick={onClose}
                >
                    Go to Profile Now
                </button>
            </div>
        </div>
    );
}
