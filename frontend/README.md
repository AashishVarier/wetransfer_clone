 # Frontend - WeTransfer Clone

React 18 + Vite + Tailwind CSS for the file sharing web application.

## Setup

### Prerequisites
- Node.js 16+ and npm
- Backend API running (see `../backend/README.md`)

### Installation

```bash
cd frontend
npm install
```

### Configuration

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Configure environment variables:
```env
VITE_API_BASE_URL=http://localhost:3001/api  # Backend API endpoint
MAX_FILE_SIZE_MB=2                           # Max upload size
FILE_EXPIRATION_MINUTES=2                    # When files auto-delete
```

For production, set `VITE_API_BASE_URL` to your deployed backend URL.

### Development

Run the dev server with hot reload:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

Or use the helper script from root:
```bash
bash ../scripts/dev.sh frontend
```

### Building

Build for production:
```bash
npm run build
```

Output will be in the `dist/` folder, ready for S3 deployment.

### Testing

Run tests with Jest + React Testing Library:
```bash
npm test
```

Or from root:
```bash
bash ../scripts/dev.sh test
```

Run with coverage:
```bash
npm test -- --coverage
```

## Deployment to S3

Using the deploy script (requires AWS credentials):
```bash
bash ../scripts/deploy-frontend.sh dev
```

Or manually:

1. Build the project:
   ```bash
   npm run build
   ```

2. Upload `dist/` folder to AWS S3:
   ```bash
   aws s3 sync dist/ s3://your-bucket-name/ --delete
   ```

3. Enable static website hosting in S3 bucket settings.

4. (Optional) Set up CloudFront CDN for caching and HTTPS.

## Project Structure

```
frontend/
├── src/
│   ├── main.jsx                 # React app entry point
│   ├── App.jsx                  # Main app component with routing
│   ├── index.css                # Global styles
│   ├── components/
│   │   ├── AuthGuard.jsx        # Authentication wrapper component
│   │   ├── UploadForm.jsx       # File upload form (2MB validation)
│   │   └── FileList.jsx         # Display uploaded files table
│   └── services/
│       └── api.js               # Backend API client wrapper
├── tests/
│   ├── App.test.jsx             # Main app tests
│   └── (component tests)
├── .env.example                 # Environment template
├── vite.config.js               # Vite bundler configuration
├── tailwind.config.js           # Tailwind utility CSS config
├── jest.config.js               # Jest test runner config
├── jest.setup.js                # Jest test setup (DOM utilities)
├── postcss.config.js            # PostCSS + Tailwind pipeline
├── package.json                 # Dependencies and scripts
└── README.md
```

## Components

### AuthGuard
Wraps the app and ensures user is authenticated before showing content.
- Checks for `authToken` in localStorage
- Shows login form if not authenticated
- Uses demo login (placeholder for real OAuth/JWT)

**Location:** `src/components/AuthGuard.jsx`

### UploadForm
File upload interface with validation and progress tracking.
- Drag-and-drop file input
- 2MB file size validation
- Progress bar during upload
- Error messages on validation fail

**Location:** `src/components/UploadForm.jsx`

**Usage:**
```jsx
<UploadForm onUploadComplete={(fileId) => refreshFileList()} />
```

### FileList
Displays table of user's uploaded files with action buttons.
- Shows filename, size, upload time, expiration time
- Download button (generates presigned URL)
- Copy share link button (TODO: implement share URL)
- Delete button (with confirmation)
- Pagination support (TODO: implement)

**Location:** `src/components/FileList.jsx`

**Usage:**
```jsx
<FileList onFileDeleted={() => refreshFileList()} />
```

## API Service

The `src/services/api.js` module provides wrapper functions for backend calls:

```javascript
// Upload file and get presigned URL
const { uploadUrl, fileId } = await uploadFile('filename.pdf');

// List user's files with pagination
const { files, nextToken } = await getFiles(paginationToken);

// Get presigned download URL
const { downloadUrl } = await getDownloadUrl(fileId);

// Delete a file
await deleteFile(fileId);

// Check rate limit status
const { requestsRemaining } = await checkRateLimit();

// Generate a shareable link
const shareUrl = await generateShareLink(fileId);

// Health check
const { status } = await healthCheck();
```

All functions include:
- Authorization header with JWT token from localStorage
- Error handling with user-friendly messages
- Timeout protection
- Automatic retry logic (TODO)

See `src/services/api.js` for implementation details.

## Development Workflow

1. **Start backend** (in separate terminal):
   ```bash
   cd ../backend
   bash ../scripts/dev.sh backend
   ```

2. **Start frontend dev server**:
   ```bash
   bash ../scripts/dev.sh frontend
   ```

3. **In another terminal, run tests**:
   ```bash
   bash ../scripts/dev.sh test
   ```

4. **Edit React components** - changes hot-reload automatically in browser

## Environment Variables

Copy and configure `.env.example`:
```env
# Backend API endpoint
VITE_API_BASE_URL=http://localhost:3001/api

# File upload constraints
MAX_FILE_SIZE_MB=2
FILE_EXPIRATION_MINUTES=2

# Feature flags (for gradual rollout)
VITE_ENABLE_SHARE_LINKS=true
VITE_ENABLE_RATE_LIMIT_UI=true
VITE_DEBUG_MODE=false
```

**Note:** Vite environment variables must start with `VITE_` prefix to be exposed to client code.

## Testing

The test suite uses:
- **Jest** - Test runner and assertion library
- **React Testing Library** - Component testing utilities (prefer testing behavior over implementation)
- **@testing-library/jest-dom** - Extended matchers (toBe Visible, etc.)

Run tests:
```bash
npm test                    # Run in watch mode
npm test -- --coverage      # Generate coverage report
npm test -- --ci --coverage # CI mode (no watch)
```

**Key test patterns:**
- Render components with test props
- Simulate user interactions (click, type, etc.)
- Assert on rendered output, not component state
- Mock API calls to isolate component logic

See `tests/App.test.jsx` for examples.

## Build & Deploy

### Development Build
```bash
npm run build
```

Output in `dist/` folder (~150KB gzipped).

### Production Deployment

1. **Prerequisites:**
   - AWS account with S3 bucket created
   - AWS CLI configured with credentials
   - CloudFront distribution (optional, for caching)

2. **Build:**
   ```bash
   npm run build
   ```

3. **Deploy to S3:**
   ```bash
   bash ../scripts/deploy-frontend.sh dev
   ```

   Or manually:
   ```bash
   aws s3 sync dist/ s3://your-bucket-name/ --delete
   ```

4. **Update CORS if needed:**
   - Frontend and backend at different origins
   - Backend `serverless.yml` includes CORS headers
   - Check `src/services/api.js` for credential handling

5. **Monitor:**
   - S3 bucket metrics in AWS Console
   - CloudFront cache hit rates
   - Browser DevTools for API calls and errors

## Troubleshooting

**API calls fail / CORS errors:**
- Verify `VITE_API_BASE_URL` in `.env` matches backend endpoint
- Check backend `serverless.yml` has `cors: true` on API Gateway
- Ensure Authorization header includes valid JWT token

**File upload fails (413 Payload Too Large):**
- API Gateway has 10MB limit by default
- Check `MAX_FILE_SIZE_MB` in frontend `.env`
- Verify presigned URL is being used for direct S3 upload

**Hot reload not working:**
- Restart dev server: `npm run dev`
- Clear browser cache (Ctrl+Shift+Delete)
- Check port 5173 not in use: `lsof -i :5173`

**Tests failing:**
- Clear Jest cache: `npm test -- --clearCache`
- Ensure all dependencies installed: `npm install`
- Check Node version 16+: `node --version`

See `../../docs/INSTRUCTION.md` for more troubleshooting.

## Production Hardening

The code includes TODO comments for production features:
- [ ] Real OAuth/JWT authentication (currently localStorage demo)
- [ ] Share link generation and validation
- [ ] Error recovery and retry logic
- [ ] Offline mode with service worker
- [ ] Performance monitoring (Sentry, etc.)
- [ ] Analytics integration
- [ ] A/B testing framework
- [ ] Accessibility audit (a11y)

Start with `src/components/AuthGuard.jsx` and `src/services/api.js` for immediate TODO items.
