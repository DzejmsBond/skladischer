from fastapi import APIRouter

router = APIRouter(
    prefix="/qr_kode",
    tags=["qr_kode"]
)

@router.get("/")
async def acquire_qr(data: str):
    #TODO: Ustvari QR kodo za podatek "data".
    return None