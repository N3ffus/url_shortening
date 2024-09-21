# Url Shortener

## Tech stack
- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL

## Features
- Create a new short URL
- Retrieve an original URL from a short URL
- Update an existing short URL
- Delete an existing short URL
- Get statistics on the short URL (e.g., number of times accessed)

## API endpoints
### POST /shorten
Create a new short URL
### GET /shorten/<short_code>
Retrieve original URL from short URL
### PUT /shorten/<short_code>
Update an existing short URL
### DELETE /shorten/<short_code>
Delete an existing short URL
### GET /shorten/<short_code>/stats
Get statistic for a short URL
