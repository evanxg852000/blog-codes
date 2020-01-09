import asyncio

from resp import Client

async def main_client(prompt, evt_loop):
    print(f'{prompt} Welcome to pyRedis')
    running = True
    cl = Client(evt_loop)
    while running:
        #  await asyncio.sleep(1)
        cmd = input(f'{prompt} ')
        if cmd == '.exit':
            running = False
        else:
            try:
                reply = await cl.execute(cmd)
                print(prompt, reply)
            except Exception as e:
                print(prompt, 'errr:', e)
    cl.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main_client('$pyredis>>', loop))
loop.close()

