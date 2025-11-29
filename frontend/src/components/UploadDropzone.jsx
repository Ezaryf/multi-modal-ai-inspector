import React, { useState, useRef } from 'react';
import './UploadDropzone.css';

export default function UploadDropzone({ onUploaded }) {
    const [isDragging, setIsDragging] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [progress, setProgress] = useState(0);
    const fileInputRef = useRef(null);

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = async (e) => {
        e.preventDefault();
        setIsDragging(false);

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            await uploadFile(files[0]);
        }
    };

    const handleFileSelect = async (e) => {
        const files = e.target.files;
        if (files.length > 0) {
            await uploadFile(files[0]);
        }
    };

    const uploadFile = async (file) => {
        setUploading(true);
        setProgress(0);

        try {
            const { api } = await import('../services/api');

            const result = await api.uploadFile(file, (percent) => {
                setProgress(percent);
            });

            // Notify parent component
            if (onUploaded) {
                onUploaded(result);
            }
        } catch (error) {
            console.error('Upload failed:', error);
            alert('Upload failed: ' + (error.response?.data?.detail || error.message));
        } finally {
            setUploading(false);
            setProgress(0);
        }
    };

    return (
        <div className="upload-dropzone-container">
            <div
                className={`dropzone ${isDragging ? 'dragging' : ''} ${uploading ? 'uploading' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => !uploading && fileInputRef.current?.click()}
            >
                {uploading ? (
                    <div className="upload-status">
                        <div className="spinner"></div>
                        <p className="upload-text">Uploading... {progress}%</p>
                        <div className="progress-bar">
                            <div className="progress-fill" style={{ width: `${progress}%` }}></div>
                        </div>
                    </div>
                ) : (
                    <div className="upload-prompt">
                        <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                        <h3 className="gradient-text">Drop your media here</h3>
                        <p className="upload-description">or click to browse</p>
                        <p className="upload-hint">Support: Images, Audio, Video (max 100MB)</p>
                    </div>
                )}

                <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*,audio/*,video/*"
                    onChange={handleFileSelect}
                    style={{ display: 'none' }}
                />
            </div>
        </div>
    );
}
