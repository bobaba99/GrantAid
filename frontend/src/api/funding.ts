import { apiClient } from './client';

export interface FundingDefinition {
    id: string;
    name: string;
    agency: string;
    cycle_year: string;
    deadline: string;
    website_url: string;
    description?: string;
}

export const getFundings = async (): Promise<FundingDefinition[]> => {
    const response = await apiClient.get('/api/funding/fundings');
    return response.data;
};

export const getFundingById = async (id: string): Promise<FundingDefinition> => {
    const response = await apiClient.get(`/api/funding/fundings/${id}`);
    return response.data;
};
