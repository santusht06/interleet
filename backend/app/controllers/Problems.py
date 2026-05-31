from fastapi import HTTPException
from slugify import slugify
from datetime import datetime
from uuid import UUID

from app.models.problems import ProblemModel
from app.core.db import get_db

db = get_db()


def serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


class ProblemController:
    @staticmethod
    async def create_problem(problem: ProblemModel):
        slug = slugify(problem.title)
        if await db.problems.find_one({"slug": slug}):
            raise HTTPException(400, "Problem with this slug already exists")

        now = datetime.utcnow()
        problem.slug = slug
        problem.created_at = problem.updated_at = now

        await db.problems.insert_one(problem.model_dump())
        return {"success": True, "problem_id": str(problem.problem_id), "slug": slug}

    @staticmethod
    async def get_problem_by_slug(slug: str):
        problem = await db.problems.find_one({"slug": slug, "is_active": True})
        if not problem:
            raise HTTPException(404, "Problem not found")
        return {"success": True, "problem": serialize(problem)}

    @staticmethod
    async def get_all_problems():
        problems = [serialize(p) async for p in db.problems.find({"is_active": True})]
        return {"success": True, "count": len(problems), "problems": problems}

    @staticmethod
    async def update_problem(problem_id: UUID, updates: dict):
        updates.pop("problem_id", None)
        updates.pop("created_at", None)

        if "title" in updates:
            slug = slugify(updates["title"])
            if await db.problems.find_one(
                {"slug": slug, "problem_id": {"$ne": str(problem_id)}}
            ):
                raise HTTPException(400, "Problem with this slug already exists")
            updates["slug"] = slug

        updates["updated_at"] = datetime.utcnow()

        result = await db.problems.find_one_and_update(
            {"problem_id": str(problem_id)},
            {"$set": updates},
            return_document=True,
        )
        if not result:
            raise HTTPException(404, "Problem not found")
        return {"success": True, "problem": serialize(result)}

    @staticmethod
    async def delete_problem(problem_id: UUID, hard: bool = False):
        if hard:
            result = await db.problems.delete_one({"problem_id": str(problem_id)})
            if result.deleted_count == 0:
                raise HTTPException(404, "Problem not found")
            return {"success": True, "deleted": True}

        result = await db.problems.find_one_and_update(
            {"problem_id": str(problem_id)},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}},
            return_document=True,
        )
        if not result:
            raise HTTPException(404, "Problem not found")
        return {"success": True, "archived": True}

    @staticmethod
    async def get_problems_by_user(user_id: str):
        user = await db.users.find_one({"user_id": user_id}, {"solved_problems": 1})
        if not user:
            raise HTTPException(404, "User not found")

        solved_slugs = user.get("solved_problems", [])
        if not solved_slugs:
            return {"success": True, "count": 0, "problems": []}

        problems = [
            serialize(p)
            async for p in db.problems.find(
                {"slug": {"$in": solved_slugs}, "is_active": True}
            )
        ]
        return {"success": True, "count": len(problems), "problems": problems}
