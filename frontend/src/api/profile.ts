import { apiClient } from './client';

export interface UserProfile {
    id: string;
    email: string;
    full_name: string;
    program_level: string;
    research_field: string;
    research_focus: string;
    institution: string;
}

export const getUserProfile = async (): Promise<UserProfile> => {
    const response = await apiClient.get('/me');
    return response.data;
};

export const updateUserProfile = async (profile: Partial<UserProfile>): Promise<void> => {
    await apiClient.put('/me', profile);
};
