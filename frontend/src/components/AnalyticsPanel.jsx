import React from 'react';
import './AnalyticsPanel.css';

export default function AnalyticsPanel({ analysis, mediaType }) {
    if (!analysis) {
        return (
            <div className="analytics-panel">
                <div className="analytics-loading">
                    <div className="spinner"></div>
                    <p>Analyzing media...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="analytics-panel">
            <h2 className="panel-title gradient-text">📊 Analysis Results</h2>

            <div className="analytics-grid">
                {/* Image Analysis */}
                {analysis.caption && (
                    <div className="analytics-card">
                        <h3 className="card-title">🖼️ Caption</h3>
                        <p className="card-text">{analysis.caption}</p>
                    </div>
                )}

                {/* Colors */}
                {analysis.colors && (
                    <div className="analytics-card">
                        <h3 className="card-title">🎨 Dominant Colors</h3>
                        <div className="color-palette">
                            {analysis.colors.map((color, i) => (
                                <div
                                    key={i}
                                    className="color-swatch"
                                    style={{ backgroundColor: color }}
                                    title={color}
                                ></div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Transcript */}
                {analysis.transcript && (
                    <div className="analytics-card full-width">
                        <h3 className="card-title">📝 Transcript</h3>
                        <div className="transcript-container">
                            <p className="card-text">{analysis.transcript}</p>
                        </div>
                    </div>
                )}

                {/* Sentiment */}
                {analysis.sentiment && (
                    <div className="analytics-card">
                        <h3 className="card-title">💭 Sentiment</h3>
                        <div className="sentiment-badge" data-sentiment={analysis.sentiment.label}>
                            {analysis.sentiment.label}
                        </div>
                        <p className="sentiment-score">
                            Confidence: {(analysis.sentiment.score * 100).toFixed(1)}%
                        </p>
                    </div>
                )}

                {/* Language */}
                {analysis.language && (
                    <div className="analytics-card">
                        <h3 className="card-title">🌐 Language</h3>
                        <p className="card-text language-text">{analysis.language}</p>
                    </div>
                )}

                {/* Video Summary */}
                {analysis.visual_summary && (
                    <div className="analytics-card full-width">
                        <h3 className="card-title">🎬 Visual Summary</h3>
                        <p className="card-text">{analysis.visual_summary}</p>
                    </div>
                )}

                {/* Frame Analysis */}
                {analysis.frames && analysis.frames.samples && (
                    <div className="analytics-card full-width">
                        <h3 className="card-title">
                            🎞️ Frame Analysis ({analysis.frames.analyzed} of {analysis.frames.total_extracted})
                        </h3>
                        <div className="frames-list">
                            {analysis.frames.samples.slice(0, 5).map((frame, i) => (
                                <div key={i} className="frame-item">
                                    <span className="frame-time">{frame.timestamp.toFixed(1)}s</span>
                                    <span className="frame-caption">{frame.caption}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Word Count */}
                {analysis.word_count && (
                    <div className="analytics-card">
                        <h3 className="card-title">📊 Word Count</h3>
                        <p className="stat-number">{analysis.word_count}</p>
                    </div>
                )}
            </div>
        </div>
    );
}
