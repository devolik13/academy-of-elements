# api/building_api.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from database import UserDatabase
from building_manager import BuildingManager

async def api_build(request: Request):
    """
    Endpoint для начала постройки здания через Web App.
    Ожидает JSON с user_id, building_id, cell_index.
    """
    try:
        data = await request.json()
        user_id = data.get("user_id")
        building_id = data.get("building_id")
        cell_index = data.get("cell_index") # cell_index теперь обязателен

        if not all([user_id, building_id, cell_index is not None]): # Проверка на None для cell_index
            raise HTTPException(status_code=400, detail="Missing user_id, building_id, or cell_index")

        # Используем существующую логику из BuildingManager
        success, message = await BuildingManager.start_construction(user_id, building_id, cell_index)
        if success:
            return JSONResponse(content={"success": True, "message": message})
        else:
            # Можно использовать 400 для ошибок логики игры
            raise HTTPException(status_code=400, detail=message)

    except HTTPException:
        # Повторно вызываем, чтобы он был обработан middleware FastAPI
        raise
    except Exception as e:
        print(f"❌ Ошибка в /api/build: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")