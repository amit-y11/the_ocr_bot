# Mock database for saving file_path

my_database = {}


'''
{chat_id : {
        message_id_1 : file_path_1,
        message_id_2 : file_path_2,
    }
}
'''

def insert_file_path(chat_id:int, message_id:int, file_path:str) -> None:
    try:
        my_database[chat_id][message_id] = file_path
    except KeyError:
        my_database[chat_id] = {}
        my_database[chat_id][message_id] = file_path

def get_file_path(chat_id:int, message_id:int):
    try:
        file_path = my_database[chat_id][message_id]
        del my_database[chat_id][message_id]
        return file_path
    except KeyError:
        return None
