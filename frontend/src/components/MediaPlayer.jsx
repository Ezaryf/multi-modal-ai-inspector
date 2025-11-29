import React from 'react';
import './MediaPlayer.css';

export default function MediaPlayer({ mediaData }) {
    if (!mediaData) return null;

    const { media_type, filename } = mediaData;
    const mediaUrl = `/download/${mediaData.id}`;

    return (
        <div className="media-player">
            <h3 className="media-title">{filename}</h3>

            <div className="media-container">
                {media_type === 'image' && (
                    <img
                        src={mediaUrl}
                        alt={filename}
                        className="media-content"
                    />
                )}

                {media_type === 'audio' && (
                    <div className="audio-player">
                        <audio controls className="media-content">
                            <source src={mediaUrl} />
                            Your browser does not support audio playback.
                        </audio>
                    </div>
                )}

                {media_type === 'video' && (
                    <video controls className="media-content">
                        <source src={mediaUrl} />
                        Your browser does not support video playback.
                    </video>
                )}
            </div>

            <div className="media-metadata">
                <div className="metadata-item">
                    <span className="metadata-label">Type:</span>
                    <span className="metadata-value">{media_type}</span>
                </div>

                {mediaData.width && mediaData.height && (
                    <div className="metadata-item">
                        <span className="metadata-label">Dimensions:</span>
                        <span className="metadata-value">{mediaData.width} × {mediaData.height}</span>
                    </div>
                )}

                {mediaData.duration && (
                    <div className="metadata-item">
                        <span className="metadata-label">Duration:</span>
                        <span className="metadata-value">{Math.round(mediaData.duration)}s</span>
                    </div>
                )}

                <div className="metadata-item">
                    <span className="metadata-label">Size:</span>
                    <span className="metadata-value">
                        {(mediaData.size_bytes / 1024 / 1024).toFixed(2)} MB
                    </span>
                </div>
            </div>
        </div>
    );
}
