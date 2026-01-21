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
        <div style={{ padding: '2rem', width: '100%', margin: '0 auto' }}>
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

            <ExperiencesAnalysisSection fundingId={id!} />

            <div style={{ marginTop: '2rem' }}>
                <Link to="/fundings">Back to List</Link>
            </div>
        </div>
    );
}

import { analyzeExperiences, type ExperienceAnalysis } from '../api/funding';

function ExperiencesAnalysisSection({ fundingId }: { fundingId: string }) {
    const [analyses, setAnalyses] = useState<ExperienceAnalysis[] | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleAnalyze = async () => {
        setLoading(true);
        setError('');
        try {
            const data = await analyzeExperiences(fundingId);
            setAnalyses(data);
        } catch (err) {
            setError('Failed to analyze experiences: ' + String(err));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ marginTop: '2rem', borderTop: '1px solid #ccc', paddingTop: '1rem' }}>
            <h2>My Relevant Experiences</h2>
            <p>See how your experiences align with this funding opportunity.</p>

            {!analyses && !loading && (
                <button onClick={handleAnalyze} style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}>
                    Analyze My Experiences
                </button>
            )}

            {loading && <p>Analyzing... This may take a few moments.</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {analyses && (
                <div style={{ display: 'grid', gap: '1rem', marginTop: '1rem' }}>
                    {analyses.map(({ experience, analysis }) => (
                        <div key={experience.id} style={{ border: '1px solid #ddd', padding: '1rem', borderRadius: '8px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <h3>{experience.title} at {experience.organization}</h3>
                                <div style={{
                                    background: analysis.experience_rating >= 8 ? '#d4edda' : analysis.experience_rating >= 5 ? '#fff3cd' : '#f8d7da',
                                    padding: '0.5rem', borderRadius: '4px', fontWeight: 'bold'
                                }}>
                                    Rating: {analysis.experience_rating}/10
                                </div>
                            </div>
                            <p><strong>Original:</strong> {experience.description}</p>
                            <div style={{ background: '#f9f9f9', padding: '1rem', marginTop: '1rem' }}>
                                <p><strong>Story:</strong> {analysis.story}</p>
                                <p><strong>Rationale:</strong> <i>{analysis.rationale}</i></p>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
