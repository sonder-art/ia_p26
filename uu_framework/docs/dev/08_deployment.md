---
title: "Deployment"
---

# Deployment to GitHub Pages

uu_framework sites deploy automatically to GitHub Pages at `www.sonder.art/{repo-name}/`.

## How It Works

1. **Push to main** → GitHub Actions workflow triggers
2. **Build** → Python preprocessing + Eleventy + Tailwind CSS
3. **Deploy** → Uploaded to GitHub Pages

## Prerequisites

### 1. Repository Settings

1. Go to **Settings > Pages**
2. Set **Source** to "GitHub Actions"
3. (Optional) Verify custom domain shows `www.sonder.art`

### 2. Organization Setup (One-time)

For custom domain `www.sonder.art`:

1. Create `{org}.github.io` repository (if not exists)
2. Add `CNAME` file with `www.sonder.art`
3. Configure DNS:
   - `A` records pointing to GitHub Pages IPs
   - `CNAME` for `www` pointing to `{org}.github.io`

## Creating a New Course Repo

1. **Create repo** at `{org}/{course-name}`

2. **Copy uu_framework structure**:
   ```
   {course-name}/
   ├── .github/workflows/deploy.yaml  # Copy from {repo-name}
   ├── clase/                         # Your course content
   ├── uu_framework/                  # Copy entire directory
   └── .gitignore                     # Copy from {repo-name}
   ```

3. **Update docker-compose.yaml** (for local dev):
   ```yaml
   environment:
     - PATH_PREFIX=/{course-name}/
   ```

4. **Push to main** → Automatic deployment

## Workflow Details

The workflow (`.github/workflows/deploy.yaml`) is designed to be **reusable**:

- **Auto-detects repo name** for path prefix
- **Adds CNAME** for custom domain
- **Caches dependencies** for faster builds

### Key Environment Variables

| Variable | Source | Purpose |
|----------|--------|---------|
| `PATH_PREFIX` | Auto from repo name | URL path prefix |
| `CUSTOM_DOMAIN` | Workflow env | CNAME file content |
| `NODE_ENV` | Set to `production` | Optimizes build |

## Manual Deployment

Trigger manually via GitHub:

1. Go to **Actions** tab
2. Select **Deploy to GitHub Pages**
3. Click **Run workflow**

## Troubleshooting

### Build Fails

1. Check **Actions** tab for error logs
2. Common issues:
   - Missing `package-lock.json` in `uu_framework/eleventy/`
   - Python dependencies not listed
   - Invalid markdown syntax

### 404 on Deployed Site

1. Verify GitHub Pages is enabled
2. Check `pathPrefix` matches repo name
3. Wait 2-5 minutes for DNS propagation

### CSS Not Loading

1. Check `pathPrefix` in URLs
2. Verify Tailwind build step succeeded
3. Check browser console for 404s

## Local Testing Before Deploy

```bash
# Start dev server
docker compose -f uu_framework/docker/docker-compose.yaml up dev

# Build production version
docker compose -f uu_framework/docker/docker-compose.yaml run build

# Check _site/ output
ls -la _site/
```

## URLs

| Environment | URL |
|-------------|-----|
| Production | `https://www.sonder.art/{repo-name}/` |
| Local dev | `http://localhost:3000/{repo-name}/` |
