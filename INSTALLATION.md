# XReason Installation Guide

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (3.9 recommended for pydatalog compatibility)
- Node.js 18+
- OpenAI API key

## Quick Start

### Option 1: Using Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd xreason
   ```

2. **Run the setup script:**
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

3. **Configure environment:**
   ```bash
   cp backend/env.example backend/.env
   # Edit backend/.env and add your OpenAI API key
   ```

4. **Start services:**
   ```bash
   docker-compose up -d
   ```

5. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Install Python 3.9

**macOS:**
```bash
# Using Homebrew
brew install python@3.9

# Or run the installation script
chmod +x scripts/install_python39.sh
./scripts/install_python39.sh
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3.9 python3.9-venv python3.9-dev
```

**Windows:**
Download Python 3.9 from https://www.python.org/downloads/

#### Backend Setup

1. **Create virtual environment:**
   ```bash
   cd backend
   python3.9 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Start the backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the frontend:**
   ```bash
   npm start
   ```

## Troubleshooting

### Python Version Issues

If you get errors about Python version compatibility:

1. **Check your Python version:**
   ```bash
   python --version
   ```

2. **Install Python 3.9 if needed:**
   ```bash
   # macOS
   brew install python@3.9
   
   # Ubuntu/Debian
   sudo apt-get install python3.9
   ```

3. **Use Python 3.9 explicitly:**
   ```bash
   python3.9 -m venv venv
   ```

### Pydatalog Installation Issues

If pydatalog fails to install:

1. **Ensure you're using Python 3.9:**
   ```bash
   python --version  # Should show Python 3.9.x
   ```

2. **Try installing with pip:**
   ```bash
   pip install pydatalog==0.17.1
   ```

3. **If still failing, the system will use fallback methods:**
   - The application will work without pydatalog
   - You'll see warnings about pydatalog not being available
   - Traditional rule-based reasoning will still function

### Z3 Solver Issues

If Z3 solver fails to install:

1. **Install system dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install build-essential
   
   # macOS
   xcode-select --install
   ```

2. **Try installing Z3:**
   ```bash
   pip install z3-solver
   ```

### OpenAI API Issues

1. **Ensure you have a valid OpenAI API key**
2. **Check your API quota and billing**
3. **Verify the API key is correctly set in `.env`**

## Development Mode

For development with hot reloading:

```bash
docker-compose --profile dev up -d
```

This will start:
- Backend with auto-reload
- Frontend dev server on http://localhost:3001

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Support

If you encounter issues:

1. Check the logs: `docker-compose logs`
2. Verify environment configuration
3. Ensure all prerequisites are installed
4. Check the troubleshooting section above
5. Open an issue on GitHub with detailed error information

