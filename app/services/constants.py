
FORMAT = "%Y/%m/%d %H:%M:%S"

SPREADSHEET_DRAFT = {
    'properties': {
        'title': f'Отчет на ',
        'locale': 'ru_RU'
    },
    'sheets': [{
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': '',
            'gridProperties': {
                'rowCount': 0,
                'columnCount': 0
            }
        }
    }]
}
TABLE_VALUES_DRAFT = [
    ['Отчет от', ],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
