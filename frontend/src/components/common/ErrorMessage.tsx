import React from 'react';

interface ErrorMessageProps {
    message: string;
    onClose: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onClose }) => {
    if (!message) return null;

    return (
        <div style={{
            position: 'fixed',
            top: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            backgroundColor: '#fdezea',
            color: '#c53030',
            border: '1px solid #c53030',
            borderRadius: '4px',
            padding: '1rem',
            zIndex: 1000,
            display: 'flex',
            alignItems: 'center',
            gap: '1rem',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
            <span>{message}</span>
            <button
                onClick={onClose}
                style={{
                    background: 'none',
                    border: 'none',
                    color: '#c53030',
                    fontSize: '1.2rem',
                    cursor: 'pointer',
                    padding: '0 0.5rem',
                    lineHeight: 1
                }}
            >
                ×
            </button>
        </div>
    );
};
