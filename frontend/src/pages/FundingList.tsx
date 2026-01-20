import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getFundings, type FundingDefinition } from '../api/funding';

export function FundingList() {
    const [fundings, setFundings] = useState<FundingDefinition[]>([]);
    const [error, setError] = useState<string>('');

    useEffect(() => {
        getFundings()
            .then(setFundings)
            .catch((err) => setError(String(err)));
    }, []);

    if (error) {
        if (error.includes('401')) {
            return (
                <div style={{ padding: '2rem', color: 'red' }}>
                    <h2>Authentication Required</h2>
                    <p>Your session has expired or is invalid (did you reset the database?).</p>
                    <Link to="/">Go to Auth Home to Login/Signup</Link>
                </div>
            );
        }
        return <div style={{ color: 'red' }}>Error: {error}</div>;
    }

    return (
        <div style={{ padding: '2rem' }}>
            <h1>Available Grants</h1>
            <div style={{ display: 'grid', gap: '1rem' }}>
                {fundings.map((f) => (
                    <div key={f.id} style={{ border: '1px solid #ccc', padding: '1rem' }}>
                        <h2>{f.name} ({f.agency})</h2>
                        <p>Deadline: {f.deadline}</p>
                        <Link to={`/funding/${f.id}`}>View Details</Link>
                    </div>
                ))}
            </div>
            <div style={{ marginTop: '2rem' }}>
                <Link to="/">Back to Home</Link>
            </div>
        </div>
    );
}
