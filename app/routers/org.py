from fastapi import APIRouter, Depends, HTTPException, Header
from app.schemas import OrgCreate, OrgUpdate
from app.db import DB
from app.utils import hash_password, verify_token

router = APIRouter(tags=["Organization"])

def current_admin(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token required")
    token = authorization.split(" ")[1]
    return verify_token(token)

@router.post("/org/create")
def create_organization(data: OrgCreate):
    if DB.master().find_one({"name": data.organization_name}):
        raise HTTPException(status_code=400, detail="Organization name already exists")
    
    coll_name = f"org_{data.organization_name.lower().replace(' ', '_')}"
    DB.create_collection(coll_name)
    
    org_doc = {
        "name": data.organization_name,
        "collection_name": coll_name,
        "admin_email": data.email,
        "admin_password_hash": hash_password(data.password)
    }
    DB.master().insert_one(org_doc)
    
    return {"message": "Organization created successfully", "organization": data.organization_name}

@router.get("/org/get")
def get_organization(organization_name: str):
    org = DB.master().find_one({"name": organization_name})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return {
        "organization_name": org["name"],
        "collection_name": org["collection_name"],
        "admin_email": org["admin_email"]
    }

@router.put("/org/update")
def update_organization(data: OrgUpdate, admin = Depends(current_admin)):
    org = DB.master().find_one({"name": admin["org_name"]})
    if not org or org["admin_email"] != admin["admin_email"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if data.organization_name != org["name"]:
        if DB.master().find_one({"name": data.organization_name}):
            raise HTTPException(status_code=400, detail="New organization name already taken")
        new_coll = f"org_{data.organization_name.lower().replace(' ', '_')}"
        DB.rename(org["collection_name"], new_coll)
    else:
        new_coll = org["collection_name"]
    
    update_data = {
        "name": data.organization_name,
        "collection_name": new_coll,
        "admin_email": data.email,
        "admin_password_hash": hash_password(data.password)
    }
    DB.master().update_one({"_id": org["_id"]}, {"$set": update_data})
    return {"message": "Organization updated successfully"}

@router.delete("/org/delete")
def delete_organization(organization_name: str, admin = Depends(current_admin)):
    if admin["org_name"] != organization_name:
        raise HTTPException(status_code=403, detail="Cannot delete another organization")
    
    org = DB.master().find_one({"name": organization_name})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    DB.drop(org["collection_name"])
    DB.master().delete_one({"_id": org["_id"]})
    return {"message": "Organization and all data deleted successfully"}