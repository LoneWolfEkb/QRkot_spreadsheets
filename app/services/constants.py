
FORMAT = "%Y/%m/%d %H:%M:%S"

SPREADSHEET_ROWCOUNT_DRAFT = 100
SPREADSHEET_COLUMNCOUNT_DRAFT = 11

SPREADSHEET_DRAFT = {
    'properties': {
        'title': f'Отчет на ',  # noqa
        'locale': 'ru_RU'
    },
    'sheets': [{
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': '',
            'gridProperties': {
                'rowCount': SPREADSHEET_ROWCOUNT_DRAFT,
                'columnCount': SPREADSHEET_COLUMNCOUNT_DRAFT
            }
        }
    }]
}
TABLE_VALUES_DRAFT = [
    ['Отчет от', ],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
