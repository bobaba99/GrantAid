import { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { useParams, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { getFundingById, type FundingDefinition } from '../api/funding';
import '../styles/FundingDetail.css';

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
        <div className="funding-detail-container">
            <div className="detail-header">
                <h1 className="detail-title">{funding.name}</h1>
                <h2 className="detail-agency">AGENCY: {funding.agency}</h2>
                <div className="detail-meta-grid">
                    <div className="meta-item">
                        <span className="material-symbols-outlined" style={{ fontSize: '20px' }}>calendar_month</span>
                        Cycle: {funding.cycle_year}
                    </div>
                    <div className="meta-item">
                        <span className="material-symbols-outlined" style={{ fontSize: '20px' }}>schedule</span>
                        Deadline: {funding.deadline}
                    </div>
                </div>
                <div className="detail-actions">
                    <a href={funding.website_url} target="_blank" rel="noreferrer" className="external-link">
                        Official Website
                        <span className="material-symbols-outlined" style={{ fontSize: '18px', marginLeft: '4px' }}>open_in_new</span>
                    </a>
                    {funding.agency.includes('FRQS') && (
                        <a href="https://www.notion.so/FRQS-2eedc7826a688038a30acfc9b8f2f132?source=copy_link" target="_blank" rel="noreferrer" className="external-link">
                            Notion FRQ Page
                            <span className="material-symbols-outlined" style={{ fontSize: '18px', marginLeft: '4px' }}>open_in_new</span>
                        </a>
                    )}
                    {funding.agency.includes('CIHR') && (
                        <a href="https://www.notion.so/CIHR-2eddc7826a68808685fcfd8310e0b32e?source=copy_link" target="_blank" rel="noreferrer" className="external-link">
                            Notion CIHR Page
                            <span className="material-symbols-outlined" style={{ fontSize: '18px', marginLeft: '4px' }}>open_in_new</span>
                        </a>
                    )}
                </div>
            </div>

            <div className="split-view-container">
                <div className="criteria-section">
                    <h3 className="section-title">Criteria</h3>
                    <div className="criteria-content markdown-content">
                        <ReactMarkdown>{funding.description || 'No description available.'}</ReactMarkdown>
                    </div>
                </div>

                <div className="analysis-section">
                    <ExperiencesAnalysisSection fundingId={id!} />
                </div>
            </div>

            {createPortal(
                <Link to="/fundings" className="floating-back-btn" aria-label="Back to List">
                    <span className="material-symbols-outlined">arrow_back</span>
                </Link>,
                document.body
            )}
        </div>
    );
}

import { analyzeExperiences, getExperienceAnalyses, type ExperienceAnalysis } from '../api/funding';

function ExperiencesAnalysisSection({ fundingId }: { fundingId: string }) {
    const [analyses, setAnalyses] = useState<ExperienceAnalysis[] | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (fundingId) {
            getExperienceAnalyses(fundingId)
                .then(data => {
                    if (data && data.length > 0) {
                        setAnalyses(data);
                    }
                })
                .catch(err => console.error("Failed to load existing analyses", err));
        }
    }, [fundingId]);

    const handleAnalyze = async () => {
        setLoading(true);
        setError('');
        try {
            // If we already have analyses, this is a regeneration
            const forceRefresh = !!analyses;
            const data = await analyzeExperiences(fundingId, forceRefresh);
            setAnalyses(data);
        } catch (err) {
            setError('Failed to analyze experiences: ' + String(err));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2 className="section-title">My Relevant Experiences</h2>
            <p style={{ color: 'var(--funding-text-sub)', marginBottom: '1.5rem' }}>See how your experiences align with this funding opportunity.</p>

            {!loading && (
                <button onClick={handleAnalyze} className="primary-btn">
                    {analyses ? 'Regenerate Analysis' : 'Analyze My Experiences'}
                </button>
            )}

            {loading && (
                <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--funding-text-sub)' }}>
                    <span className="material-symbols-outlined" style={{ fontSize: '48px', animation: 'spin 1s linear infinite' }}>sync</span>
                    <p>Analyzing... This may take a few moments.</p>
                </div>
            )}

            {error && <p style={{ color: '#ef4444', marginBottom: '1rem' }}>{error}</p>}

            {analyses && (
                <div style={{ display: 'grid', gap: '1.5rem', marginTop: '1rem' }}>
                    {analyses.map(({ experience, analysis }) => (
                        <div key={experience.id} className="analysis-card">
                            <div className="analysis-header">
                                <h3 style={{ margin: 0, fontSize: '1.1rem', color: 'var(--funding-text-main)' }}>{experience.title} at {experience.organization}</h3>
                            </div>

                            {/* Facet Scores Visualization */}
                            <div style={{
                                display: 'grid',
                                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                                gap: '0.75rem',
                                margin: '1rem 0',
                                padding: '1rem',
                                background: 'var(--funding-bg-secondary, #f9fafb)',
                                borderRadius: '8px'
                            }}>
                                {[
                                    { label: 'Facet A: Competency', score: analysis.experience_rating_facet_a, color: '#3b82f6' },
                                    { label: 'Facet B: Fit', score: analysis.experience_rating_facet_b, color: '#8b5cf6' },
                                    { label: 'Facet C: Impact', score: analysis.experience_rating_facet_c, color: '#ec4899' },
                                    { label: 'Facet D: Narrative', score: analysis.experience_rating_facet_d, color: '#10b981' }
                                ].map(({ label, score, color }) => (
                                    <div key={label} style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                                        <div style={{
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            alignItems: 'center',
                                            fontSize: '0.85rem',
                                            fontWeight: '500'
                                        }}>
                                            <span style={{ color: 'var(--funding-text-main)' }}>{label}</span>
                                            <span style={{
                                                color: color,
                                                fontWeight: '700',
                                                fontSize: '0.95rem'
                                            }}>{score}/5</span>
                                        </div>
                                        <div style={{
                                            height: '8px',
                                            background: 'var(--funding-bg-main, #e5e7eb)',
                                            borderRadius: '4px',
                                            overflow: 'hidden'
                                        }}>
                                            <div style={{
                                                height: '100%',
                                                width: `${(score / 5) * 100}%`,
                                                background: color,
                                                borderRadius: '4px',
                                                transition: 'width 0.3s ease'
                                            }} />
                                        </div>
                                    </div>
                                ))}
                            </div>

                            <p style={{ textAlign: 'left', fontSize: '0.95rem', color: 'var(--funding-text-sub)', marginBottom: '1rem' }}><strong>Original:</strong> {experience.description}</p>
                            <div className="analysis-content">
                                <p style={{ textAlign: 'left', lineHeight: '2', marginBottom: '1rem', color: 'var(--funding-text-main)' }}>
                                    <strong style={{ color: 'var(--funding-primary)', lineHeight: '2' }}>Story:</strong><br /> {analysis.story}
                                </p>
                                <p style={{ textAlign: 'left', lineHeight: '2', color: 'var(--funding-text-main)' }}>
                                    <strong style={{ color: 'var(--funding-primary)', lineHeight: '2' }}>Rationale:</strong><br /> <i>{analysis.rationale}</i>
                                </p>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
