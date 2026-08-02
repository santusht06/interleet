# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import APIRouter, Body, Depends

from app.controllers.ai_assist import AiAssistController
from app.middleware.user import Middleware as UserMiddleware

router = APIRouter(prefix="/api/ai", tags=["AI Assist"])


@router.post("/hint")
async def get_hint(payload: dict = Body(...), user_auth=Depends(UserMiddleware.me)):
    user_id = user_auth["user"]["user_id"]
    return await AiAssistController.hint(
        user_id=user_id,
        problem_slug=payload.get("problem_slug", ""),
        code=payload.get("code", ""),
        language=payload.get("language", ""),
    )


@router.post("/review")
async def get_review(payload: dict = Body(...), user_auth=Depends(UserMiddleware.me)):
    user_id = user_auth["user"]["user_id"]
    return await AiAssistController.review(
        user_id=user_id,
        problem_slug=payload.get("problem_slug", ""),
        code=payload.get("code", ""),
        language=payload.get("language", ""),
        stderr=payload.get("stderr"),
    )
