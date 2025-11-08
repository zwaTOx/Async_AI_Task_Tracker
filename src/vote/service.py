from sqlalchemy.ext.asyncio.session import AsyncSession
from src.idea.repository import IdeaRepository
from src.theme.repository import ThemeRepository
from src.exceptions import NotFoundException, BadRequestException, PermissionException
from .repository import VoteRepository

class VoteService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def vote(self, user_id: int, theme_id: int, idea_id: int):
        theme = await ThemeRepository(self.session).get(theme_id)
        if theme.stage != "Vote":
            raise BadRequestException("Стадия голосования ещё не наступила")
        existing_vote = await VoteRepository(self.session).get_all(user_id=user_id, idea_id=idea_id)
        if existing_vote:
            raise NotFoundException("Вы уже проголосовали за эту идею")
        user_votes = await VoteRepository(self.session).get_all(theme_id=theme_id, user_id=user_id)
        print(len(user_votes), theme.max_voices)
        if len(user_votes) >= theme.max_voices:
            raise BadRequestException("Достигнуто максимальное число голосов")
        idea = await IdeaRepository(self.session).get(idea_id)
        if not idea or idea.theme_id != theme_id:
            raise NotFoundException("Идея не найдена в теме")
        vote = await VoteRepository(self.session).create_vote(user_id=user_id, theme_id=theme_id, idea_id=idea_id)
        return vote

    async def unvote(self, user_id: int, theme_id, idea_id: int):
        theme = await ThemeRepository(self.session).get(theme_id)
        if theme.stage != "Vote":
            raise BadRequestException("Стадия голосования уже закончилась")
        idea = await IdeaRepository(self.session).get(idea_id)
        if not idea or idea.theme_id != theme_id:
            raise NotFoundException("Идея не найдена в теме")
        vote = await VoteRepository(self.session).get_vote(user_id, idea_id)
        if not vote:
            raise BadRequestException("Голоса не найдено в идее")
        await VoteRepository(self.session).delete(vote.id)