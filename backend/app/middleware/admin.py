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

from fastapi import Request, HTTPException
from app.middleware.user import Middleware as UserMiddleware
from app.core.config import ADMIN_EMAILS

class AdminMiddleware:
    @staticmethod
    async def is_admin(request: Request):
        user_auth = await UserMiddleware.me(request)
        user = user_auth.get("user")
        email = (user or {}).get("email", "").strip().lower()
        # Require the admin role, and (when an allowlist is configured) membership in it.
        if not user or user.get("role") != "admin" or (ADMIN_EMAILS and email not in ADMIN_EMAILS):
            raise HTTPException(status_code=403, detail="Access denied. Admin access only.")
        return user
