# WeTransfer Clone

> **Disclaimer:** The boilerplate for the project was generated with the help of an Github copilot default AI agent with Claude Haiku 4.5 model. Aside from this initial scaffolding step, AI assistance has been kept to a minimum due to usage constraints on the GitHub Copilot free tier.


A MVP for a small file sharing application using React (Vite) frontend and Python AWS Lambda backend.

## ✨ Features

- 📤 **File Upload**: Upload files up to 2 MB with client-side validation
- 📋 **File History**: View all your uploaded files with timestamps
- ⏱️ **Auto-Deletion**: Files automatically delete after 2 minutes
- 🔐 **Authentication**: Placeholder for real OAuth/JWT integration
- ⚡ **Rate Limiting**: 100 requests per 15 minutes per user
- 🚀 **Serverless**: AWS Lambda, API Gateway, S3, DynamoDB
- 💰 **Free Tier**: Designed to stay within AWS Free Tier limits
- 🧪 **Well-Tested**: Jest + React Testing Library (frontend), pytest (backend)
- 📚 **Documented**: Comprehensive docs, architecture diagrams, best practices

## 🏗️ Architecture

```
Frontend (React/Vite)          Backend (Python/Lambda)       Storage (AWS)
        │                              │                           │
        ├─ Upload Form        ┌─ upload.py       ┌─ / ← S3 Bucket
        ├─ File List          ├─ list_files.py   ├─ DynamoDB Metadata
        ├─ Auth Guard         ├─ download.py     └─ SQS Queue (Deletes)
        └─ API Service        ├─ delete_file.py
                              └─ rate_limit.py
```

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- Python 3.11+
- AWS Account (Free Tier)
- Serverless Framework

### Setup
```bash
# Initialize development environment
bash scripts/dev.sh setup

# Start frontend 
bash scripts/dev.sh frontend

# Run backend tests 
bash scripts/dev.sh backend

# Run all tests
bash scripts/dev.sh test
```

### Deploy
```bash
# Deploy backend to AWS
bash scripts/deploy-backend.sh dev

# Deploy frontend to S3
bash scripts/deploy-frontend.sh dev
```

## 📁 Repository Structure

```
├── frontend/          # React + Vite + Tailwind
├── backend/           # Python + AWS Lambda + Serverless
├── .github/workflows/ # CI/CD pipeline
└── README.md
```

## Frontend Setup

See [frontend/README.md](frontend/README.md) for detailed instructions.

Quick start:
```bash
cd frontend
npm install
npm run dev
```

## Backend Setup

See [backend/README.md](backend/README.md) for detailed instructions.

Quick start:
```bash
cd backend
pip install -r requirements.txt
serverless deploy
```

## Features (Placeholder)

- File upload/download (max 2MB)
- User authentication
- Rate limiting
- Auto-delete after 2 minutes
- User data segregation
- Shareable links

## Notes

See TODO comments in the code for where real business logic should be added.
