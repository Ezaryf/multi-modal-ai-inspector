import React, { useState, useEffect } from 'react';
import UploadDropzone from './components/UploadDropzone';
import MediaPlayer from './components/MediaPlayer';
import AnalyticsPanel from './components/AnalyticsPanel';
import ChatPanel from './components/ChatPanel';
import './App.css';

function App() {
    const [currentMedia, setCurrentMedia] = useState(null);
    const [mediaData, setMediaData] = useState(null);
    const [polling, setPolling] = useState(false);

    // Poll for analysis completion
    useEffect(() => {
        if (!currentMedia || !polling) return;

        const pollInterval = setInterval(async () => {
            try {
                const { api } = await import('./services/api');
                const data = await api.getMedia(currentMedia);

                setMediaData(data);

                // Stop polling when analysis is complete
                if (data.status === 'completed') {
                    setPolling(false);
                }
            } catch (error) {
                console.error('Polling failed:', error);
                setPolling(false);
            }
        }, 3000); // Poll every 3 seconds

        return () => clearInterval(pollInterval);
    }, [currentMedia, polling]);

    const handleUpload = async (uploadResult) => {
        setCurrentMedia(uploadResult.media_id);
        setMediaData(null);
        setPolling(true);

        // Initial fetch
        try {
            const { api } = await import('./services/api');
            const data = await api.getMedia(uploadResult.media_id);
            setMediaData(data);

            if (data.status !== 'completed') {
                setPolling(true);
            }
        } catch (error) {
            console.error('Failed to fetch media:', error);
        }
    };

    return (
        <div className="app">
            <header className="app-header">
                <div className="container">
                    <h1 className="app-title">
                        <span className="gradient-text">Multi-Modal AI Inspector</span>
                    </h1>
                    <p className="app-subtitle">
                        Upload images, audio, or video • Get deep AI insights • Ask questions
                    </p>
                </div>
            </header>

            <main className="app-main">
                <div className="container">
                    <UploadDropzone onUploaded={handleUpload} />

                    {mediaData && (
                        <>
                            <MediaPlayer mediaData={mediaData} />

                            {mediaData.status === 'processing' && (
                                <div className="processing-status">
                                    <div className="spinner"></div>
                                    <p>Analyzing your media... This may take a moment.</p>
                                </div>
                            )}

                            {mediaData.status === 'completed' && mediaData.analysis && (
                                <>
                                    <AnalyticsPanel
                                        analysis={mediaData.analysis}
                                        mediaType={mediaData.media_type}
                                    />

                                    <ChatPanel mediaId={currentMedia} />
                                </>
                            )}
                        </>
                    )}
                </div>
            </main>

            <footer className="app-footer">
                <div className="container">
                    <p>
                        Powered by BLIP, Whisper, and local LLMs •
                        <a href="https://github.com" target="_blank" rel="noopener noreferrer">
                            View on GitHub
                        </a>
                    </p>
                </div>
            </footer>
        </div>
    );
}

export default App;
