from typing import Optional

from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    @staticmethod
    async def get_project_id_by_name(
            name: str, session: AsyncSession) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == name))
        return db_project_id.scalars().first()

    @staticmethod
    async def get_projects_to_elaborate(session: AsyncSession):
        projects = await session.execute(
            select(CharityProject).
            where(CharityProject.fully_invested == False)  # noqa
            .order_by(CharityProject.create_date))  # noqa
        return projects.scalars().all()


    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession()
    ):
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            ).order_by(
                extract('year', self.model.close_date) -
                extract('year', self.model.create_date),
                extract('month', self.model.close_date) -
                extract('month', self.model.create_date),
                extract('day', self.model.close_date) -
                extract('day', self.model.create_date)
            )
        )
        projects = projects.all()
        return projects


project_crud = CRUDCharityProject(CharityProject)
