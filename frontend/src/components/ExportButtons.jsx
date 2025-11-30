import React from 'react';
import './ExportButtons.css';

export default function ExportButtons({ mediaId }) {
    const handleExport = async (format) => {
        const url = `/export/${mediaId}/${format}`;

        try {
            // Open in new tab for direct download
            window.open(url, '_blank');
        } catch (error) {
            console.error(`Export failed:`, error);
            alert(`Failed to export as ${format.toUpperCase()}`);
        }
    };

    return (
        <div className="export-buttons">
            <h3 className="export-title">📥 Export Report</h3>

            <div className="export-button-group">
                <button
                    className="export-btn export-pdf"
                    onClick={() => handleExport('pdf')}
                    title="Download as PDF"
                >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="export-icon">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                    </svg>
                    PDF
                </button>

                <button
                    className="export-btn export-json"
                    onClick={() => handleExport('json')}
                    title="Download as JSON"
                >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="export-icon">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                    </svg>
                    JSON
                </button>

                <button
                    className="export-btn export-markdown"
                    onClick={() => handleExport('markdown')}
                    title="Download as Markdown"
                >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="export-icon">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Markdown
                </button>
            </div>
        </div>
    );
}
