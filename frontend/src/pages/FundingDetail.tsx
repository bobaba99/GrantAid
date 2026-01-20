import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getFundingById, type FundingDefinition } from '../api/funding';

export function FundingDetail() {
    const { id } = useParams<{ id: string }>();
    const [funding, setFunding] = useState<FundingDefinition | null>(null);
    const [error, setError] = useState<string>('');

    useEffect(() => {
        if (id) {
            getFundingById(id)
                .then(setFunding)
                .catch((err) => setError(String(err)));
        }
    }, [id]);

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
    if (!funding) return <div>Loading...</div>;

    return (
        <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
            <h1>{funding.name}</h1>
            <h3>Agency: {funding.agency}</h3>
            <p>Cycle: {funding.cycle_year}</p>
            <p>Deadline: {funding.deadline}</p>
            <a href={funding.website_url} target="_blank" rel="noreferrer">Official Website</a>

            <div style={{ marginTop: '2rem', textAlign: 'left' }}>
                <h2>Context / Instructions</h2>
                <pre style={{ whiteSpace: 'pre-wrap', background: '#f5f5f5', padding: '1rem' }}>
                    {funding.description || 'No description available.'}
                </pre>
            </div>

            <div style={{ marginTop: '2rem' }}>
                <Link to="/fundings">Back to List</Link>
            </div>
        </div>
    );
}
