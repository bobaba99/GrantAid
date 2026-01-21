import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getUserProfile, type UserProfile } from '../api/profile';
import { getExperiences, createExperience, deleteExperience, updateExperience, type Experience } from '../api/experiences';

import '../styles/Profile.css';

export function Profile() {
    const [profile, setProfile] = useState<UserProfile | null>(null);
    const [experiences, setExperiences] = useState<Experience[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [editingId, setEditingId] = useState<string | null>(null);

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

    const resetForm = () => {
        setFormData({
            type: 'Professional',
            title: '',
            organization: '',
            start_date: '',
            end_date: '',
            description: '',
        });
        setEditingId(null);
    };

    const handleEdit = (exp: Experience) => {
        setEditingId(exp.id);
        setFormData({
            type: exp.type,
            title: exp.title,
            organization: exp.organization,
            start_date: exp.start_date,
            end_date: exp.end_date || '',
            description: exp.description,
        });
        // Scroll to form
        document.querySelector('.experience-form')?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const dataToSubmit = {
                ...formData,
                key_skills: [], // Basic implementation for now
                end_date: formData.end_date || null,
            };

            if (editingId) {
                await updateExperience(editingId, dataToSubmit);
            } else {
                await createExperience(dataToSubmit);
            }

            resetForm();
            await fetchData();
        } catch (err) {
            setError(`Failed to ${editingId ? 'update' : 'create'} experience: ` + String(err));
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
        <div className="profile-container">
            <header className="profile-header">
                <h1>My Profile</h1>
                {profile && (
                    <div className="profile-info">
                        <p><strong>Email:</strong> {profile.email}</p>
                        <p><strong>Full Name:</strong> {profile.full_name}</p>
                        <p><strong>Program Level:</strong> {profile.program_level}</p>
                        <p><strong>Research Field:</strong> {profile.research_field}</p>
                        <p><strong>Research Focus:</strong> {profile.research_focus}</p>
                        <p><strong>Institution:</strong> {profile.institution}</p>
                    </div>
                )}
            </header>

            <section className="experiences-section">
                <h2 className="section-title">My Experiences</h2>
                {experiences.length === 0 ? <p>No experiences added yet.</p> : (
                    <div className="experiences-list">
                        {experiences.map(exp => (
                            <div key={exp.id} className="experience-card">
                                <div className="experience-header">
                                    <h3>{exp.title} at {exp.organization}</h3>
                                    <div className="action-buttons">
                                        <button onClick={() => handleEdit(exp)} className="edit-btn">Edit</button>
                                        <button onClick={() => handleDelete(exp.id)} className="delete-btn">Delete</button>
                                    </div>
                                </div>
                                <p className="experience-meta"><strong>Type:</strong> {exp.type}</p>
                                <p className="experience-meta">{exp.start_date} - {exp.end_date || 'Present'}</p>
                                <p className="experience-desc">{exp.description}</p>
                            </div>
                        ))}
                    </div>
                )}
            </section>

            <section className="add-experience-section">
                <h2 className="section-title">{editingId ? 'Edit Experience' : 'Add New Experience'}</h2>
                <form onSubmit={handleSubmit} className="experience-form">
                    <select
                        value={formData.type}
                        onChange={e => setFormData({ ...formData, type: e.target.value as any })}
                        className="form-select"
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
                        className="form-input"
                    />

                    <input
                        type="text"
                        placeholder="Organization"
                        required
                        value={formData.organization}
                        onChange={e => setFormData({ ...formData, organization: e.target.value })}
                        className="form-input"
                    />

                    <div className="form-group-row">
                        <input
                            type="date"
                            required
                            placeholder="Start Date"
                            value={formData.start_date}
                            onChange={e => setFormData({ ...formData, start_date: e.target.value })}
                            className="form-input"
                            style={{ flex: 1 }}
                        />
                        <input
                            type="date"
                            placeholder="End Date (Optional)"
                            value={formData.end_date || ''}
                            onChange={e => setFormData({ ...formData, end_date: e.target.value })}
                            className="form-input"
                            style={{ flex: 1 }}
                        />
                    </div>

                    <textarea
                        placeholder="Description"
                        required
                        rows={5}
                        value={formData.description}
                        onChange={e => setFormData({ ...formData, description: e.target.value })}
                        className="form-textarea"
                    />

                    <div style={{ display: 'flex', justifyContent: 'center' }}>
                        <button type="submit" className="submit-btn">
                            {editingId ? 'Update Experience' : 'Add Experience'}
                        </button>
                        {editingId && (
                            <button type="button" onClick={resetForm} className="cancel-btn">
                                Cancel
                            </button>
                        )}
                    </div>
                </form>
            </section>
        </div>
    );
}
