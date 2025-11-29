# Multi-Modal AI Inspector - Frontend

Modern React frontend for the Multi-Modal AI Inspector with stunning UI and real-time analytics.

## Features

- 🎨 **Modern Dark UI** - Glassmorphism, gradients, smooth animations
- 📤 **Drag & Drop Upload** - Easy file uploads with progress tracking
- 📊 **Analytics Dashboard** - Visual cards for all analysis results
- 💬 **AI Chat Interface** - Conversational assistant with typing indicators
- 📱 **Fully Responsive** - Works beautifully on all devices
- ⚡ **Real-time Updates** - Polling for analysis completion

## Tech Stack

- React 18
- Vite (lightning-fast build tool)
- Axios for API calls
- Modern CSS with custom design system
- Google Fonts (Inter)

## Setup

### Installation

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm run dev
```

Frontend will be available at: http://localhost:5173

### Build for Production

```bash
npm run build
```

Build output will be in `dist/` directory.

Preview production build:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── UploadDropzone.jsx
│   │   ├── UploadDropzone.css
│   │   ├── MediaPlayer.jsx
│   │   ├── MediaPlayer.css
│   │   ├── AnalyticsPanel.jsx
│   │   ├── AnalyticsPanel.css
│   │   ├── ChatPanel.jsx
│   │   └── ChatPanel.css
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── package.json
├── vite.config.js
└── index.html
```

## Components

### UploadDropzone
- Drag-and-drop file upload
- Progress bar during upload
- File validation and size limits
- Animated hover effects

### MediaPlayer
- Displays images, audio, and video
- Shows metadata (dimensions, duration, size)
- Responsive media controls

### AnalyticsPanel
- Dynamic cards for all analysis types
- Color palette visualization
- Sentiment badges
- Frame-by-frame breakdown
- Transcript viewer

### ChatPanel
- Real-time chat interface
- Message history
- Typing indicators
- Source attribution
- Auto-scroll

## API Integration

The frontend proxies API requests to `http://localhost:8000` during development.

Configure in `vite.config.js`:
```javascript
server: {
  proxy: {
    '/upload': 'http://localhost:8000',
    '/media': 'http://localhost:8000',
    // ...
  }
}
```

## Design System

All design tokens are defined in `src/index.css`:

- Colors: Primary, secondary, backgrounds
- Spacing: xs, sm, md, lg, xl, 2xl
- Typography: Font sizes, families
- Shadows & effects
- Transitions & animations

## Customization

### Change Colors

Edit CSS variables in `src/index.css`:

```css
:root {
  --color-primary: hsl(250, 84%, 54%);
  --color-secondary: hsl(280, 80%, 56%);
  /* ... */
}
```

### Add New Components

1. Create component file in `src/components/`
2. Create corresponding CSS file
3. Import and use in `App.jsx`

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Development Tips

- Hot Module Replacement (HMR) enabled for instant updates
- React DevTools recommended for debugging
- ESLint configuration available (optional)

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Vercel auto-detects Vite config
4. Deploy!

### Build + Static Host

```bash
npm run build
# Upload dist/ folder to any static host
```

Compatible with:
- Netlify
- GitHub Pages
- Cloudflare Pages
- AWS S3 + CloudFront

## Environment Variables

Create `.env.local` for custom API URL:

```
VITE_API_URL=https://your-api-domain.com
```

## License

MIT
