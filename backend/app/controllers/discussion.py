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

from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException

from app.core.db import get_db

db = get_db()


class DiscussionController:
    """Per-problem discussion threads + solved-gated editorials."""

    @staticmethod
    def _public(doc: dict) -> dict:
        doc.pop("_id", None)
        doc.pop("upvoters", None)  # don't leak who upvoted
        created = doc.get("created_at")
        if isinstance(created, datetime):
            doc["created_at"] = created.isoformat()
        return doc

    @staticmethod
    async def list_for_problem(slug: str):
        cursor = db.discussions.find({"problem_slug": slug}).sort("created_at", -1)
        items = [DiscussionController._public(d) async for d in cursor]
        return {"success": True, "discussions": items}

    @staticmethod
    async def create(user: dict, slug: str, content: str):
        content = (content or "").strip()
        if not content:
            raise HTTPException(status_code=400, detail="Comment cannot be empty.")
        if len(content) > 5000:
            raise HTTPException(status_code=400, detail="Comment is too long (max 5000 characters).")

        doc = {
            "id": str(uuid4()),
            "problem_slug": slug,
            "user_id": user.get("user_id"),
            "username": user.get("username") or user.get("full_name") or "Anonymous",
            "content": content,
            "upvotes": 0,
            "upvoters": [],
            "created_at": datetime.utcnow(),
        }
        await db.discussions.insert_one(doc)
        return {"success": True, "discussion": DiscussionController._public(dict(doc))}

    @staticmethod
    async def upvote(user_id: str, discussion_id: str):
        disc = await db.discussions.find_one({"id": discussion_id})
        if not disc:
            raise HTTPException(status_code=404, detail="Discussion not found.")

        upvoters = list(disc.get("upvoters", []) or [])
        if user_id in upvoters:
            upvoters.remove(user_id)
            upvoted = False
        else:
            upvoters.append(user_id)
            upvoted = True

        await db.discussions.update_one(
            {"id": discussion_id},
            {"$set": {"upvoters": upvoters, "upvotes": len(upvoters)}},
        )
        return {"success": True, "upvotes": len(upvoters), "upvoted": upvoted}

    @staticmethod
    async def _has_solved(user: dict, slug: str) -> bool:
        if slug in (user.get("solved_problems") or []):
            return True
        count = await db.submissions.count_documents(
            {"user_id": user.get("user_id"), "problem_slug": slug, "status": "accepted"}
        )
        return count > 0

    @staticmethod
    async def editorial(user: dict, slug: str):
        if not await DiscussionController._has_solved(user, slug):
            raise HTTPException(
                status_code=403,
                detail="Solve this problem to unlock the editorial.",
            )

        ref = await db.reference_solutions.find_one({"challenge_slug": slug, "is_primary": True})
        if not ref:
            ref = await db.reference_solutions.find_one({"challenge_slug": slug})
        if not ref:
            raise HTTPException(status_code=404, detail="No editorial is available for this problem yet.")

        return {
            "success": True,
            "editorial": {
                "language": ref.get("language", ""),
                "code": ref.get("code", ""),
                "description": ref.get("description") or "",
            },
        }
