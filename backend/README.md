# Backend: Simple Movie App with ReactJS

Backend for ReactJS WebApp using FastAPI

## Setup (Bash)

### Prepare virtual environment

```bash
# Create virtual environment -m (module)
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Install package

```bash
# Install package using requirement files (-r)
pip install -r requirements.txt
```

### Run Server

Run server using backend.py

```bash
python backend.py
```

For Development mode we can use reload feature

```bash
uvicorn backend:app --reload
```
