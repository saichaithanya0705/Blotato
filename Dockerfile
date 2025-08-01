### Stage 1: Build React frontend ###
FROM node:18 AS frontend
WORKDIR /app
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install --legacy-peer-deps
COPY frontend ./frontend
RUN cd frontend && npm run build

### Stage 2: Setup Python backend ###
FROM python:3.10-slim

# Create backend app folder
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend ./backend

# Copy built React app from Stage 1 into backend/static (if serving via Flask/FastAPI)
COPY --from=frontend /app/frontend/build ./backend/static

WORKDIR /app/backend

# Run the backend app
CMD ["python", "main.py"]
