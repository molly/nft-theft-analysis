# nft-theft-analysis

Get details on an NFT theft incident.

## Usage
`python analyze.py`

### Arguments
#### Required
* `-thief` OR `-victim` (one or the other is required): ETH wallet address of the thief or the victim

#### Optional
* `-start`: Timestamp of the earliest theft (any Etherscan format like `Jun-04-2022 03:52:45 AM +UTC` or `2022-06-04 3:52:45` will work)
* `-end`: Timestamp of the last theft
