from fastapi import APIRouter, HTTPException
from services.cluster import get_cluster_label

router = APIRouter()

@router.get('/get')
async def get_cluster(q: str):
    if not q.strip():
        return HTTPException(status_code=400, detail="text is empty")
    
    try:
        result = await get_cluster_label(q)

        if result is None:
            return HTTPException(status_code=404, detail="Not Found")
        
        return result
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="Internel Server Error")

