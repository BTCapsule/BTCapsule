Introducing the Bitcoin Time Capsule. You don't have to trust a lawyer or other third-party to ensure your family has access to your bitcoin. Create a timelocked wallet on BTCapsule, and when the time comes, your bitcoin will be available to whomever you choose.


<b>How it works</b>


BTCapsule is an open-source program that can timelock your bitcoin to a date of your choosing. You simply generate a P2SH address, add a date, the txid and vout number of your transaction, and the amount of BTC you sent to the address.

This will create several files. You will get two separate paper wallets (sender_wallet.txt and receiver_wallet.txt), and two copies of the QR code for the P2SH address to add additional funds. 

The senders_wallet will contain a redeem script that can be used at any time to get your bitcoin back, just in case you ever change your mind. It also contains the master private key used to create the transactions.

The receiver_wallet will contain a timelocked redeem script that is not redeemable until the date you chose. They will also have their own private key to sweep the wallet.

Just copy the BTCapsule, the redeem_wallet, and a copy of the QR code to a flash drive and give it to your loved one. They will not get the bitcoin until you choose, and if you’re (hopefully) still alive when the timelock expires, just redeem from your sender_wallet and create a new transaction.

When you’re ready to redeem, just visit a blockchain explorer and broadcast the redeem script. Once it’s been confirmed, you can use BTCapsule’s Sweep Wallet feature.

<b>Sweep Wallet</b>

To sweep your wallet, make sure the wallet with your particular redeem script is in the same folder as BTCapsule. Run BTCapsule, enter an address and the amount of BTC you want to redeem (a little less than available if you want to pay miner fees), and it will create a new file called redeem.txt that can be broadcast on a block explorer.

You can download BTCapsule for Windows and learn more at:

https://btcapsule.com/
