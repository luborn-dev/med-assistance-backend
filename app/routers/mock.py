from fastapi import APIRouter

router = APIRouter()


@router.get("/mock")
async def mock_api():
    return [{"username": "johndoe"}, {"username": "janedoe"}]
