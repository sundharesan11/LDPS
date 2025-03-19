import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const predictLoanDefault = async (applicationData) => {
  try {
    const response = await apiClient.post('/predict', applicationData);
    return response.data;
  } catch (error) {
    console.error('Error predicting loan default:', error);
    throw error;
  }
};

export const generateSyntheticData = async (count = 1, defaultRatio = 0.3) => {
  try {
    const response = await apiClient.post('/generate-synthetic', {
      count,
      default_ratio: defaultRatio
    });
    return response.data;
  } catch (error) {
    console.error('Error generating synthetic data:', error);
    throw error;
  }
};

export const predictWithSynthetic = async (count = 1, defaultRatio = 0.3) => {
  try {
    const response = await apiClient.post('/predict-synthetic', {
      count,
      default_ratio: defaultRatio
    });
    return response.data;
  } catch (error) {
    console.error('Error predicting with synthetic data:', error);
    throw error;
  }
};