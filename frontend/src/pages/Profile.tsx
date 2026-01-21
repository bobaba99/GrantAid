import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getUserProfile, updateUserProfile, type UserProfile } from '../api/profile';
import { getExperiences, createExperience, deleteExperience, updateExperience, type Experience } from '../api/experiences';

import '../styles/Profile.css';

export function Profile() {
    const [profile, setProfile] = useState<UserProfile | null>(null);
    const [experiences, setExperiences] = useState<Experience[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Experience editing state
    const [editingId, setEditingId] = useState<string | null>(null);
    const [showExperienceModal, setShowExperienceModal] = useState(false);

    // Profile editing state
    const [isEditingProfile, setIsEditingProfile] = useState(false);
    const [profileFormData, setProfileFormData] = useState<UserProfile>({
        id: '',
        email: '',
        full_name: '',
        program_level: '',
        research_field: '',
        research_focus: '',
        institution: '',
    });

    // Experience form state
    const [isCurrentRole, setIsCurrentRole] = useState(false);
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

    // Profile Edit Handlers
    const handleEditProfile = () => {
        if (profile) {
            setProfileFormData(profile);
            setIsEditingProfile(true);
        }
    };

    const handleProfileUpdate = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await updateUserProfile(profileFormData);
            setIsEditingProfile(false);
            await fetchData();
        } catch (err) {
            setError('Failed to update profile: ' + String(err));
        }
    };

    const cancelProfileEdit = () => {
        setIsEditingProfile(false);
    };

    // Experience Handlers
    const resetForm = () => {
        setFormData({
            type: 'Professional',
            title: '',
            organization: '',
            start_date: '',
            end_date: '',
            description: '',
        });
        setIsCurrentRole(false);
        setEditingId(null);
        setShowExperienceModal(false);
    };

    const handleEdit = (exp: Experience) => {
        setEditingId(exp.id);
        const current = !exp.end_date;
        setIsCurrentRole(current);
        setFormData({
            type: exp.type,
            title: exp.title,
            organization: exp.organization,
            start_date: exp.start_date,
            end_date: exp.end_date || '',
            description: exp.description,
        });
        setShowExperienceModal(true);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const dataToSubmit = {
                ...formData,
                key_skills: [], // Basic implementation for now
                end_date: isCurrentRole ? null : (formData.end_date || null),
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

    // Helper for badge styles
    const getBadgeStyle = (type: string) => {
        const t = type.toLowerCase();
        if (t === 'academic') return { bg: 'var(--badge-academic-bg)', text: 'var(--badge-academic-text)', dot: 'var(--badge-academic-dot)', gradient: 'from-blue-500 to-blue-300' }; // simplified naming for logic, but using vars in CSS
        if (t === 'professional') return { bg: 'var(--badge-professional-bg)', text: 'var(--badge-professional-text)', dot: 'var(--badge-professional-dot)', gradient: 'from-emerald-600 to-emerald-400' };
        if (t === 'volunteer') return { bg: 'var(--badge-volunteer-bg)', text: 'var(--badge-volunteer-text)', dot: 'var(--badge-volunteer-dot)', gradient: 'from-orange-500 to-orange-300' };
        return { bg: 'var(--badge-research-bg)', text: 'var(--badge-research-text)', dot: 'var(--badge-research-dot)', gradient: 'from-violet-600 to-violet-400' };
    };

    // Helper for gradient (using inline style for dynamic color since we don't have Tailwind classes)
    const getGradientStyle = (type: string) => {
        const t = type.toLowerCase();
        if (t === 'academic') return 'linear-gradient(to right, #3b82f6, #93c5fd)';
        if (t === 'professional') return 'linear-gradient(to right, #059669, #34d399)';
        if (t === 'volunteer') return 'linear-gradient(to right, #f97316, #fdba74)';
        return 'linear-gradient(to right, #7c3aed, #a78bfa)';
    };

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
            <div className="profile-header-grid">
                <div style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', padding: '1rem' }}>
                    <h1 className="page-title">Experiences Library</h1>
                    <p className="page-subtitle" style={{ margin: '0 auto' }}>
                        Keep your professional history up to date. This master list is used by our AI to evaluate your eligibility for specific grants.
                    </p>
                </div>
            </div>

            {/* User Profile Section */}
            <div className="info-group" style={{ flexBasis: '100%', display: 'flex', justifyContent: 'flex-end', paddingBottom: '1rem' }}>
                <button onClick={handleEditProfile} className="icon-btn" style={{ padding: 0, gap: '2rem 0.5rem', width: 'auto' }}>
                    <span style={{ textDecoration: 'underline' }}>Edit Profile Details</span>
                </button>
            </div>

            <div className="user-info-card" style={{ padding: '1.5rem 1.5rem' }}>
                <div className="info-group">
                    <span className="info-label" >Full Name</span>
                    <div className="info-value">{profile?.full_name || 'Not set'}</div>
                </div>
                <div className="info-group">
                    <span className="info-label">Email</span>
                    <div className="info-value">{profile?.email}</div>
                </div>
                <div className="info-group">
                    <span className="info-label">Institution</span>
                    <div className="info-value">{profile?.institution || 'Not set'}</div>
                </div>
                <div className="info-group">
                    <span className="info-label">Program Level</span>
                    <div className="info-value">{profile?.program_level || 'Not set'}</div>
                </div>
            </div>

            {/* Experiences Grid */}
            <div className="experiences-grid">
                {experiences.map(exp => {
                    const badgeStyle = getBadgeStyle(exp.type);
                    return (
                        <article key={exp.id} className="experience-card-new group">
                            {/* Hover Decoration */}
                            <div className="card-decoration" style={{ background: getGradientStyle(exp.type) }}></div>

                            <div className="experience-header-new">
                                <div>
                                    <span className="badge" style={{ backgroundColor: badgeStyle.bg, color: badgeStyle.text }}>
                                        <span className="badge-dot" style={{ backgroundColor: badgeStyle.dot }}></span>
                                        {exp.type}
                                    </span>
                                    <h3 style={{ textAlign: 'left', fontSize: '18px' }} className="exp-title">{exp.title}</h3>
                                    <p style={{ textAlign: 'left', fontSize: '16px' }} className="exp-org">{exp.organization}</p>
                                </div>
                                <div className="exp-date-badge" style={{ fontSize: '16px' }}>
                                    {exp.start_date} - {exp.end_date ? exp.end_date.split('-')[0] : 'Present'}
                                </div>
                            </div>

                            <p style={{ textAlign: 'left', fontSize: '16px' }} className="exp-description">{exp.description}</p>

                            <div className="card-footer-new">
                                <button onClick={() => handleEdit(exp)} className="icon-btn" title="Edit">
                                    <span className="material-symbols-outlined">Edit</span>
                                </button>
                                <button onClick={() => handleDelete(exp.id)} className="icon-btn delete" title="Delete">
                                    <span className="material-symbols-outlined">Delete</span>
                                </button>
                            </div>
                        </article>
                    );
                })}

                {/* Visual "Add" Card that acts as shortcut to form */}
                <button
                    onClick={() => {
                        resetForm();
                        setEditingId(null);
                        setShowExperienceModal(true);
                    }}
                    className="group"
                    style={{
                        borderRadius: '1rem',
                        border: '2px dashed var(--profile-border)',
                        background: 'transparent',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        minHeight: '250px',
                        cursor: 'pointer',
                        transition: 'all 0.2s',
                        color: 'var(--profile-text-sub)'
                    }}
                >
                    <div style={{
                        width: '3.5rem', height: '3.5rem', borderRadius: '9999px',
                        background: '#f1f5f9', display: 'flex', alignItems: 'center', justifyContent: 'center',
                        marginBottom: '1rem', transition: 'background-color 0.2s'
                    }}>
                        <span className="material-symbols-outlined" style={{ fontSize: '28px', fontWeight: '700', verticalAlign: 'middle' }}>add</span>
                    </div>
                    <h3 style={{ fontSize: '1.125rem', fontWeight: '700', margin: 0 }}>Add Experience</h3>
                </button>
            </div>

            {/* Modal for Add/Edit Experience */}
            {showExperienceModal && (
                <div className="modal-overlay" onClick={() => resetForm()}>
                    <div className="modal-content" onClick={e => e.stopPropagation()}>
                        <h2 className="section-title" style={{ marginTop: 0, marginBottom: '1.5rem', textAlign: 'left' }}>{editingId ? 'Edit Experience' : 'Add New Experience'}</h2>
                        <form onSubmit={handleSubmit} className="modern-form">
                            <div className="form-group-row">
                                <div className="input-group-modern" style={{ flex: 1 }}>
                                    <label className="label-modern">Type</label>
                                    <select
                                        value={formData.type}
                                        onChange={e => setFormData({ ...formData, type: e.target.value as any })}
                                        className="select-modern"
                                    >
                                        <option value="Professional">Professional</option>
                                        <option value="Academic">Academic</option>
                                        <option value="Volunteer">Volunteer</option>
                                        <option value="Research">Research</option>
                                    </select>
                                </div>
                                <div className="input-group-modern" style={{ flex: 1 }}>
                                    <label className="label-modern">Organization</label>
                                    <input
                                        type="text"
                                        required
                                        value={formData.organization}
                                        onChange={e => setFormData({ ...formData, organization: e.target.value })}
                                        className="input-modern"
                                    />
                                </div>
                            </div>

                            <div className="input-group-modern">
                                <label className="label-modern">Title / Role</label>
                                <input
                                    type="text"
                                    required
                                    value={formData.title}
                                    onChange={e => setFormData({ ...formData, title: e.target.value })}
                                    className="input-modern"
                                />
                            </div>

                            <div className="form-group-row">
                                <div className="input-group-modern" style={{ flex: 1 }}>
                                    <label className="label-modern">Start Date</label>
                                    <input
                                        type="date"
                                        required
                                        value={formData.start_date}
                                        onChange={e => setFormData({ ...formData, start_date: e.target.value })}
                                        className="input-modern"
                                    />
                                </div>
                                <div className="input-group-modern" style={{ flex: 1 }}>
                                    <label className="label-modern">End Date</label>
                                    <input
                                        type="date"
                                        value={formData.end_date || ''}
                                        onChange={e => setFormData({ ...formData, end_date: e.target.value })}
                                        className="input-modern"
                                        disabled={isCurrentRole}
                                        style={{ opacity: isCurrentRole ? 0.5 : 1 }}
                                    />
                                    <label style={{ fontSize: '0.9rem', marginTop: '0.5rem', display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                                        <input
                                            type="checkbox"
                                            checked={isCurrentRole}
                                            onChange={e => {
                                                setIsCurrentRole(e.target.checked);
                                                if (e.target.checked) {
                                                    setFormData({ ...formData, end_date: '' });
                                                }
                                            }}
                                            style={{ marginRight: '0.5rem' }}
                                        />
                                        Currently working here
                                    </label>
                                </div>
                            </div>

                            <div className="input-group-modern">
                                <label className="label-modern">Description</label>
                                <textarea
                                    required
                                    rows={5}
                                    value={formData.description}
                                    onChange={e => setFormData({ ...formData, description: e.target.value })}
                                    className="textarea-modern"
                                />
                            </div>

                            <div className="form-actions">
                                <button type="button" onClick={resetForm} className="cancel-btn-modern">
                                    Cancel
                                </button>
                                <button type="submit" className="submit-btn-modern">
                                    {editingId ? 'Update Experience' : 'Add Experience'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Modal for Edit Profile */}
            {isEditingProfile && (
                <div className="modal-overlay" onClick={cancelProfileEdit}>
                    <div className="modal-content" onClick={e => e.stopPropagation()}>
                        <h2 className="section-title" style={{ marginTop: 0, marginBottom: '1.5rem', textAlign: 'left' }}>Edit Profile Details</h2>
                        <form onSubmit={handleProfileUpdate} className="modern-form">
                            <div className="form-group-row">
                                <div className="input-group-modern" style={{ flex: 1 }}>
                                    <label className="label-modern">Full Name</label>
                                    <input
                                        type="text"
                                        value={profileFormData.full_name || ''}
                                        onChange={e => setProfileFormData({ ...profileFormData, full_name: e.target.value })}
                                        className="input-modern"
                                    />
                                </div>
                                <div className="input-group-modern" style={{ flex: 1 }}>
                                    <label className="label-modern">Program Level</label>
                                    <input
                                        type="text"
                                        value={profileFormData.program_level || ''}
                                        onChange={e => setProfileFormData({ ...profileFormData, program_level: e.target.value })}
                                        className="input-modern"
                                    />
                                </div>
                            </div>

                            <div className="form-group-row">
                                <div className="input-group-modern" style={{ flex: 1 }}>
                                    <label className="label-modern">Research Field</label>
                                    <input
                                        type="text"
                                        value={profileFormData.research_field || ''}
                                        onChange={e => setProfileFormData({ ...profileFormData, research_field: e.target.value })}
                                        className="input-modern"
                                    />
                                </div>
                                <div className="input-group-modern" style={{ flex: 1 }}>
                                    <label className="label-modern">Research Focus</label>
                                    <input
                                        type="text"
                                        value={profileFormData.research_focus || ''}
                                        onChange={e => setProfileFormData({ ...profileFormData, research_focus: e.target.value })}
                                        className="input-modern"
                                    />
                                </div>
                            </div>

                            <div className="input-group-modern">
                                <label className="label-modern">Institution</label>
                                <input
                                    type="text"
                                    value={profileFormData.institution || ''}
                                    onChange={e => setProfileFormData({ ...profileFormData, institution: e.target.value })}
                                    className="input-modern"
                                />
                            </div>

                            <div className="form-actions">
                                <button type="button" onClick={cancelProfileEdit} className="cancel-btn-modern">Cancel</button>
                                <button type="submit" className="submit-btn-modern">Save Changes</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
