import copy
from datetime import datetime
from typing import List, Optional

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.schemas.charity_project import CharityProjectDB
from app.services.constants import (SPREADSHEET_DRAFT,
                                    SPREADSHEET_ROWCOUNT_DRAFT,
                                    SPREADSHEET_COLUMNCOUNT_DRAFT,
                                    TABLE_VALUES_DRAFT)


async def spreadsheets_create(wrapper_services: Aiogoogle,
                              spreadsheet_body_draft:
                              Optional[dict] = None,) -> str:
    now_date_time = datetime.now().strftime(str)
    service = await wrapper_services.discover('sheets', 'v4')
    if spreadsheet_body_draft is None:
        spreadsheet_body_draft = SPREADSHEET_DRAFT
    spreadsheet_body = copy.deepcopy(spreadsheet_body_draft)
    spreadsheet_body['properties']['title'] += now_date_time
    spreadsheet_body['sheets'][0]['properties']['title'] = 'Лист1'

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )

    spreadsheet_id = response.get('spreadsheetId')
    return spreadsheet_id


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }

    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
    spreadsheetid: str,
    projects: List[CharityProjectDB],
    wrapper_services: Aiogoogle,
    table_values_draft: Optional[list] = None,

):
    now_date_time = datetime.now().strftime(str)
    service = await wrapper_services.discover('sheets', 'v4')

    if table_values_draft is None:
        table_values_draft = TABLE_VALUES_DRAFT
    table_values = copy.deepcopy(table_values_draft)
    table_values[0].append(now_date_time)

    projects = sorted(((project.name,
                        str(project.close_date - project.create_date),
                        project.description) for project in projects),
                      key=lambda x: x[1])
    table_values.extend(projects)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values,
    }

    columns_value = max([len(items_to_count)
                         for items_to_count in table_values])
    rows_value = len(table_values)

    if (SPREADSHEET_ROWCOUNT_DRAFT >= rows_value and
            SPREADSHEET_COLUMNCOUNT_DRAFT >= columns_value):
        response = await wrapper_services.as_service_account(
            service.spreadsheets.values.update(
                spreadsheetId=spreadsheetid,
                range=f'R1C1:R{rows_value}C{columns_value}',
                valueInputOption='USER_ENTERED',
                json=update_body
            )
        )
        return response
    else:
        return
