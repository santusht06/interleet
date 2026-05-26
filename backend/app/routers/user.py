from fastapi import APIRouter, Response, Request, Depends
from app.models.users import UserModel as User
from app.models.users import OTPverify

from app.controllers.user import UserController
from app.utils.JWT import check_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/sendOTP")
async def send_otp(
    user: User,
    _: None = Depends(check_token),
):
    return await UserController.send_otp(user)


@router.post("/verify")
async def verify_otp(
    OTP: OTPverify,
    Response: Response,
    Request: Request,
    _: None = Depends(check_token),
):
    return await UserController.verify_otp(OTP, Response, Request)
