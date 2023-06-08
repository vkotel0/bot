import asyncio 


async def loundary():
    print ("нач")
    await asyncio.sleep(2)
    print("закончили стрику")

async def cooking():
    print ("нач еда")
    await asyncio.sleep(2)
    print("закончили еда")

async def tea():
    print ("нач чай")
    await asyncio.sleep(1)
    print("закончили чай")



async def main():
    tasks = [
    loundary(),
    tea(),
    cooking(),
    ]

    await asyncio.gather(*tasks)



asyncio.run(main())


























