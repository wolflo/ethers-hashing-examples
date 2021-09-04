import pytest
from web3 import Web3 as web3
from eth_abi import encode_abi
from eth_account.messages import encode_structured_data

UNISWAP_V3_POOL_INIT_CODE_HASH = "0xe34f199b19b2b4f47f68442619d555527d244f78a3297ea89325f843f87b8b54"

def get_uniswap_v3_pair(factory, token0, token1, fee):
    salt_input = encode_abi(
        [ 'address', 'address', 'uint256'],
        [ web3.toChecksumAddress(token0), web3.toChecksumAddress(token1), fee ]
    )
    salt = web3.keccak(salt_input)
    create2_hash = web3.solidityKeccak(
        [ 'bytes1', 'address', 'bytes32', 'bytes32' ],
        [ "0xff", factory, salt, UNISWAP_V3_POOL_INIT_CODE_HASH ]
    )
    return web3.toChecksumAddress(create2_hash[12:].hex())

# from https://github.com/yearn/yearn-vaults/blob/95a87334762e5ed68a031a63a69c8cfc6ec03a07/tests/conftest.py#L92
def get_uniswap_v2_permit_hash(verifying_addr, owner, spender, value, nonce, deadline):
    name = "Uniswap V2"
    version = "1"
    chain_id = 1
    data = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Permit": [
                {"name": "owner", "type": "address"},
                {"name": "spender", "type": "address"},
                {"name": "value", "type": "uint256"},
                {"name": "nonce", "type": "uint256"},
                {"name": "deadline", "type": "uint256"},
            ],
        },
        "domain": {
            "name": name,
            "version": version,
            "chainId": chain_id,
            "verifyingContract": verifying_addr,
        },
        "primaryType": "Permit",
        "message": {
            "owner": owner,
            "spender": spender,
            "value": value,
            "nonce": nonce,
            "deadline": deadline,
        },
    }

    msg = encode_structured_data(data)
    digest = web3.keccak(b'\x19\x01' + msg.header + msg.body)
    return digest

def test_uniswap_v3_pair():
    # USDC-WETH
    factory = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
    token0 = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    token1 = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    fee = 500;
    pair = "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"
    assert get_uniswap_v3_pair(factory, token0, token1, fee) == pair

def test_permit_hash():
    owner = "0x617072Cb2a1897192A9d301AC53fC541d35c4d9D"
    spender = "0x2819c144D5946404C0516B6f817a960dB37D4929"
    value = web3.toWei(10, "ether")
    nonce = 1
    deadline = 3133728498
    verifying_addr = "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"

    digest = get_uniswap_v2_permit_hash(verifying_addr, owner, spender, value, nonce, deadline)

    expected = "0x7b90248477de48c0b971e0af8951a55974733455191480e1e117c86cc2a6cd03"
    assert digest.hex() == expected
