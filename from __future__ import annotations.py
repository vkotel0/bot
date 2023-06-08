from __future__ import annotations
import asyncio, aiohttp



def get_link_of_igames(answer: list[dict[str, int | str]]) -> list[str]:
    result = []


    for i in range(len(answer)):
        result.append(answer[i]["url"])
        return result


async def request():
    link = "https://api.thecatapi.com/v1/images/search?limit=10"

    session = await aiohttp.ClientSession()
    answer = await response.json()


    for link in get_links(answer):
        response = await