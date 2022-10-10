import copy
from datetime import datetime
from typing import List, Union

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.schemas.charity_project import CharityProjectDB


async def spreadsheets_create(wrapper_services: Aiogoogle, spreadsheet_body_draft: Union[dict, None], format_const: str) -> str:
	now_date_time = datetime.now().strftime(format_const)
	service = await wrapper_services.discover('sheets', 'v4')
	spreadsheet_body = copy.deepcopy(spreadsheet_body_draft)
	spreadsheet_body['properties']['title'] += now_date_time
	spreadsheet_body['sheets'][0]['properties']['title'] = 'Лист1'
	spreadsheet_body['sheets'][0]['properties']['gridProperties']['rowCount'] = 100
	spreadsheet_body['sheets'][0]['properties']['gridProperties']['columnCount'] = 11

	response = await wrapper_services.as_service_account(
		service.spreadsheets.create(json = spreadsheet_body)
	)

	spreadsheetid = response.get('spreadsheetId')
	return spreadsheetid


async def set_user_permissions(
		spreadsheetid: str,
		wrapper_services: Aiogoogle
) -> Union[str, None]:
	permissions_body = {
		'type': 'user',
		'role': 'writer',
		'emailAddress': settings.email
	}
	try:
		service = await wrapper_services.discover('drive', 'v3')
		await wrapper_services.as_service_account(
			service.permissions.create(
				fileId = spreadsheetid,
				json = permissions_body,
				fields = "id"
			))
	except Exception as e:
		return f'Ошибка при отправке в гугл таблицу: {e}'


async def spreadsheets_update_value(
		spreadsheetid: str,
		projects: List[CharityProjectDB],
		wrapper_services: Aiogoogle,
		table_values_draft: list,
		format_const: str
):
	now_date_time = datetime.now().strftime(format_const)
	service = await wrapper_services.discover('sheets', 'v4')
	table_values = table_values_draft.copy()
	table_values[0].append(now_date_time)

	projects = sorted(((project.name, str(project.close_date - project.create_date), project.description) for project in projects), key = lambda x: x[1])
	table_values.extend(projects)

	update_body = {
		'majorDimension': 'ROWS',
		'values': table_values,
	}
	try:
		response = await wrapper_services.as_service_account(
			service.spreadsheets.values.update(
				spreadsheetId = spreadsheetid,
				range = f'A1:C{len(table_values)}',
				valueInputOption = 'USER_ENTERED',
				json = update_body
			)
		)
	except Exception as e:
		return f'Ошибка при отправке в гугл таблицу {e}'
	else:
		return response
