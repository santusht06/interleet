from fastapi import HTTPException, Response, Request
from datetime import datetime
from uuid import uuid4
import logging
from app.models.users import UserModel as User
from app.models.users import OTPverify as OTP
from app.core.db import get_db
from app.core.config import PROJECT_ENVIRONMENT
from app.utils.OTP import (
    sendOTP,
    VerifyOTPbyUtils,
)
from app.utils.JWT import (
    generate_token,
)
from app.lib.generateOTP import generateOTP


logger = logging.getLogger(__name__)
is_prod = PROJECT_ENVIRONMENT == "PRODUCTION"


db = get_db()


class UserController:
    @staticmethod
    async def send_otp(user: User):
        try:
            if not user.email:
                raise HTTPException(status_code=400, detail="Email is required")

            otp_code = generateOTP()

            otp_response = await sendOTP(user.email, otp_code)

            if not otp_response.get("success"):
                raise HTTPException(status_code=400, detail="Failed to send OTP")

            return {
                "success": True,
                "message": f"OTP sent to {user.email}",
                "transactionID": otp_response.get("transactionID"),
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.exception(f"Send OTP failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    async def verify_otp(payload: OTP, response: Response, request: Request):
        try:
            verify_result = await VerifyOTPbyUtils(payload.transactionID, payload.OTP)

            if not verify_result.get("valid"):
                raise HTTPException(
                    status_code=400, detail=verify_result.get("reason", "Invalid OTP")
                )

            user_email = verify_result.get("email")
            if not user_email:
                raise HTTPException(status_code=400, detail="Email not found")

            existing_user = await db.users.find_one({"email": user_email})

            if not existing_user:
                user_id = str(uuid4())
                new_user = {
                    "user_id": user_id,
                    "email": user_email,
                    "role": "user",
                    "auth_provider": "OTP",
                    "frontend_rating": 0,
                    "backend_rating": 0,
                    "fullstack_rating": 0,
                    "devops_rating": 0,
                    "overall_rating": 0,
                    "solved_problems": [],
                    "badges": [],
                    "streak_count": 0,
                    "is_verified": True,
                    "is_active": True,
                    "is_locked": False,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                    "last_login": datetime.utcnow(),
                }
                await db.users.insert_one(new_user)
                generate_token(user_id, response)

                if request.cookies.get("guest_session"):
                    response.delete_cookie(
                        key="guest_session",
                        httponly=True,
                        samesite="lax",
                        secure=is_prod,
                    )
                return {"success": True, "message": "User created successfully"}

            if existing_user.get("is_locked"):
                raise HTTPException(status_code=403, detail="Account is locked")
            if not existing_user.get("is_active", True):
                raise HTTPException(status_code=403, detail="Account is inactive")

            await db.users.update_one(
                {"email": user_email},
                {
                    "$set": {
                        "is_verified": True,
                        "updated_at": datetime.utcnow(),
                        "last_login": datetime.utcnow(),
                    }
                },
            )

            generate_token(existing_user["user_id"], response)

            if request.cookies.get("guest_session"):
                response.delete_cookie(
                    key="guest_session",
                    httponly=True,
                    samesite="lax",
                    secure=is_prod,
                )
            return {"success": True, "message": "Login successful"}
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(f"Verify OTP failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
