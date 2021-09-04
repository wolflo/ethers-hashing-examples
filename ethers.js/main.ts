import { ethers, BigNumber, utils } from "ethers";
import "ethers";
import { expect } from 'chai';

const UNISWAP_V2_USDC_ETH_PAIR = "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc";
const UNISWAP_V3_USDC_ETH_PAIR = "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640";
const UNISWAP_V3_POOL_INIT_CODE_HASH = "0xe34f199b19b2b4f47f68442619d555527d244f78a3297ea89325f843f87b8b54"

function get_uniswap_v3_pair(factory: string, token0: string, token1: string, fee: BigNumber): string {
  const salt = utils.keccak256(
    utils.defaultAbiCoder.encode(
      [ "address", "address", "uint24" ],
      [ token0, token1, fee ]
    )
  );

  return utils.getCreate2Address(factory, salt, UNISWAP_V3_POOL_INIT_CODE_HASH);
}

function get_uniswap_v2_permit_hash(owner: string, spender: string, value: BigNumber, nonce: BigNumber, deadline: BigNumber): string {
  const domain = {
   name: "Uniswap V2",
   version: "1",
   chainId: 1,
   verifyingContract: UNISWAP_V2_USDC_ETH_PAIR
  };
  const types = {
     Permit: [
          {name: "owner", type: "address"},
          {name: "spender", type: "address"},
          {name: "value", type: "uint256"},
          {name: "nonce", type: "uint256"},
          {name: "deadline", type: "uint256"},
      ],
  };
  const values = {
      owner: owner,
      spender: spender,
      value: value,
      nonce: nonce,
      deadline: deadline
  };

  return ethers.utils._TypedDataEncoder.hash(domain, types, values);
}

describe("ether.js", () => {
  it("Generates UniswapV3 Pair address", () => {
    const factory = "0x1F98431c8aD98523631AE4a59f267346ea31F984";
    const token0 = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48";
    const token1 = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    const fee = BigNumber.from(500);
    const pair = get_uniswap_v3_pair(factory, token0, token1, fee)
    expect(pair).eq(UNISWAP_V3_USDC_ETH_PAIR);
  });

  it("Generates UniswapV2 permit hash", () => {
    const owner = "0x617072Cb2a1897192A9d301AC53fC541d35c4d9D";
    const spender = "0x2819c144D5946404C0516B6f817a960dB37D4929";
    const value = utils.parseEther("10");
    const nonce = BigNumber.from("1");
    const deadline = BigNumber.from("3133728498");

    const digest = get_uniswap_v2_permit_hash(owner, spender, value, nonce, deadline);

    const expected = "0x7b90248477de48c0b971e0af8951a55974733455191480e1e117c86cc2a6cd03";
    expect(digest).eq(expected);
  });
});
