from fastapi import APIRouter, Body, HTTPException
from db.config import engine
from models.request_body import RequestBody

router = APIRouter(
    prefix='/api/request_bodies'
)


@router.post("/", responses={
    200: {"content": {
        "application/json": {
            "example": {"key": "YTRkMg=="}
        }}},
    500: {"content": {
        "application/json": {
            "example": {"message": "Error: Нет доступа к БД"}
        }}},
})
async def add_body(body: dict = Body(...)):
    """
    Добавление тела запроса в базу
    """
    req_body = RequestBody(body=body)
    """
    Не нравится реализвация, подумаю как переписать
    """
    req_body_in_db = await engine.find_one(RequestBody, RequestBody.key == req_body.key)
    if req_body_in_db:
        req_body_in_db.duplicates += 1
        await engine.save(req_body_in_db)
    else:
        await engine.save(req_body)
    return {"key": req_body.key}


@router.get("/{key}", responses={
    200: {"content": {
        "application/json": {
            "example": {"body": {"sdf": "sdfff"}, "duplicates": 4}
        }}},
    400: {"content": {
        "application/json": {
            "example": {
                "detail": "Нет записей с данным идентификатором"
            }
        }}},
})
async def get_body(key: str):
    """
    Получение тела запроса в базу
    """
    req_body_in_db = await engine.find_one(RequestBody, RequestBody.key == key)
    if not req_body_in_db:
        raise HTTPException(status_code=400, detail="Нет записей с данным идентификатором")
    return {"body": req_body_in_db.body, "duplicates": req_body_in_db.duplicates}


@router.delete("/{key}", status_code=204, responses={
    400: {"content": {
        "application/json": {
            "example": {
                "detail": "Нет записей с данным идентификатором"
            }
        }}}
})
async def delete_body(key: str):
    """
    Удаление тела запроса
    """
    req_body_in_db = await engine.find_one(RequestBody, RequestBody.key == key)
    if req_body_in_db:
        await engine.delete(req_body_in_db)
    else:
        raise HTTPException(status_code=400, detail="Нет записей с данным идентификатором")
    return None


@router.put("/{key}", responses={
    200: {"content": {
        "application/json": {
            "example": {"key": "YTRkMg=="}
        }}},
    400: {"content": {
        "application/json": {
            "example": {
                "detail": "Нет записей с данным идентификатором"
            }
        }}},
})
async def update_body(key: str, body: dict = Body(...)):
    """
    Изменение тела запроса
    """
    req_body_in_db = await engine.find_one(RequestBody, RequestBody.key == key)
    if req_body_in_db:
        req_body_in_db.body = body
        """
        Хорошо было бы добавить проверку: есть ли в базе запись с новым ключем,
         если есть - то у той записи увеличить число дубликатов на 1, и вернуть ее ключ
        """
        req_body_in_db.duplicates = 1
        await engine.save(req_body_in_db)
    else:
        raise HTTPException(status_code=400, detail="Нет записей с данным идентификатором")
    return {"key": req_body_in_db.key}


@router.get("/statistic", responses={
    200: {"content": {
        "application/json": {
            "example": {"duplicates_percent": "42"}
        }}},
    400: {"content": {
        "application/json": {
            "example": {
                "detail": "Нет записей с данным идентификатором"
            }
        }}},
})
async def get_duplicate_percent():
    """
    Получение % дубликатов от колличества общих запросов.
    """
    entries_count = await engine.count(RequestBody)
    if entries_count:
        duplicates_percent = await engine.count(RequestBody, RequestBody.duplicates != 1) / entries_count * 100
    else:
        raise HTTPException(status_code=422, detail="Нет записей в БД")
    """
    Возможно не верно понял задание
    """
    return {"duplicates_percent": duplicates_percent}
