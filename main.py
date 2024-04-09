import asyncio
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from anchorpy import Program, Provider, Wallet

from program_id import PROGRAM_ID


async def main():
    client = AsyncClient("https://api.devnet.solana.com")
    provider = Provider(client, Wallet.local())
    program = await Program.at(
        PROGRAM_ID, provider
    )
    # result = program.idl.instructions
    result = await program.rpc['hello']()
    print(result.to_json())
    print(result.default())
    print(result)
    await program.close()


asyncio.run(main())
