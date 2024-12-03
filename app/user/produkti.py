from fastapi import APIRouter

router = APIRouter(
    prefix="/produkti",
    tags=["produkti"]
)

@router.get("/")
async def get_products():
    # TODO: Vrni seznam vseh produktov v tem skladišču.
    return None

@router.post("/addProduct")
async def add_product(produkt: str):
    # TODO: Dodaj produkt "produkt" v skladišče.
    return None

@router.delete("/removeProduct")
async def remove_product(produkt: str, n: int):
    # TODO: Odstrani "n" produktov "produkt" iz skladišča.
    return None

@router.post("/changeAttribute")
async def change_attribute(produkt: str, attribute: str, value: str):
    # TODO: Spremeni atribut "attribute" produkta "produkt" na vrednost "value".
    return None