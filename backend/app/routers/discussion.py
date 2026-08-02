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

from app.controllers.discussion import DiscussionController
from app.middleware.user import Middleware as UserMiddleware

router = APIRouter(prefix="/api", tags=["Discussions"])


@router.get("/challenges/{slug}/discussions")
async def list_discussions(slug: str):
    return await DiscussionController.list_for_problem(slug)


@router.post("/challenges/{slug}/discussions")
async def create_discussion(
    slug: str,
    payload: dict = Body(...),
    user_auth=Depends(UserMiddleware.me),
):
    return await DiscussionController.create(user_auth["user"], slug, payload.get("content", ""))


@router.post("/discussions/{discussion_id}/upvote")
async def upvote_discussion(discussion_id: str, user_auth=Depends(UserMiddleware.me)):
    return await DiscussionController.upvote(user_auth["user"]["user_id"], discussion_id)


@router.get("/challenges/{slug}/editorial")
async def get_editorial(slug: str, user_auth=Depends(UserMiddleware.me)):
    return await DiscussionController.editorial(user_auth["user"], slug)
