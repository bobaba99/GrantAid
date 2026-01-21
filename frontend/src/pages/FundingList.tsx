import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getFundings, type FundingDefinition } from '../api/funding';
import '../styles/FundingList.css';

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
                    <p>Your session has expired or is invalid.</p>
                    <Link to="/">Go to Auth Home to Login/Signup</Link>
                </div>
            );
        }
        return <div style={{ color: 'red' }}>Error: {error}</div>;
    }

    return (
        <div className="funding-container">
            <h1 className="funding-title">Available Fundings</h1>
            <br></br>
            <div className="funding-grid">
                {fundings.map((f) => (
                    <div key={f.id} className="funding-card">
                        <div>
                            <h2>{f.name}</h2>
                            <div className="funding-agency">{f.agency}</div>
                            <div className="funding-details">
                                <p><strong>Cycle:</strong> {f.cycle_year}</p>
                                <p><strong>Deadline:</strong> {f.deadline}</p>
                            </div>
                        </div>
                        <Link to={`/funding/${f.id}`} className="view-details-link">View Details</Link>
                    </div>
                ))}
            </div>
        </div>
    );
}
