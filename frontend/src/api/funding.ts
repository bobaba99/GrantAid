import { apiClient } from './client';
import type { Experience } from './experiences';

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

export interface ExperienceAnalysis {
    experience: Experience;
    analysis: StoryTellingResponse;
}

export const analyzeExperiences = async (fundingId: string, forceRefresh = false): Promise<ExperienceAnalysis[]> => {
    const url = `/api/funding/fundings/${fundingId}/analyze-experiences${forceRefresh ? '?force_refresh=true' : ''}`;
    const response = await apiClient.post(url);
    return response.data;
};

export const getExperienceAnalyses = async (fundingId: string): Promise<ExperienceAnalysis[]> => {
    const response = await apiClient.get(`/api/funding/fundings/${fundingId}/analyses`);
    return response.data;
};
