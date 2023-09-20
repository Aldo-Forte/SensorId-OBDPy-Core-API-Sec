from fastapi import Header, HTTPException

_header_token = "74YWejRl6OZ=uVc7jZiC-vsZTQvHJ6MRlv5e559XwXvpXILXV7z7pFN1L8uCuTz3"

# va nell'header
async def get_token_header(x_token: str = Header()):
    if x_token != _header_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")

# Va nella querystring come parametro
# async def get_query_token(token: str):
#     if token != _token:
#         raise HTTPException(status_code=400, detail="No sensorid token provided")
