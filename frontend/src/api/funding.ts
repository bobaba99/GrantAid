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

export interface StoryTellingResponse {
    experience_id: string;
    experience_rating: number;
    story: string;
    rationale: string;
}

export interface Experience {
    id: string;
    type: string;
    title: string;
    organization: string;
    start_date: string;
    end_date?: string;
    description: string;
    key_skills: string[];
}

export interface ExperienceAnalysis {
    experience: Experience;
    analysis: StoryTellingResponse;
}

export const analyzeExperiences = async (fundingId: string): Promise<ExperienceAnalysis[]> => {
    const response = await apiClient.post(`/api/funding/fundings/${fundingId}/analyze-experiences`);
    return response.data;
};
