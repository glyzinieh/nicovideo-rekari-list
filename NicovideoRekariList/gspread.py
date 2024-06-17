import gspread
from google.oauth2.service_account import Credentials


# シートからデータを取得する際に、辞書型で取得できるようにする
def get_all_values_to_dicts(self) -> list[dict]:
    dicts_data = list()
    lists_data = self.get_all_values()
    header = lists_data[0]
    body = lists_data[1:]
    for i in body:
        dicts_data.append(dict(zip(header, i)))
    return dicts_data


setattr(gspread.Worksheet, "get_all_values_to_dicts", get_all_values_to_dicts)

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

credentials = Credentials.from_service_account_file("credentials.json", scopes=scopes)

gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1IIXr6q8NEUQJfAR7uvQj9YADcIfSIJoGsjdbNK0gvCM/"
)

setting_worksheet = spreadsheet.worksheet("設定")
list_worksheet = spreadsheet.worksheet("動画一覧")

YEAR = setting_worksheet.acell("B1").value


def get_rekari_list():
    videos = [i for i in list_worksheet.get_all_values_to_dicts() if i["年"] == YEAR]
    return videos


def get_id_list():
    ids = [i["ID"] for i in list_worksheet.get_all_values_to_dicts()]
    return ids


def get_video_info(id):
    video = [i for i in list_worksheet.get_all_values_to_dicts() if i["ID"] == id]
    return video[0] if video else None


def record_post(id, title):
    list_worksheet.append_row([id, title, "", "", "", "", "", "", "", YEAR])
    return True
