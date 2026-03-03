# WeTransfer Clone -  Project

> **Disclaimer:** The boilerplate for the project was generated with the help of an AI agent. The prompt used for generation can be found in the `doc/boilerplate_workflow_with_agent.txt` file. Aside from this initial scaffolding step, AI assistance has been kept to a minimum due to usage constraints on the GitHub Copilot free tier.


A MVP for a small file sharing application using React (Vite) frontend and Python AWS Lambda backend.

## Project Structure

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
