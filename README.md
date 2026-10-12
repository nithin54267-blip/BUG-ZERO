# BUG-ZERO: AI-Powered Code Bug Finder

Paste code in any language, get bugs with type, severity, plain explanation and corrected code. Reports are saved per user.

## Run it
```bash
cd BUG-ZERO
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
cp .env.example .env                                  # then edit .env: add ANTHROPIC_API_KEY and a SECRET_KEY
cd backend && python app.py
```
Open http://localhost:5000. Flask serves the frontend and the API (`/api/...`) together.
If you host the frontend separately, change `API` in `frontend/js/api.js`.

## API
| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | /api/register | no | username, email, password |
| POST | /api/login | no | identifier (email or username), password |
| POST | /api/analyze | JWT | code, optional language |
| GET | /api/history?q= | JWT | list/search reports |
| GET | /api/history/<id> | JWT | one report |
| DELETE | /api/history/<id> | JWT | delete a report |

## Notes
- Passwords are hashed with werkzeug; sessions use JWT (24 h).
- Code is never executed on the server; it is only sent to the LLM API.
- Model is set by `ANTHROPIC_MODEL` in `.env`.
- Deploying with MySQL: change `models/db.py` to use a MySQL driver (e.g. PyMySQL) and adapt `database/schema.sql` (`AUTO_INCREMENT`, `DATETIME`).
- Keep `.env` private and out of Git.
