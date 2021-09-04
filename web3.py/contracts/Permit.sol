pragma solidity ^0.7.0;

contract Permit {
    bytes32 private constant DOMAIN_SEPARATOR = 0xe8d93546d488d196c53f3e93ad73ba237e3fb527bddca6a240f54d03552dc70f;
    bytes32 private constant PERMIT_TYPEHASH= 0x6e71edae12b1b97f4d1f60370fef10105fa2faae0126114a169c64845d6126c9;

    function digest(address owner, address spender, uint value, uint nonce, uint deadline) public pure returns (bytes32) {
        bytes32 digest = keccak256(
            abi.encodePacked(
                '\x19\x01',
                DOMAIN_SEPARATOR,
                keccak256(abi.encode(PERMIT_TYPEHASH, owner, spender, value, nonce, deadline))
            )
        );
        return digest;
    }

    function verify(address owner, address spender, uint value, uint nonce, uint deadline, uint8 v, bytes32 r, bytes32 s) external view returns (bool) {
        bytes32 digest = digest(owner, spender, value, nonce, deadline);
        address recoveredAddress = ecrecover(digest, v, r, s);
        // require(owner == recoveredAddress, "WrOnG SiGnEr");
        require(recoveredAddress != address(0));
        return owner == recoveredAddress;
    }

}
