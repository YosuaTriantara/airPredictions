from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success(data=None, message="Success", status_code=200):

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(
            {
                "success": True,
                "message": message,
                "data": data
            }
        )
    )


def error(message, status_code=400):

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message
        }
    )