/**
 * API service for backend communication
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export const api = {
    // Upload media file
    uploadFile: async (file, onProgress) => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
            onUploadProgress: (progressEvent) => {
                const percentCompleted = Math.round(
                    (progressEvent.loaded * 100) / progressEvent.total
                );
                if (onProgress) onProgress(percentCompleted);
            },
        });

        return response.data;
    },

    // Get media info and analysis
    getMedia: async (mediaId) => {
        const response = await axios.get(`${API_BASE_URL}/media/${mediaId}`);
        return response.data;
    },

    // Get all analyses for a media
    getAllAnalyses: async (mediaId) => {
        const response = await axios.get(`${API_BASE_URL}/media/${mediaId}/analysis`);
        return response.data;
    },

    // Ask a question
    askQuestion: async (mediaId, question) => {
        const response = await axios.post(`${API_BASE_URL}/ask`, {
            media_id: mediaId,
            question,
        });
        return response.data;
    },

    // Get chat history
    getChatHistory: async (mediaId) => {
        const response = await axios.get(`${API_BASE_URL}/chat/${mediaId}`);
        return response.data;
    },

    // List all media
    listMedia: async (limit = 20, offset = 0) => {
        const response = await axios.get(`${API_BASE_URL}/media`, {
            params: { limit, offset },
        });
        return response.data;
    },

    // Get download URL
    getDownloadUrl: (mediaId) => {
        return `${API_BASE_URL}/download/${mediaId}`;
    },
};
