from fastapi import APIRouter
# Prvi poskus strukturiranja tovrstnih datotek.
# TODO: Odlocimo se za anglescino ali slovenscino :)
# TODO: ... in za camelCase ali underscore_case
router = APIRouter(
    prefix="/uporabniki",
    tags=["uporabniki"]
)

@router.get("/")
async def read_users():
    # TODO: Vrni seznam vseh uporabnikov.
    return None

@router.get("/{uporabnik}")
async def read_user(uporabnik: str):
    # TODO: Vrni podatke o uporabniku "uporabnik".
    return None

@router.post("/createUser")
async def create_user(uporabnik: str):
    # TODO: Ustvari uporabnika "uporabnik".
    return None

@router.delete("/deleteUser")
async def delete_user(uporabnik: str):
    # TODO: Izbriši uporabnika "uporabnik".
    return None
