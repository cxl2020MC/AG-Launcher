from niquests import AsyncSession


session = AsyncSession(happy_eyeballs=True)


async def close():
    return await session.close()