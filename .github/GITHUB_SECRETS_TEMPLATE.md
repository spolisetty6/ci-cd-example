# GitHub Secrets Configuration

This document describes the secrets needed for the CI/CD pipelines to work correctly.

## How to Add Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret below

---

## Required Secrets

### Docker Registry Credentials
```
DOCKER_HUB_USERNAME
Type: String
Description: Your Docker Hub username
Example: myusername
```

```
DOCKER_HUB_PASSWORD
Type: String
Description: Your Docker Hub password or access token
Example: dckr_pat_...
```

### Deployment Credentials
```
DEPLOY_KEY
Type: String (SSH Private Key)
Description: SSH private key for deployment server access
Generate with: ssh-keygen -t ed25519 -f deploy_key
Format: -----BEGIN OPENSSH PRIVATE KEY-----
        [key content]
        -----END OPENSSH PRIVATE KEY-----
```

```
DEPLOY_HOST
Type: String
Description: Production server hostname or IP
Example: api.example.com
```

```
DEPLOY_USER
Type: String
Description: SSH user for deployment
Example: deploy
```

```
STAGING_HOST
Type: String
Description: Staging server hostname or IP
Example: staging-api.example.com
```

```
DB_PASSWORD
Type: String (Secret)
Description: Database password for production
Example: secure_password_here
```

### Monitoring and Notifications
```
SLACK_WEBHOOK_URL
Type: String (Secret)
Description: Slack webhook URL for CI/CD notifications
Get from: Slack App → Incoming Webhooks
Format: https://hooks.slack.com/services/TXXXXXXXX/BXXXXXXXX/XXXXXXXXXXXX
```

```
SNYK_TOKEN
Type: String (Secret)
Description: Snyk security scanning API token
Get from: https://app.snyk.io/account/api-token
```

### Code Quality
```
CODECOV_TOKEN
Type: String (Secret)
Description: Codecov.io API token for coverage reports
Optional if repository is public
Get from: https://codecov.io/account
```

---

## Optional Secrets

### Container Registry (GitHub Container Registry)
GitHub automatically uses `GITHUB_TOKEN` for GHCR authentication.
No additional setup needed.

### PyPI (Python Package Publishing)
```
PYPI_API_TOKEN
Type: String (Secret)
Description: PyPI API token for publishing Python packages
Get from: https://pypi.org/account/api-tokens/
```

---

## Secret Management Best Practices

1. **Rotate Regularly**: Change secrets every 90 days
2. **Use Least Privilege**: Create tokens with minimal required permissions
3. **Monitor Usage**: Check audit logs for secret access
4. **Use Environment-Specific Secrets**: Have separate secrets for staging/production
5. **Never Commit Secrets**: Use `.gitignore` to prevent accidental commits
6. **Use GitHub Environments**: Separate secrets for staging and production

---

## Testing Secrets

To verify secrets are working in your workflows:

```yaml
- name: Test Secret Access
  run: |
    if [ -n "${{ secrets.DEPLOY_KEY }}" ]; then
      echo "✓ Secret is accessible"
    else
      echo "✗ Secret is not set"
    fi
```

---

## Troubleshooting

**Issue**: Secret not available in workflow
- **Solution**: Verify secret name matches exactly in workflow file (case-sensitive)

**Issue**: Deployment fails with permission error
- **Solution**: Check SSH key permissions (600), add public key to authorized_keys

**Issue**: Cannot access secret in pull request
- **Solution**: Secrets are not available in pull requests from forks by default

---

## Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments)
- [Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
