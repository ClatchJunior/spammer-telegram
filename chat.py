import asyncio
from telethon import TelegramClient
import telethon
import time
import configparser


async def main():
    
    config = configparser.ConfigParser()
    config.read('config.ini')

    api_id = config.getint('DEFAULT', 'api_id')
    api_hash = config.get('DEFAULT', 'api_hash')
    delay = config.getint('DEFAULT', 'timing') * 60
    client = TelegramClient("mywe", api_id, api_hash)

    # Конектимся
    await client.start()

    chat_id = config.getint('DEFAULT', 'chat_id')
    message = await client.get_messages(chat_id, limit=1)
    message_text = message[0]
    
    ### message = read_json_file("acc.json") ##здесь вставляем путь к файлу json в котром прописываем сообщение которое будет отправляться


    while True:
        dialogs = await client.get_dialogs()
        # Перебираем чаты и отправляем сообщение каждому из них
        for dialog in dialogs:
            if dialog.is_group or dialog.is_channel:
                try:
                    await client.forward_messages(dialog.entity, message_text)
                    print('Спам начался')
                except telethon.errors.UserBannedInChannelError:
                    pass        
                except telethon.errors.SlowModeWaitError:
                    pass    
                except telethon.errors.ChatAdminRequiredError:
                    pass
                except telethon.errors.FloodWaitError:
                    pass
                except telethon.errors.ChatWriteForbiddenError:
                    pass
        next_launch = time.time() + delay
        while time.time() < next_launch:
            await asyncio.sleep(60)
            time_left = int(next_launch - time.time())
            print(f'Время до следуещего спама: {time_left // 60} минутки {time_left % 60} секундочки')



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
