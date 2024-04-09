from pathlib import Path
import asyncio
import json
from solders.pubkey import Pubkey
from anchorpy import Idl, Program

from program_id import PROGRAM_ID


async def main():
    # Read the generated IDL.
    with Path("idl.json").open() as f:
        raw_idl = f.read()
    idl = Idl.from_json(raw_idl)
    # Generate the program client from IDL.
    async with Program(idl, PROGRAM_ID) as program:
        # Execute the RPC.
        await program.rpc["hello"]()
    # If we don't use the context manager, we need to
    # close the underlying http client, otherwise we get warnings.
    await program.close()


asyncio.run(main())
