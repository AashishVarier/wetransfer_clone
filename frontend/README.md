 # Frontend - WeTransfer Clone

React + Vite + Tailwind CSS for the file sharing application.

## Setup

### Prerequisites
- Node.js 16+ and npm

### Installation

```bash
npm install
```

### Development

Run the dev server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Building

Build for production:
```bash
npm run build
```

Output will be in the `dist/` folder.

### Testing

Run tests:
```bash
npm test
```

## Deployment to S3

1. Build the project:
   ```bash
   npm run build
   ```

2. Upload `dist/` folder to AWS S3:
   ```bash
   aws s3 sync dist/ s3://your-bucket-name/
   ```

3. Enable static website hosting in S3 bucket settings.

4. (Optional) Set up CloudFront for CDN.

## Project Structure

- `src/main.jsx` - Entry point
- `src/App.jsx` - Main App component
- `src/components/` - React components
  - `UploadForm.jsx` - File upload form
  - `FileList.jsx` - List of files
- `src/services/api.js` - API calls to backend
- `tests/` - Jest + React Testing Library tests

## TODO

- [ ] Connect UploadForm to actual API
- [ ] Implement real file list fetching
- [ ] Add authentication UI
- [ ] Add error handling
- [ ] Improve styling with Tailwind
