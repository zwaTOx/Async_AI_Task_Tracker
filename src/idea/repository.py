from typing import Any, Dict
from src.repository import SQLAlchemyRepository
from src.vote.models import Vote
from .models import Idea
from sqlalchemy.orm import selectinload
from sqlalchemy import func, select

class IdeaRepository(SQLAlchemyRepository):
    model=Idea

    async def get_all(self, user_id: int, project_id: int, theme_id: int):
        user_votes_cte = (
            select(Vote.idea_id)
            .where(Vote.user_id == user_id)
            .cte('user_votes')
        )
        
        query = (
            select(
                Idea,
                (Idea.id == user_votes_cte.c.idea_id).label('is_voted')
            )
            .where(Idea.project_id == project_id, Idea.theme_id == theme_id)
            .outerjoin(
                user_votes_cte, 
                Idea.id == user_votes_cte.c.idea_id
            )
            .options(selectinload(Idea.votes))
        )
        
        result = await self.session.execute(query)
        ideas_with_status = result.all()
        ideas = []
        for idea, is_voted in ideas_with_status:
            idea.is_voted = is_voted if is_voted is not None else False
            ideas.append(idea)
        return ideas