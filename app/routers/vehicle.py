from fastapi import APIRouter, Depends
from dependencies import get_token_header
from models.consumption import Consumption
from models.data_request import DataRequest
from models.trip import Trip
from idp import OIDCUser, idp
from models.data_request import PidValueRequest

router = APIRouter(
    prefix="/vehicle",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.get("/km")
async def trip(data_request: DataRequest, user: OIDCUser = Depends(idp.get_current_user())):
    trip = Trip()
    total_km = trip.get_distance(data_request)
    return {"device": data_request.device, "kms": total_km }


@router.get("/consumption")
async def trip(data_request: DataRequest, user: OIDCUser = Depends(idp.get_current_user())):
    try:
        consumption = Consumption()
        trip_consumption = consumption.get_consumption(data_request)
        print(f"{trip_consumption=}")
        return {"device": data_request.device, "consumption": trip_consumption}
    except Exception as ex:
        return {"device": data_request.device, "error": str(ex)}
