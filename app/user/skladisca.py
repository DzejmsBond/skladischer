from fastapi import APIRouter

router = APIRouter(
    prefix="/skladisca",
    tags=["skladisca"]
)

@router.get("/")
async def read_storages():
    # TODO: Vrni seznam vseh tvojih skladišč.
    return None

@router.get("/{skladisce}")
async def get_storage(skladisce: str):
    # TODO: Vrni podatke o skladišču "skladisce".
    return None

@router.post("/createStorage")
async def create_storage(skladisce: str):
    # TODO: Ustvari skladišče "skladisce".
    return None

@router.delete("/deleteStorage")
async def delete_storage(skladisce: str):
    # TODO: Izbriši skladišče "skladisce".
    return None

@router.post("/renameStorage")
async def rename_storage(skladisce: str, ime: str):
    # TODO: Preimenuj skladišče "skladisce" v "ime".
    return None

@router.post("/moveStorage")
async def move_storage(src: str, dest: str):
    # TODO: Premakni vse izdelke iz skladišča "src" v skladišče "dest".
    return None