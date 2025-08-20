# XReason Deployment Guide

## Overview

This guide covers deploying XReason in various environments, from local development to production.

## Prerequisites

- Docker and Docker Compose
- OpenAI API key
- (Optional) Domain name and SSL certificate for production

## Local Development

### Quick Start

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
   # Edit backend/.env and add your OpenAI API key
   cp backend/env.example backend/.env
   # Add your OpenAI API key to backend/.env
   ```

4. **Start services:**
   ```bash
   docker-compose up -d
   ```

5. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Development Mode

For development with hot reloading:

```bash
docker-compose --profile dev up -d
```

This will start:
- Backend with auto-reload
- Frontend dev server on http://localhost:3001

## Production Deployment

### Docker Compose (Recommended)

1. **Create production environment file:**
   ```bash
   cp backend/env.example backend/.env.prod
   ```

2. **Configure production settings:**
   ```bash
   # Edit backend/.env.prod
   DEBUG=False
   LOG_LEVEL=WARNING
   OPENAI_API_KEY=your_production_key
   SECRET_KEY=your_secure_secret_key
   ```

3. **Create production docker-compose file:**
   ```bash
   cp docker-compose.yml docker-compose.prod.yml
   ```

4. **Deploy:**
   ```bash
   docker-compose -f docker-compose.prod.yml --env-file backend/.env.prod up -d
   ```

### Kubernetes Deployment

1. **Create namespace:**
   ```bash
   kubectl create namespace xreason
   ```

2. **Create ConfigMap for environment variables:**
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: xreason-config
     namespace: xreason
   data:
     DEBUG: "False"
     LOG_LEVEL: "WARNING"
     OPENAI_MODEL: "gpt-4o"
   ```

3. **Create Secret for sensitive data:**
   ```bash
   kubectl create secret generic xreason-secrets \
     --from-literal=openai-api-key=your_key \
     --from-literal=secret-key=your_secret \
     -n xreason
   ```

4. **Apply Kubernetes manifests:**
   ```bash
   kubectl apply -f infrastructure/kubernetes/
   ```

### Cloud Platform Deployments

#### AWS ECS

1. **Create ECR repositories:**
   ```bash
   aws ecr create-repository --repository-name xreason-backend
   aws ecr create-repository --repository-name xreason-frontend
   ```

2. **Build and push images:**
   ```bash
   # Backend
   docker build -t xreason-backend ./backend
   docker tag xreason-backend:latest $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com/xreason-backend:latest
   docker push $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com/xreason-backend:latest

   # Frontend
   docker build -t xreason-frontend ./frontend
   docker tag xreason-frontend:latest $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com/xreason-frontend:latest
   docker push $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com/xreason-frontend:latest
   ```

3. **Deploy using ECS:**
   ```bash
   aws ecs create-cluster --cluster-name xreason
   aws ecs create-service --cluster xreason --service-name xreason-backend --task-definition xreason-backend
   aws ecs create-service --cluster xreason --service-name xreason-frontend --task-definition xreason-frontend
   ```

#### Google Cloud Run

1. **Build and deploy backend:**
   ```bash
   gcloud builds submit --tag gcr.io/$PROJECT_ID/xreason-backend ./backend
   gcloud run deploy xreason-backend \
     --image gcr.io/$PROJECT_ID/xreason-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

2. **Build and deploy frontend:**
   ```bash
   gcloud builds submit --tag gcr.io/$PROJECT_ID/xreason-frontend ./frontend
   gcloud run deploy xreason-frontend \
     --image gcr.io/$PROJECT_ID/xreason-frontend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

#### Azure Container Instances

1. **Build and push to Azure Container Registry:**
   ```bash
   az acr build --registry $ACR_NAME --image xreason-backend ./backend
   az acr build --registry $ACR_NAME --image xreason-frontend ./frontend
   ```

2. **Deploy containers:**
   ```bash
   az container create \
     --resource-group $RG_NAME \
     --name xreason-backend \
     --image $ACR_NAME.azurecr.io/xreason-backend:latest \
     --ports 8000 \
     --environment-variables OPENAI_API_KEY=$OPENAI_API_KEY
   ```

## Environment Variables

### Backend (.env)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | Yes |
| `OPENAI_MODEL` | OpenAI model to use | gpt-4o | No |
| `DEBUG` | Debug mode | True | No |
| `LOG_LEVEL` | Logging level | INFO | No |
| `SECRET_KEY` | Secret key for security | - | Yes (prod) |
| `DATABASE_URL` | Database connection string | sqlite:///./xreason.db | No |
| `BACKEND_CORS_ORIGINS` | CORS origins | ["http://localhost:3000"] | No |

### Frontend (.env)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `REACT_APP_API_URL` | Backend API URL | http://localhost:8000 | No |

## Monitoring and Logging

### Health Checks

The application includes built-in health checks:

```bash
# Basic health check
curl http://localhost:8000/health/

# Detailed health check
curl http://localhost:8000/health/detailed
```

### Logging

Logs are available through Docker:

```bash
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# Follow logs
docker-compose logs -f backend
```

### Metrics

For production deployments, consider adding:

- Prometheus metrics endpoint
- Grafana dashboards
- Application Performance Monitoring (APM)

## Security Considerations

### Production Checklist

- [ ] Use HTTPS/TLS
- [ ] Set secure `SECRET_KEY`
- [ ] Configure CORS properly
- [ ] Implement rate limiting
- [ ] Add authentication/authorization
- [ ] Use secrets management
- [ ] Enable security headers
- [ ] Regular security updates

### SSL/TLS Configuration

For production, configure SSL certificates:

```nginx
# nginx.conf
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    # ... rest of configuration
}
```

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/xreason
```

### Load Balancing

Use a reverse proxy like nginx or Traefik:

```yaml
# docker-compose.yml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
```

## Backup and Recovery

### Database Backup

```bash
# SQLite (development)
cp backend/xreason.db backup/xreason-$(date +%Y%m%d).db

# PostgreSQL (production)
pg_dump $DATABASE_URL > backup/xreason-$(date +%Y%m%d).sql
```

### Application Backup

```bash
# Backup configuration
tar -czf backup/config-$(date +%Y%m%d).tar.gz backend/.env* frontend/.env*

# Backup logs
tar -czf backup/logs-$(date +%Y%m%d).tar.gz logs/
```

## Troubleshooting

### Common Issues

1. **OpenAI API errors:**
   - Check API key is valid
   - Verify API quota/limits
   - Check network connectivity

2. **Docker build failures:**
   - Clear Docker cache: `docker system prune -a`
   - Check Dockerfile syntax
   - Verify dependencies

3. **Service won't start:**
   - Check logs: `docker-compose logs <service>`
   - Verify environment variables
   - Check port conflicts

4. **Frontend can't connect to backend:**
   - Verify CORS configuration
   - Check API URL in frontend
   - Ensure backend is healthy

### Debug Mode

Enable debug mode for troubleshooting:

```bash
# Backend
DEBUG=True LOG_LEVEL=DEBUG docker-compose up backend

# Frontend
REACT_APP_DEBUG=true docker-compose up frontend
```

## Support

For deployment issues:

1. Check the logs: `docker-compose logs`
2. Verify environment configuration
3. Test individual services
4. Check the troubleshooting section above
5. Open an issue on GitHub with logs and configuration details
