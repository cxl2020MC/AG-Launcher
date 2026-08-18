# from niquests import AsyncSession
import niquests

session = niquests.AsyncSession(happy_eyeballs=True)


async def close():
    return await session.close()
