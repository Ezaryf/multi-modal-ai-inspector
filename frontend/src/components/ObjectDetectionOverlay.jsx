import React from 'react';
import './ObjectDetectionOverlay.css';

export default function ObjectDetectionOverlay({ detections, imageDimensions, visible = true }) {
    if (!visible || !detections || detections.length === 0) {
        return null;
    }

    const { width: imgWidth, height: imgHeight } = imageDimensions;

    return (
        <div className="object-detection-overlay">
            <svg
                className="detection-svg"
                viewBox={`0 0 ${imgWidth} ${imgHeight}`}
                preserveAspectRatio="xMidYMid meet"
            >
                {detections.map((detection, index) => {
                    const { bbox, label, confidence } = detection;
                    const { x, y, width, height } = bbox;

                    // Color based on confidence
                    const hue = confidence * 120; // Green at 100%, red at 0%
                    const color = `hsl(${hue}, 70%, 50%)`;

                    return (
                        <g key={index} className="detection-box">
                            {/* Bounding box rectangle */}
                            <rect
                                x={x}
                                y={y}
                                width={width}
                                height={height}
                                fill="none"
                                stroke={color}
                                strokeWidth="3"
                                className="bbox-rect"
                            />

                            {/* Label background */}
                            <rect
                                x={x}
                                y={y - 25}
                                width={label.length * 8 + 20}
                                height={25}
                                fill={color}
                                className="label-bg"
                            />

                            {/* Label text */}
                            <text
                                x={x + 5}
                                y={y - 8}
                                fill="white"
                                fontSize="14"
                                fontWeight="bold"
                                className="label-text"
                            >
                                {label} {(confidence * 100).toFixed(0)}%
                            </text>
                        </g>
                    );
                })}
            </svg>
        </div>
    );
}
