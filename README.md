Introducing the Bitcoin Time Capsule. You don't have to trust a lawyer or other third-party to ensure your family has access to your bitcoin. Create a timelocked wallet on BTCapsule, and when the time comes, your bitcoin will be available to whomever you choose.

You can download BTCapsule (testnet) for Windows or Linux and learn more at:

https://btcapsule.com/

BTCapsule creates a P2SH address that is timelocked to 500,000,001 (the earliest timestamp recognized by the Bitcoin network) at the script level. The sender wallet contains a raw transaction that is timelocked to 500,000,001 at the transaction level and allows you, the original holder, to redeem your Bitcoin at any time. The receiver wallet contains a raw transaction that is locked at whatever date you choose, which is then converted to a unix timestamp.


<b>How it works</b>


BTCapsule is an open-source program that can timelock your bitcoin to a date of your choosing. You simply generate a P2SH address, add a date, the txid and vout number of your transaction, and the amount of BTC you sent to the address (minus miner fees).

This will create two folders with several files. You will get two separate paper wallets (sender_wallet.txt and receiver_wallet.txt).

The senders_wallet will contain a redeem script that can be used at any time to get your bitcoin back, just in case you ever change your mind. It also contains the master private key used to create the transactions.

The receiver_wallet will contain a timelocked redeem script that is not redeemable until the date you chose. They will also have their own private key to sweep the wallet.

Just copy the receiver_files folder to a flash drive and give it to your loved one. They will not get the bitcoin until you choose, and if you’re (hopefully) still alive when the timelock expires, just redeem from your sender_wallet and create a new transaction.

When you’re ready to redeem, just visit a blockchain explorer and broadcast the redeem script. Once it’s been confirmed, you can use BTCapsule’s Sweep Wallet feature.

<b>How to build</b>

Install Python 3 with pip

Open cmd (Windows) or terminal (Linux)

Run following commands:

Windows and Linux:

```pip3 install bitcoin-utils pypng pyqrcode Pillow==9.1.0```

Add the following commands, depending on your OS:

Windows:

```pip3 install tk python-dateutil```

Linux:

```sudo apt-get install python3-dateutil python3-tk```

If you would like an executable so your receiver does not need Python, install PyInstaller with ```pip3 install pyinstaller``` and then run ```python3 -m PyInstaller --onefile -w --hidden-import='PIL._tkinter_finder'```

You can then run the executable and create a timelocked wallet, and the executable will be included in the ```receiver_files``` folder.



<b>Sweep Wallet</b>

To sweep your wallet, make sure the wallet with your particular redeem script is in the same folder as BTCapsule. Run BTCapsule, enter an address and the amount of BTC to redeem (a little less than available to pay miner fees), and it will create a new file called redeem.txt that can be broadcast on a block explorer.

