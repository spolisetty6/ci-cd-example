# CI/CD Setup Guide

This guide walks you through setting up the complete CI/CD pipeline for your project.

## Prerequisites

- GitHub account with repository access
- Docker installed locally (for testing)
- SSH key pair for deployment
- Accounts on third-party services (optional):
  - Docker Hub
  - Codecov.io
  - Slack (for notifications)
  - Snyk (for security scanning)

## Step 1: Clone and Customize

```bash
# Clone the repository
git clone https://github.com/spolisetty6/ci-cd-example.git
cd ci-cd-example

# Update repository references
# Edit .github/workflows/*.yml files
# Replace:
#   - ghcr.io/spolisetty6/ci-cd-example with your registry
#   - Your deployment hosts
#   - Slack webhook URL
```

## Step 2: Configure GitHub Secrets

See `.github/GITHUB_SECRETS_TEMPLATE.md` for detailed instructions.

Quick steps:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add required secrets:
   - `DEPLOY_KEY` (SSH private key)
   - `DEPLOY_HOST` (server hostname)
   - `DEPLOY_USER` (SSH user)
   - `DOCKER_HUB_USERNAME` / `DOCKER_HUB_PASSWORD`
   - `SLACK_WEBHOOK_URL` (optional)

## Step 3: Test Locally

### Node.js App
```bash
cd node-app
npm install
npm run build
npm test
npm run lint
```

### Python App
```bash
cd python-app
pip install -r requirements.txt
pytest
flake8 src/
```

### Docker
```bash
# Build image
docker build -t my-app:latest .

# Run container
docker run -p 8080:8080 my-app:latest

# Test health endpoint
curl http://localhost:8080/health

# Run with docker-compose
docker-compose up -d
curl http://localhost:8080/health
```

## Step 4: Set Up Deployment Server

### SSH Setup
```bash
# On your local machine
ssh-keygen -t ed25519 -f deploy_key -N ""

# On deployment server
cat ~/.ssh/authorized_keys
# Add public key content
```

### Server Requirements
```bash
# Update system
sudo apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Verify installation
docker --version
docker-compose --version
```

### Clone Application
```bash
# On deployment server
git clone https://github.com/your-username/ci-cd-example.git /app
cd /app

# Create environment file
echo "NODE_ENV=production" > .env
echo "DATABASE_URL=postgresql://user:password@db:5432/appdb" >> .env
```

## Step 5: Trigger CI/CD Pipeline

### Method 1: Push to Main Branch
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Method 2: Manual Trigger
1. Go to **Actions** tab in GitHub
2. Select workflow
3. Click **Run workflow**

### Method 3: Create Release Tag
```bash
git tag v1.0.0
git push origin v1.0.0
# Triggers Docker build and production deployment
```

## Step 6: Monitor Pipelines

1. Go to **Actions** tab
2. Click on workflow run to see details
3. Check **Logs** for each job
4. View **Artifacts** (build outputs, coverage reports)

## Step 7: Set Up Notifications

### Slack Integration
```bash
# Create Slack app
# 1. Go to https://api.slack.com/apps
# 2. Create New App
# 3. Enable Incoming Webhooks
# 4. Copy Webhook URL
# 5. Add to GitHub Secrets as SLACK_WEBHOOK_URL
```

## Workflow Details

### Node.js CI/CD (`node-ci.yml`)
- **Triggers**: Push to main/develop, PRs
- **Jobs**:
  1. Lint (ESLint, Prettier)
  2. Test (Jest with coverage)
  3. Build (TypeScript compilation)
  4. Security (npm audit, Snyk)
  5. Notify (Slack)

### Python CI/CD (`python-ci.yml`)
- **Triggers**: Push to main/develop, PRs
- **Jobs**:
  1. Lint (flake8, black, pylint)
  2. Test (pytest, multiple Python versions)
  3. Security (Bandit, Safety)
  4. Build (wheel distribution)
  5. Type check (mypy)
  6. Docs (Sphinx)

### Docker Build (`docker-build.yml`)
- **Triggers**: Push to main, tags (v*.*.*)
- **Jobs**:
  1. Build and push image
  2. Security scan (Trivy)
  3. Test image
  4. Create release notes

### Production Deployment (`deploy-production.yml`)
- **Triggers**: Push to main, version tags
- **Jobs**:
  1. Pre-deployment checks
  2. Deploy to staging
  3. Await approval
  4. Deploy to production
  5. Post-deployment tests
  6. Automatic rollback on failure

## Troubleshooting

### Pipeline fails with "secret not found"
- Check secret names match exactly in workflows (case-sensitive)
- Verify secret is configured in Settings → Secrets

### Docker push fails
- Verify Docker credentials are correct
- Check Docker Hub account permissions
- Ensure image tag format is valid

### Deployment fails
- Check SSH key permissions: `chmod 600 ~/.ssh/deploy_key`
- Verify server connectivity: `ssh -i deploy_key user@host`
- Check server logs: `docker-compose logs`

### Tests fail locally but pass in CI
- Ensure Python/Node versions match CI configuration
- Install exact dependency versions: `npm ci` or `pip install -r requirements.txt`
- Check environment variables in `.env`

## Best Practices

1. **Always review** workflow files for your specific needs
2. **Test locally** before pushing to main
3. **Use feature branches** for development
4. **Require PR reviews** before merging
5. **Monitor action logs** for errors
6. **Keep dependencies updated** regularly
7. **Rotate secrets** every 90 days
8. **Use environment-specific** configurations

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Node.js Best Practices](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/)
- [Python Docker Best Practices](https://docs.docker.com/language/python/build-images/)
- [Deployment Strategies](https://en.wikipedia.org/wiki/Deployment_strategy)

## Support

For issues or questions:
1. Check GitHub Actions logs
2. Review this guide
3. Consult official documentation
4. Open an issue on the repository
