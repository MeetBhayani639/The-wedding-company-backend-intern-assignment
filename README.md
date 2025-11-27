# The Wedding Company - Backend Intern Assignment

**Candidate:** Meet Bhayani  
**Multi-tenant Organization Management Service using FastAPI + MongoDB**

## Features Implemented
- Create organization with dynamic MongoDB collection
- Admin login with JWT authentication
- Get, Update (with collection rename & data sync), Delete organization
- Secure password hashing with bcrypt
- Proper JWT-based authorization for update/delete

## Architecture Evaluation
This design is **good for medium scale** (100–5000 tenants).  
**Pros:** Strong data isolation, easy backups per tenant  
**Cons:** Too many collections hurt performance at scale (>10k tenants), schema changes are hard

**Better Production Design Suggestion:**  
Use **single collection with `tenant_id` field + database sharding** — easier to manage, better performance, same isolation via indexes.

## Run Locally
```bash
python -m virtualenv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload