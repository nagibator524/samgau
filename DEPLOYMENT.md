# Deployment Guide for Vercel

## Prerequisites
- Vercel account
- Git repository with your code

## Steps to Deploy

1. **Install Vercel CLI** (optional):
   ```bash
   npm i -g vercel
   ```

2. **Deploy via Vercel Dashboard**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your Git repository
   - Vercel will automatically detect it's a Python project

3. **Deploy via CLI**:
   ```bash
   vercel
   ```

## Important Notes

- The application uses SQLite database which will be reset on each deployment
- For production, consider using a persistent database like PostgreSQL
- Admin credentials: username: `admin`, password: `admin123`

## Environment Variables

No environment variables are required for basic deployment.

## File Structure

```
├── app.py              # Main Flask application
├── wsgi.py             # WSGI entry point for Vercel
├── vercel.json         # Vercel configuration
├── requirements.txt    # Python dependencies
├── static/             # Static files (CSS, JS, images)
│   └── images/
│       └── logo.jpeg   # Logo image
└── templates/          # HTML templates
```

## Troubleshooting

- If you get database errors, the SQLite file might not be created. The app will create it automatically on first run.
- Make sure all static files are in the `static/` directory.
- Check that `requirements.txt` includes all necessary dependencies.

