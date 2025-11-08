from sqlalchemy import select
from src.repository import SQLAlchemyRepository
from .models import Vote

class VoteRepository(SQLAlchemyRepository):
    model = Vote

    async def get_vote(self, user_id: int, idea_id: int) -> Vote:
        statement = (
            select(Vote)
            .where(
                Vote.user_id == user_id,
                Vote.idea_id == idea_id
            )
        )
        result = await self.session.exec(statement)
        return result.scalar_one_or_none()

    async def create_vote(self, user_id: int, theme_id: int, idea_id: int):
        vote = Vote(user_id=user_id, idea_id=idea_id, theme_id=theme_id)
        self.session.add(vote)
        await self.session.commit()
        await self.session.refresh(vote)
        return vote