from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import CRUDCharityProject
from app.services.constants import SPREADSHEET_DRAFT, FORMAT, TABLE_VALUES_DRAFT
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
    status_code=status.HTTP_201_CREATED
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await CRUDCharityProject.get_projects_columns_for_completion_rate(
        session
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services,
                                               spreadsheet_body_draft=SPREADSHEET_DRAFT,
                                               format_const=FORMAT)
    if spreadsheet_id is None:
        raise HTTPException(status_code=403,
                            detail="Не удалось создать гугл-таблицу")

    response_user_perm = await set_user_permissions(spreadsheet_id, wrapper_services)

    if response_user_perm:
        raise HTTPException(status_code=403, detail=response_user_perm)

    response = await spreadsheets_update_value(
        spreadsheet_id,
        projects,
        wrapper_services,
        table_values_draft=TABLE_VALUES_DRAFT,
        format_const=FORMAT
    )
    return response
