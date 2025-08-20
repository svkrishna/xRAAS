import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ReasoningRequest {
  question: string;
  context?: string;
  domain?: string;
  confidence_threshold?: number;
  max_steps?: number;
}

export interface ReasoningTrace {
  stage: string;
  output: string;
  confidence?: number;
  metadata?: any;
}

export interface ReasoningResponse {
  answer: string;
  reasoning_trace: ReasoningTrace[];
  confidence: number;
  domain?: string;
  metadata?: any;
}

export interface HealthResponse {
  success: boolean;
  message: string;
  data: any;
}

export const reasoningService = {
  async reason(request: ReasoningRequest): Promise<ReasoningResponse> {
    try {
      const response = await api.post('/api/v1/reason/', request);
      return response.data;
    } catch (error: any) {
      if (error.response) {
        throw new Error(error.response.data.detail || 'API request failed');
      }
      throw new Error('Network error');
    }
  },

  async getHealth(): Promise<HealthResponse> {
    try {
      const response = await api.get('/health/');
      return response.data;
    } catch (error: any) {
      throw new Error('Health check failed');
    }
  },

  async getDetailedHealth(): Promise<HealthResponse> {
    try {
      const response = await api.get('/health/detailed');
      return response.data;
    } catch (error: any) {
      throw new Error('Detailed health check failed');
    }
  },

  async getRules(domain?: string): Promise<any> {
    try {
      const params = domain ? { domain } : {};
      const response = await api.get('/api/v1/reason/rules', { params });
      return response.data;
    } catch (error: any) {
      throw new Error('Failed to fetch rules');
    }
  },

  async getKnowledgeSummary(domain?: string): Promise<any> {
    try {
      const params = domain ? { domain } : {};
      const response = await api.get('/api/v1/reason/knowledge', { params });
      return response.data;
    } catch (error: any) {
      throw new Error('Failed to fetch knowledge summary');
    }
  },

  async getCapabilities(domain?: string): Promise<any> {
    try {
      const params = domain ? { domain } : {};
      const response = await api.get('/api/v1/reason/capabilities', { params });
      return response.data;
    } catch (error: any) {
      throw new Error('Failed to fetch capabilities');
    }
  },

  async validateRequest(request: ReasoningRequest): Promise<any> {
    try {
      const response = await api.post('/api/v1/reason/validate', request);
      return response.data;
    } catch (error: any) {
      throw new Error('Request validation failed');
    }
  },
};
