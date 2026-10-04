# 🚀 KAVACH: Cloud Deployment & Custom Domain Guide (e.g., `kavach.co`)

This guide shows you step-by-step how to deploy **KAVACH** permanently to the live internet with your own custom domain (e.g. `kavach.co`, `kavach.dev`, `kavach-security.io`) and free automatic HTTPS/SSL certificates.

---

## ⚡ Quick Architecture Overview

Because KAVACH is built with FastAPI mounting the frontend static assets under `/static` and redirecting `/` to the dashboard, **the entire app runs as a single unified service**:
- **Backend API**: FastAPI on `uvicorn`
- **Frontend Dashboard**: Served automatically on the same host and port (no CORS issues, zero separate frontend hosting required)
- **Database / Disk Store**: `backend/data/workflow_runs.json`

---

## 🌟 Method 1: Render.com (Recommended — 100% Free Tier + Custom Domain)

Render is the simplest and most reliable platform for hosting full-stack Python/FastAPI projects with free SSL and custom domain support.

### Step 1: Push your KAVACH project to GitHub
1. Create a repository on GitHub (e.g., `kavach-security-platform`).
2. Commit and push your project code:
   ```bash
   git init
   git add .
   git commit -m "feat: complete KAVACH security platform with 100+ query library"
   git branch -M main
   git remote add origin https://github.com/<your-username>/kavach.git
   git push -u origin main
   ```

### Step 2: Create a Web Service on Render
1. Go to [render.com](https://render.com) and sign up with your GitHub account.
2. Click **New +** &rarr; **Web Service**.
3. Select your `kavach` repository.
4. Fill in the settings:
   - **Name**: `kavach-security` (or any name you like)
   - **Region**: Frankfurt / Oregon / Singapore (pick closest to your users)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT`
   - **Instance Type**: **Free**
5. Under **Environment Variables**, add:
   - `PYTHON_VERSION`: `3.11.9`
   - `GEMINI_API_KEY`: *(Your Google AI Studio API key)*
   - `GROQ_API_KEY`: *(Optional, for Groq Whisper voice input)*
6. Click **Create Web Service**.
7. In ~3 minutes, your live URL will be active: `https://kavach-security.onrender.com`.

---

## 🌐 Method 2: Railway.app (Alternative 1-Click Cloud)

1. Go to [railway.app](https://railway.app).
2. Click **New Project** &rarr; **Deploy from GitHub repo**.
3. Select your `kavach` repository.
4. Railway will automatically detect the [Dockerfile](file:///c:/Users/jaind/Videos/PRJ-IV%20Work/kavach/Dockerfile).
5. In **Settings** &rarr; **Networking**, click **Generate Domain** to get a public `*.up.railway.app` URL.

---

## 🏷️ How to Connect Your Custom Domain (`kavach.co` / `kavach.dev`)

### Step 1: Buy Your Domain Name
You can purchase `kavach.co`, `kavach.dev`, `kavach.io`, or `kavach-security.org` from any registrar:
- **Cloudflare Registrar** (At-cost pricing, ~$8-$10/year, no markup)
- **Porkbun** or **Namecheap** (~$8-$12/year)

### Step 2: Point Domain to Render or Railway

#### In Render:
1. Open your Web Service dashboard &rarr; **Settings** &rarr; **Custom Domains**.
2. Click **Add Custom Domain** and enter:
   - `kavach.co` and `www.kavach.co`
3. Render will give you DNS instructions:
   - **For `www.kavach.co`**: Add a `CNAME` record pointing to `kavach-security.onrender.com`
   - **For apex `kavach.co`**: Add an `ANAME` or `ALIAS` record pointing to `kavach-security.onrender.com` (or an `A` record with the IP Render provides).

#### In Cloudflare DNS (Best Practice):
If you use Cloudflare for DNS (Free):
| Type | Name | Content / Target | Proxy status | TTL |
| :--- | :--- | :--- | :--- | :--- |
| `CNAME` | `@` | `kavach-security.onrender.com` | Proxied (Orange) | Auto |
| `CNAME` | `www` | `kavach-security.onrender.com` | Proxied (Orange) | Auto |

Cloudflare will automatically provide:
- 🔒 **Zero-SSL / Global HTTPS**
- ⚡ **Global CDN Edge Caching**
- 🛡️ **DDoS & Web Application Firewall (WAF)**

---

## 🐳 Method 3: Self-Hosting with Docker (VPS / AWS / DigitalOcean)

If you prefer full control on an Ubuntu VPS ($4-$6/mo on DigitalOcean, Hetzner, or AWS Lightsail):

```bash
# 1. Clone repository
git clone https://github.com/<your-username>/kavach.git
cd kavach

# 2. Launch container with Docker Compose
docker compose up -d --build
```
Your service will be running on port 8000. Set up Nginx as a reverse proxy:

```nginx
server {
    server_name kavach.co www.kavach.co;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Run `certbot --nginx -d kavach.co -d www.kavach.co` to get a free SSL certificate.

---

## 🛡️ Checklist Before Launching Publicly

- [ ] Set `GEMINI_API_KEY` in your hosting dashboard environment variables.
- [ ] Confirm `/health` returns status `200` (`https://kavach.co/health`).
- [ ] Verify the 100+ Enterprise Test Query Library opens in the browser.
- [ ] Test a sample workflow request and verify the green permanent sync badge is active.
