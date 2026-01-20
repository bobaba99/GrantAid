import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getUserProfile, type UserProfile } from '../api/profile';
import { getExperiences, createExperience, deleteExperience, type Experience } from '../api/experiences';

export function Profile() {
    const [profile, setProfile] = useState<UserProfile | null>(null);
    const [experiences, setExperiences] = useState<Experience[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Form state
    const [formData, setFormData] = useState<Omit<Experience, 'id' | 'key_skills' | 'user_id'>>({
        type: 'Professional',
        title: '',
        organization: '',
        start_date: '',
        end_date: '',
        description: '',
    });

    const fetchData = async () => {
        try {
            setLoading(true);
            const [u, e] = await Promise.all([getUserProfile(), getExperiences()]);
            setProfile(u);
            setExperiences(e);
        } catch (err: any) {
            if (String(err).includes('401')) {
                setError('Unauthorized. Please login.');
            } else {
                setError(String(err));
            }
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await createExperience({
                ...formData,
                key_skills: [], // Basic implementation for now
                end_date: formData.end_date || null,
            });
            // Reset form and reload
            setFormData({
                type: 'Professional',
                title: '',
                organization: '',
                start_date: '',
                end_date: '',
                description: '',
            });
            await fetchData();
        } catch (err) {
            setError('Failed to create experience: ' + String(err));
        }
    };

    const handleDelete = async (id: string) => {
        if (!window.confirm("Are you sure?")) return;
        try {
            await deleteExperience(id);
            await fetchData();
        } catch (err) {
            setError('Failed to delete: ' + String(err));
        }
    }

    if (loading) return <div>Loading profile...</div>;
    if (error) return (
        <div style={{ color: 'red', padding: '2rem' }}>
            <h2>Error</h2>
            <p>{error}</p>
            <Link to="/">Back to Login</Link>
        </div>
    );

    return (
        <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
            <h1>My Profile</h1>
            {profile && (
                <div style={{ borderBottom: '1px solid #ccc', paddingBottom: '1rem', marginBottom: '2rem' }}>
                    <p><strong>Email:</strong> {profile.email}</p>
                    <p><strong>User ID:</strong> {profile.id}</p>
                </div>
            )}

            <div style={{ marginBottom: '2rem' }}>
                <h2>My Experiences</h2>
                {experiences.length === 0 ? <p>No experiences added yet.</p> : (
                    <div style={{ display: 'grid', gap: '1rem' }}>
                        {experiences.map(exp => (
                            <div key={exp.id} style={{ border: '1px solid #eee', padding: '1rem', borderRadius: '4px' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                    <h3>{exp.title} at {exp.organization}</h3>
                                    <button onClick={() => handleDelete(exp.id)} style={{ background: 'red', color: 'white' }}>Delete</button>
                                </div>
                                <p><strong>Type:</strong> {exp.type}</p>
                                <p>{exp.start_date} - {exp.end_date || 'Present'}</p>
                                <p>{exp.description}</p>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <div style={{ borderTop: '1px solid #ccc', paddingTop: '1rem' }}>
                <h2>Add New Experience</h2>
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '500px' }}>
                    <select
                        value={formData.type}
                        onChange={e => setFormData({ ...formData, type: e.target.value as any })}
                        style={{ padding: '0.5rem' }}
                    >
                        <option value="Professional">Professional</option>
                        <option value="Academic">Academic</option>
                        <option value="Volunteer">Volunteer</option>
                        <option value="Research">Research</option>
                    </select>

                    <input
                        type="text"
                        placeholder="Title / Role"
                        required
                        value={formData.title}
                        onChange={e => setFormData({ ...formData, title: e.target.value })}
                        style={{ padding: '0.5rem' }}
                    />

                    <input
                        type="text"
                        placeholder="Organization"
                        required
                        value={formData.organization}
                        onChange={e => setFormData({ ...formData, organization: e.target.value })}
                        style={{ padding: '0.5rem' }}
                    />

                    <div style={{ display: 'flex', gap: '1rem' }}>
                        <input
                            type="date"
                            required
                            placeholder="Start Date"
                            value={formData.start_date}
                            onChange={e => setFormData({ ...formData, start_date: e.target.value })}
                            style={{ padding: '0.5rem', flex: 1 }}
                        />
                        <input
                            type="date"
                            placeholder="End Date (Optional)"
                            value={formData.end_date || ''}
                            onChange={e => setFormData({ ...formData, end_date: e.target.value })}
                            style={{ padding: '0.5rem', flex: 1 }}
                        />
                    </div>

                    <textarea
                        placeholder="Description..."
                        required
                        rows={5}
                        value={formData.description}
                        onChange={e => setFormData({ ...formData, description: e.target.value })}
                        style={{ padding: '0.5rem' }}
                    />

                    <button type="submit" style={{ padding: '0.75rem', background: '#0070f3', color: 'white', border: 'none', cursor: 'pointer' }}>
                        Add Experience
                    </button>
                </form>
            </div>

            <div style={{ marginTop: '2rem' }}>
                <Link to="/">Back to Home</Link>
            </div>
        </div>
    );
}
