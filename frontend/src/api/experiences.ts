import { apiClient } from './client';

export interface Experience {
    id: string;
    type: 'Professional' | 'Academic' | 'Volunteer' | 'Research';
    title: string;
    organization: string;
    start_date: string;
    end_date?: string | null;
    description: string;
    key_skills: string[];
    user_id?: string;
}

export const getExperiences = async (): Promise<Experience[]> => {
    const response = await apiClient.get('/api/experiences');
    return response.data;
};

export const createExperience = async (experience: Omit<Experience, 'id'>): Promise<Experience> => {
    const response = await apiClient.post('/api/experiences', experience);
    return response.data;
};

export const deleteExperience = async (id: string): Promise<void> => {
    await apiClient.delete(`/api/experiences/${id}`);
};

export const updateExperience = async (id: string, experience: Partial<Experience>): Promise<Experience> => {
    const response = await apiClient.put(`/api/experiences/${id}`, experience);
    return response.data;
};
