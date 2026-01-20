import { apiClient } from './client';

export interface UserProfile {
    id: string;
    email: string;
}

export const getUserProfile = async (): Promise<UserProfile> => {
    const response = await apiClient.get('/me');
    return response.data;
};
