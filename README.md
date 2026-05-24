# BlinkFinder

A FastAPI backend that scrapes and stores Hot Wheels product listings from FirstCry, with price history tracking per pincode.

## Project Structure

```
BlinkFinder/
├── models/
│   └── item.py            # SQLAlchemy DB models
├── routes/
│   └── firstcry.py        # API route definitions
├── services/
│   └── fcrequester.py     # Fetching and parsing logic
├── database.py            # DB connection and session
├── main.py                # FastAPI app entry point
├── Procfile               # Railway deployment config
├── requirements.txt       # Python dependencies
├── .env                   # Secret config (not committed)
└── .env.example           # Template for environment variables
```

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/BlinkFinder.git
cd BlinkFinder
```

### 2. Install dependencies
```bash
pip install fastapi uvicorn requests python-dotenv sqlalchemy psycopg2-binary
```

### 3. Configure environment variables
```
FC_COOKIE="your_firstcry_cookie_here"
FC_DEFAULT_PCODE="500***"
DATABASE_URL="postgresql://user:password@host:5432/dbname"
```

To get your `FC_COOKIE`: Open firstcry.com in Chrome → DevTools → Network tab → any product request → copy the `Cookie` header value.

### 4. Run the server
```bash
uvicorn main:app --reload
```

---

## API Reference

### `GET /fc`
Fetches live listings from FirstCry and saves to DB.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | `1` | Page number |
| `pcode` | str | from `.env` | Delivery pincode |

---

### `GET /fc/scrape-all`
Scrapes pages 1–5 and saves all products and price snapshots to DB in one shot.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `pcode` | str | from `.env` | Delivery pincode |

Response:
```json
{ "message": "Scrape complete", "snapshots_saved": 98 }
```

---

### `GET /fc/saved`
Returns saved product data from DB. No FirstCry call made.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `pcode` | str | from `.env` | Delivery pincode |

---

## Database

Two tables:
- **`products`** — pid, name, brand, size
- **`price_snapshots`** — mrp, disc_price, discount, stock, rating, shipping, pcode, scraped_at

Tables are auto-created on startup via SQLAlchemy.

---

## Deployment

Hosted on Railway with auto-deploy on every GitHub push.

Environment variables to set in Railway dashboard:
- `FC_COOKIE` — FirstCry session cookie
- `FC_DEFAULT_PCODE` — default pincode
- `DATABASE_URL` — PostgreSQL URL from Railway

> **Note:** FirstCry cookies expire periodically. Refresh `FC_COOKIE` in Railway when the API starts returning errors.