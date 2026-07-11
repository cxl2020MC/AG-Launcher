import json
import asyncio
import aiohttp
from compression import zstd
from pathlib import Path

with open("./logs/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

async def main():
    async with aiohttp.ClientSession() as session:
        for chunk_info in data["chunks"]:
            print(f"正在下载 file chunk {chunk_info['file']}...")
            for chunk in chunk_info["chunks"]:
                print(f"正在下载 chunk {chunk['id']}...")
                async with session.get(f"https://autopatchcn.juequling.com/pclauncher/chunks/cxi9diu5aadc/20260414/2.8.0/EyZoSq5h5dpT/{chunk["id"]}") as response:
                    if response.status == 200:
                        content = await response.read()
                        path = Path(f"./logs/chunks/{chunk['id']}")
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(content)
                        print(f"chunk {chunk['id']} 下载完成")
                        with zstd.ZstdFile(f"./logs/chunks/{chunk['id']}", "rb") as f:
                            decompressed_content = f.read()
                            decompressed_path = Path(f"./logs/chunks/{chunk['id']}.decompressed")
                            decompressed_path.parent.mkdir(parents=True, exist_ok=True)
                            decompressed_path.write_bytes(decompressed_content)
                        print(f"chunk {chunk['id']} 解压完成")
                        path = Path(f"./logs/{chunk_info['file']}")
                        path.parent.mkdir(parents=True, exist_ok=True)
                        with path.open("ab") as f:
                            print(f"正在写入 {chunk_info['file']} 的 chunk {chunk['id']} {chunk.get("offset", 0)}")
                            f.seek(int(chunk.get("offset", 0)))
                            with open(f"./logs/chunks/{chunk['id']}.decompressed", "rb") as chunk_file:
                                f.write(chunk_file.read())

                    else:
                        print(f"chunk {chunk['id']} 下载失败，状态码: {response.status}")


if __name__ == "__main__":
    asyncio.run(main())