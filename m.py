from fastapi import FastAPI
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solders.account import Account
from solders.instruction import Instruction, AccountMeta
from solders.system_program import SystemProgram
from solders.keypair import Keypair  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solana.rpc.types import TxOpts

import json
import asyncio

app = FastAPI()

# 假设的智能合约Program ID和用户私钥
PROGRAM_ID = Pubkey.from_string("Bg63DE1tPqqPYa29h3sX4k9vBJaJ7kBS7wptehxVf4E6")

# MAIN_SECRET_KEY = [104,85,176,13,203,129,211,179,58,101,204,64,198,223,98,200,16,157,252,165,86,200,196,13,189,242,13,141,24,9,221,137,172,79,170,40,69,208,55,36,114,178,189,55,184,169,218,237,155,191,236,113,37,147,77,6,110,97,139,38,106,174,73,83]
MAIN_SECRET_KEY = [196, 75, 188, 197, 140, 189, 165, 32, 122, 21, 183, 95, 250, 61, 252, 173, 19, 161, 54, 145, 158,
                   123, 141, 182, 75, 201, 4, 140, 149, 240, 65, 139, 60, 78, 105, 176, 183, 201, 222, 245, 64, 69, 131,
                   157, 203, 228, 39, 140, 250, 211, 91, 186, 216, 180, 140, 151, 6, 151, 65, 215, 162, 46, 174, 138]
# 2JVqELzPJFPkFXSmbbxNJtGVq4vryZoWrkFXJ5kNvppG
# 后台的私钥创建一个Keypair对象
main_keypair = Keypair.from_bytes(bytes(MAIN_SECRET_KEY))

HELLO_WORLD_PROGRAM_ID = Pubkey.from_string("Bg63DE1tPqqPYa29h3sX4k9vBJaJ7kBS7wptehxVf4E6")

print(main_keypair.pubkey())

kamino_pubkey = Pubkey.from_string("HU4W3Ra2UMCsBGXRdveHQeLNVtPbNGLBDkvbAhVDEwXr")


# print(Pubkey.default())

@app.get("/")
async def call_contract():
    # 创建一个AsyncClient实例
    async with AsyncClient("https://api.devnet.solana.com") as client:
        # 获取最近的区块哈希，它是交易的一部分
        recent_blockhash = await client.get_latest_blockhash()
        # 构建一个交易，假设是向某个地址转账
        transaction = Transaction()
        transaction.add(
            transfer(
                TransferParams(
                    from_pubkey=Pubkey.from_string("54Qp1psDvG2jZawiwRafpRQThR5HScqLhmoSXJvi3xt1"),
                    to_pubkey=kamino_pubkey,
                    lamports=10
                )
            )
        )

        # 签名并发送交易
        transaction.sign(main_keypair)
        response = await client.send_transaction(transaction, main_keypair,
                                                 opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed))

        # 返回交易的结果
        # print(response.from_bytes())
        return {"response": json.loads(response.to_json())}
        # return "123"


# 创建一个交易，调用"Hello World"程序的"get_greeting"方法
@app.get("/hello")
async def call_hello_world_program():
    # 创建一个AsyncClient实例
    async with AsyncClient("https://api.devnet.solana.com") as client:
        # 创建一个空账户，用于接收程序返回的数据
        account = Account()

        # 构建交易
        transaction = Transaction()
        instruction_data = bytes([1])
        accounts = [AccountMeta(main_keypair.pubkey(), is_signer=True, is_writable=True),
                    AccountMeta(kamino_pubkey, is_signer=False, is_writable=True), ]
        instruction = Instruction(HELLO_WORLD_PROGRAM_ID, instruction_data, accounts)

        transaction.add(instruction)

        # 签名并发送交易
        transaction.sign(main_keypair)
        response = await client.send_transaction(transaction, main_keypair)

        # 处理响应
        if response:
            # 假设返回的数据是字符串
            # greeting = response["result"]
            print("Received greeting from 'Hello World' program:", response)
        else:
            print("Failed to call 'Hello World' program.")
        return "succ"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=9111)
