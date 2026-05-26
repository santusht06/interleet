from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from uuid import uuid4, UUID


class UserModel(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    id: UUID = Field(default_factory=uuid4)
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    role: str = "user"
    frontend_rating: int = 0
    backend_rating: int = 0
    fullstack_rating: int = 0
    devops_rating: int = 0
    overall_rating: int = 0
    solved_problems: List[str] = []
    badges: List[str] = []
    streak_count: int = 0
    is_verified: bool = False
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
