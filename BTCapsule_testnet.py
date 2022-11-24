import os
import os.path
import shutil
from tkinter import *
from os.path import exists
import datetime
import dateutil.parser as dp
import time
from decimal import Decimal
from stat import S_IREAD
from itertools import islice
import threading

import pyqrcode
import png
from pyqrcode import QRCode
from PIL import ImageTk, Image


from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Locktime, Sequence
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey, P2wpkhAddress
from bitcoinutils.script import Script
from bitcoinutils.constants import TYPE_ABSOLUTE_TIMELOCK


root = Tk()
setup("testnet")


def sweep_wallet(wa, t, s, prk, a):

    txin = TxInput(t, 0)

    if wa[0] == "m" or wa[0] == "n":
        addr = P2pkhAddress(wa)
        txout = TxOutput(
            to_satoshis(s),
            Script(
                [
                    "OP_DUP",
                    "OP_HASH160",
                    addr.to_hash160(),
                    "OP_EQUALVERIFY",
                    "OP_CHECKSIG",
                ]
            ),
        )

    if wa[0] == "2":
        addr = P2shAddress(wa)
        txout = TxOutput(
            to_satoshis(s),
            Script(
                [
                    "OP_DUP",
                    "OP_HASH160",
                    addr.to_hash160(),
                    "OP_EQUALVERIFY",
                    "OP_CHECKSIG",
                ]
            ),
        )

    if wa[0] == "t":
        addr = P2wpkhAddress(wa)
        txout = TxOutput(to_satoshis(s), Script([0, addr.to_hash()]))

    tx = Transaction([txin], [txout])

    sk = PrivateKey(prk)

    from_addr = P2pkhAddress(a)

    sig = sk.sign_input(
        tx,
        0,
        Script(
            [
                "OP_DUP",
                "OP_HASH160",
                from_addr.to_hash160(),
                "OP_EQUALVERIFY",
                "OP_CHECKSIG",
            ]
        ),
    )


    tx = Transaction([txin], [txout])

    sk = PrivateKey(prk)

    from_addr = P2pkhAddress(a)

    sig = sk.sign_input(
        tx,
        0,
        Script(
            [
                "OP_DUP",
                "OP_HASH160",
                from_addr.to_hash160(),
                "OP_EQUALVERIFY",
                "OP_CHECKSIG",
            ]
        ),
    )

    pk = sk.get_public_key().to_hex()
    txin.script_sig = Script([sig, pk])
    signed_tx = tx.serialize()

    redeem_file = open("redeem.txt", "w")

    redeem_file.write("Redeem script: " + f"{signed_tx}")

    redeem_file.close()

    os.chmod("redeem.txt", S_IREAD)


def main():

    sender_exists = exists("sender_files/sender_wallet.txt")
    rec_exists = exists("receiver_files/receiver_wallet.txt")
    btc_exists = exists("BTCapsule_testnet.exe")
    btc_py_exists = exists("BTCapsule_testnet.py")
    btc_linux = exists("BTCapsule_testnet")

    seq = Sequence(TYPE_ABSOLUTE_TIMELOCK, 500000001)

    entry_x = 275

    entry_y = 200


    canvas1 = Canvas(root, width=550, height=800, bg="white", highlightthickness=0)

    canvas1.pack()

    canvas1.create_text(
        entry_x, entry_y - 140, fill="black", font="Arial 10 bold", text="CREATE TIMELOCK"
    )

    canvas1.create_text(
        entry_x, entry_y - 95, fill="black", font="Arial 10", text="Generate a P2SH address"
    )

    p2sh = Entry(root, width=42, relief=SOLID)
    canvas1.create_window(entry_x, entry_y - 70, window=p2sh)

    canvas1.create_text(
        entry_x, entry_y - 10, fill="black", font="Arial 10", text="Sender's Wallet"
    )

    canvas1.create_text(75, entry_y + 15, fill="black", font="Arial 10", text="Priv")

    canvas1.create_text(75, entry_y + 45, fill="black", font="Arial 10", text="Addr")

    sk = Entry(root, width=59, relief=SOLID)
    canvas1.create_window(entry_x + 10, entry_y + 15, window=sk)

    sa = Entry(root, width=58, relief=SOLID)
    canvas1.create_window(entry_x + 10, entry_y + 45, window=sa)

    rk = Entry(root, width=42, relief=SOLID)
    canvas1.create_window(entry_x + 475, entry_y + 45, window=rk)

    ra = Entry(root, width=42, relief=SOLID)
    canvas1.create_window(entry_x + 475, entry_y + 75, window=ra)

    rec_create_priv = PrivateKey()
    rec_privk = rec_create_priv.to_wif(compressed=True)

    rec_pub = rec_create_priv.get_public_key()

    rec_address = rec_pub.get_address()

    rec_pubk = rec_address.to_string()

    rk.insert(END, f"{rec_privk}")
    rk.bind("<FocusIn>", lambda args: rk.insert(END, ""))

    ra.insert(END, f"{rec_pubk}")
    ra.bind("<FocusIn>", lambda args: ra.insert(END, ""))

    def generate_wallet():

        sender_create_priv = PrivateKey()
        sender_privk = sender_create_priv.to_wif(compressed=True)

        sender_pub = sender_create_priv.get_public_key()

        sender_address = sender_pub.get_address()

        sender_pubk = sender_address.to_string()

        p2pkh_sk = PrivateKey(sender_privk)

        p2pkh_addr = p2pkh_sk.get_public_key().get_address()

        redeem_script = Script(
            [
                seq.for_script(),
                "OP_CHECKLOCKTIMEVERIFY",
                "OP_DROP",
                "OP_DUP",
                "OP_HASH160",
                p2pkh_addr.to_hash160(),
                "OP_EQUALVERIFY",
                "OP_CHECKSIG",
            ]
        )

        addr = P2shAddress.from_script(redeem_script)
        p2sh_addr = addr.to_string()

        p2sh.delete(0, END)
        p2sh.insert(END, f"{p2sh_addr}")
        p2sh.bind("<FocusIn>", lambda args: p2sh.insert(END, ""))

        sk.delete(0, END)
        sk.insert(END, f"{sender_privk}")
        sk.bind("<FocusIn>", lambda args: sk.insert(END, ""))

        sa.delete(0, END)
        sa.insert(END, f"{sender_pubk}")
        sa.bind("<FocusIn>", lambda args: sa.insert(END, ""))
        canvas1.create_text(
            entry_x,
            entry_y + -50,
            fill="black",
            font="Arial 10",
            text="Add funds to address",
        )

        qr_p2sh = pyqrcode.create(p2sh_addr)

        qr_p2sh.png("timelock_qr.png", scale=6)
        qr_p2sh.png("timelock_qr_copy.png", scale=6)

        image1 = Image.open("timelock_qr.png")

        resized_image = image1.resize((80, 80), Image.Resampling.LANCZOS)
        test = ImageTk.PhotoImage(resized_image)
        label1 = Label(image=test)
        label1.image = test
        label1.place(x=entry_x + 100, y=entry_y - 170)

    generate_private = Button(text="Generate", command=generate_wallet)

    generate_private.pack()
    canvas1.create_window(entry_x + 175, entry_y - 70, window=generate_private)

    root.bind("<Return>", lambda x: generate_private_key)

    canvas1.create_text(
        entry_x, entry_y + 75, fill="black", font="Arial 10", text="Enter date: MM-DD-YYYY"
    )

    def timestamp_color():
        global timestamp

    timestamp = Entry(root, fg="black", relief=SOLID)

    canvas1.create_window(entry_x, entry_y + 105, window=timestamp)

    txid_input = Entry(root, width=66, relief=SOLID)

    canvas1.create_window(entry_x, entry_y + 185, window=txid_input)

    canvas1.create_text(
        entry_x,
        entry_y + 160,
        fill="black",
        font="Arial 10",
        text="Paste txid/hash from transaction above",
    )

    vout_enter = Entry(root, relief=SOLID, width=5)

    canvas1.create_window(entry_x - 100, entry_y + 245, window=vout_enter)

    canvas1.create_text(entry_x - 100, entry_y + 220, fill="black", font="Arial 10", text="VOUT")
    
    amount = Entry(root, relief=SOLID, width=20)

    canvas1.create_window(entry_x + 130, entry_y + 245, window=amount)

    canvas1.create_text(entry_x + 125, entry_y + 220, fill="black", font="Arial 10", text="BTC- minus tx fees")

    def complete():

        if (
            timestamp.get() != ""
            and txid_input.get() != ""
            and amount.get() != ""
            and p2sh.get() != ""
            and sk.get() != ""
            and sa.get() != ""
        ):


            txid = txid_input.get()
            satoshis = Decimal(amount.get())

            sender_privk = sk.get()
            sender_pubk = sa.get()

            rec_privk = rk.get()
            rec_pubk = ra.get()

            iso = timestamp.get()
            pubk = p2sh.get()
            vout = int(vout_enter.get())

            if len(txid) == 64:


                if vout == 0 or vout == 1:

                    def validate(date_text):
                        try:
                            datetime.datetime.strptime(date_text, "%m-%d-%Y")

                            return True
                        except:

                            return False

                    if validate(iso) == True:

                        if (sender_exists == False or rec_exists == False):
                    
   
                            label1 = Label(
                                root,
                                bg="white",
                                text="Please wait while files are created",
                            )
                            canvas1.create_window(entry_x, entry_y + 270, window=label1)



                            unix = dp.parse(iso)
                            unix_dec = unix.timestamp()
                            unix_time = int(unix_dec)

                            # SENDER REDEEM

                            sender_lock = Locktime(500000001)

                            sender_txin = TxInput(txid, vout, sequence=seq.for_input_sequence())

                            sender_p2pkh_sk = PrivateKey(sender_privk)
                            sender_p2pkh_pk = sender_p2pkh_sk.get_public_key().to_hex()
                            sender_p2pkh_addr = sender_p2pkh_sk.get_public_key().get_address()

                            sender_redeem_script = Script(
                                [
                                    seq.for_script(),
                                    "OP_CHECKLOCKTIMEVERIFY",
                                    "OP_DROP",
                                    "OP_DUP",
                                    "OP_HASH160",
                                    sender_p2pkh_addr.to_hash160(),
                                    "OP_EQUALVERIFY",
                                    "OP_CHECKSIG",
                                ]
                            )

                            sender_addr = P2shAddress.from_script(sender_redeem_script)

                            sender_to_addr = P2pkhAddress(sender_pubk)
                            sender_txout = TxOutput(
                                to_satoshis(satoshis), sender_to_addr.to_script_pub_key()
                            )

                            sender_tx = Transaction(
                                [sender_txin], [sender_txout], sender_lock.for_transaction()
                            )

                            sender_sig = sender_p2pkh_sk.sign_input(
                                sender_tx, 0, sender_redeem_script
                            )

                            sender_txin.script_sig = Script(
                                [sender_sig, sender_p2pkh_pk, sender_redeem_script.to_hex()]
                            )
                            sender_signed_tx = sender_tx.serialize()

                            sender_txid = sender_tx.get_txid()

                            # RECEIVER REDEEM

                            rec_lock = Locktime(unix_time)

                            rec_txin = TxInput(txid, vout, sequence=seq.for_input_sequence())

                            rec_p2pkh_sk = PrivateKey(sender_privk)
                            rec_p2pkh_pk = rec_p2pkh_sk.get_public_key().to_hex()
                            rec_p2pkh_addr = rec_p2pkh_sk.get_public_key().get_address()

                            rec_redeem_script = Script(
                                [
                                    seq.for_script(),
                                    "OP_CHECKLOCKTIMEVERIFY",
                                    "OP_DROP",
                                    "OP_DUP",
                                    "OP_HASH160",
                                    rec_p2pkh_addr.to_hash160(),
                                    "OP_EQUALVERIFY",
                                    "OP_CHECKSIG",
                                ]
                            )

                            rec_addr = P2shAddress.from_script(rec_redeem_script)

                            rec_to_addr = P2pkhAddress(rec_pubk)
                            rec_txout = TxOutput(
                                to_satoshis(satoshis), rec_to_addr.to_script_pub_key()
                            )

                            rec_tx = Transaction(
                                [rec_txin], [rec_txout], rec_lock.for_transaction()
                            )

                            rec_sig = rec_p2pkh_sk.sign_input(rec_tx, 0, rec_redeem_script)

                            rec_txin.script_sig = Script(
                                [rec_sig, rec_p2pkh_pk, rec_redeem_script.to_hex()]
                            )
                            rec_signed_tx = rec_tx.serialize()

                            rec_txid = rec_tx.get_txid()

                            sender_wallet_text = """

    This is the sender's paper wallet. Please keep this file secure and offline. Anyone with access to this 
    file can redeem your bitcoin.
				
    You can use the redeem script to redeem your bitcoin at any time. To redeem, visit a block explorer 
    (ex. https://www.blockchain.com/btc/pushtx) and paste the redeem script into the input field.
				
    You can then open BTCapsule and use the Sweep Wallet feature. To sweep a wallet, make sure sender_wallet.txt is
    in the same folder as BTCapsule. enter the address you wish to send your bitcoin to and the amount that was added 
    to the timelock address (minus miner fees). This will create another file called redeem.txt that will contain 
    another redeem script. Paste this into the block explorer to send the bitcoin to your wallet.
				
	To add more funds, you can create another BTCapsule timelocked transaction and require the receiver to redeem
    multiple redeem scripts, or you can follow the directions to sweep your sender wallet (making the receiver's wallet 
    invalid) and create a new BTCapsule transaction with the additional funds.
				
    *IMPORTANT!* Sweeping this wallet will remove all bitcoin. You must input a smaller amount to pay for 
    miner fees. The difference between the unspent amount and the input will go to the miners.
    To give the timelocked wallet to another person, copy the receiver_files folder
    to a flash drive. DO NOT INCLUDE SENDER WALLET. Directions to redeem are included in their wallet.
				
				
				            """

                            p2sh_addr = p2sh.get()

                            sender_wallet = open("sender_wallet.txt", "w")

                            sender_wallet.write(
                                "TxId: "
                                + f"{sender_txid}"
                                + "\n\nPrivate key: "
                                + f"{sender_privk}"
                                + "\n\nPublic address: "
                                + f"{sender_pubk}"
                                + "\n\nTimelock address: "
                                + f"{p2sh_addr}"
                                + "\n\nRedeem date: "
                                + f"{iso}"
                                + "\n\nRedeem script: "
                                + f"{sender_signed_tx}"
                                + "\n\n"
                                + f"{sender_wallet_text}"
                            )

                            sender_wallet.close()

                            os.chmod("sender_wallet.txt", S_IREAD)

                            rec_wallet_text = """
    This is a timelocked paper wallet. Please keep this file secure and offline. Anyone with access to this 
    file can redeem your bitcoin.
				
    You can use the redeem script to redeem your bitcoin after the redeem date. To redeem, visit a block explorer 
    (ex. https://www.blockchain.com/btc/pushtx) and paste the redeem script into the input field.
				
    You can then open BTCapsule and use the Sweep Wallet feature. To sweep a wallet, make sure receiver_wallet.txt is
    in the same folder as BTCapsule. enter the address you wish to send your bitcoin to and the amount that was added 
    to the timelock address (minus miner fees). This will create another file called redeem.txt that will contain 
    another redeem script. Paste this into the block explorer to send the bitcoin to your wallet.
				
				
				
    *IMPORTANT!* Sweeping this wallet will remove all bitcoin. You must input a smaller amount to pay for 
    miner fees. The difference between the unspent amount and the input will go to the miners.

    The redeem time is set at 12:00AM on the redeem date. It may take several hours before the network will
    accept your redeem script. If you get an error:
    sendrawtransactiom RPC error: 
    {"code":-26,"message":"non-final"}
    this means the transaction is working as expected. Please wait a few hours and try again.
				
				
				            """

                            rec_wallet = open("receiver_wallet.txt", "w")

                            rec_wallet.write(
                                "TxId: "
                                + f"{rec_txid}"
                                + "\n\nPrivate key: "
                                + f"{rec_privk}"
                                + "\n\nPublic address: "
                                + f"{rec_pubk}"
                                + "\n\nTimelock address: "
                                + f"{p2sh_addr}"
                                + "\n\nRedeem date: "
                                + f"{iso}"
                                + "\n\nRedeem script: "
                                + f"{rec_signed_tx}"
                                + "\n\n"
                                + f"{rec_wallet_text}"
                            )

                            rec_wallet.close()

                            os.chmod("receiver_wallet.txt", S_IREAD)
                 
                            os.mkdir('receiver_files')
                            rec_path = 'receiver_files/'
                
                            os.mkdir('sender_files')
                            send_files = 'sender_files/'
             
                            shutil.copy('receiver_wallet.txt', rec_path)
                
                            sender_files = [f for f in os.listdir() if '.txt' in f.lower() or '.png' in f.lower()] 

                            for files in sender_files: 

                                new_path = send_files + files 
                                shutil.move(files, new_path)


                            if btc_exists == True:
                                shutil.copy("BTCapsule_testnet.exe", send_files)
                                shutil.copy("BTCapsule_testnet.exe", rec_path)

                
                            if btc_py_exists == True:
                                shutil.copy("BTCapsule_testnet.py", rec_path)
                                shutil.copy("BTCapsule_testnet.py", send_files)

                            
                
                            if btc_linux == True:
                                shutil.copy("BTCapsule_testnet", rec_path)
                                shutil.copy("BTCapsule_testnet", send_files)


                            label1 = Label(
                                root,
                                bg="white",
                                text="                    Success!                      ",
                            )
                            canvas1.create_window(entry_x, entry_y + 270, window=label1)


                        else:

                            
                            label1 = Label(
                                root,
                                bg="white",
                                text="            Wallet already exists. Restart BTCapsule and try again              ",
                            )
                            canvas1.create_window(entry_x, entry_y + 270, window=label1)


                            
                   
                    else:

                                    
                        label1 = Label(
                            root,
                            bg="white",
                            text="Enter a valid year: MM-DD-YYYY",
                        )
                        canvas1.create_window(entry_x, entry_y + 270, window=label1)


                else:
 
                           
                    label1 = Label(
                        root,
                        bg="white",
                        text="       VOUT should be 0 or 1          ",
                    )
                    canvas1.create_window(entry_x, entry_y + 270, window=label1)

            else:
                           
                label1 = Label(
                    root,
                    bg="white",
                    text="Invalid txid/hash",
                )
                canvas1.create_window(entry_x, entry_y + 270, window=label1)


        else:

                            
            label1 = Label(
                root,
                bg="white",
                text="Please complete all fields",
            )
            canvas1.create_window(entry_x, entry_y + 270, window=label1)


    button1 = Button(text="Enter", command=complete)
    canvas1.create_window(entry_x, entry_y + 300, window=button1)

    # SWEEP WALLET

    canvas1.create_line(
        0, entry_y + 350, entry_y + 390, entry_y + 350, fill="black", width=5
    )

    canvas1.create_text(
        entry_x, entry_y + 370, fill="black", font="Arial 10 bold", text="SWEEP WALLET"
    )

    canvas1.create_text(
        entry_x,
        entry_y + 395,
        fill="black",
        font="Arial 10",
        text="When raw transaction is successful, use \nthis field to send funds to your own wallet",
    )

    addr_enter = Entry(root, width=66, relief=SOLID)
    sat_enter = Entry(root, width=60, relief=SOLID)

    canvas1.create_text(
        entry_x,
        entry_y + 425,
        fill="black",
        font="Arial 10",
        text="Enter address to send funds",
    )

    canvas1.create_window(entry_x, entry_y + 445, window=addr_enter)

    canvas1.create_text(
        entry_x, entry_y + 475, fill="black", font="Arial 10", text="Enter BTC amoumt"
    )

    canvas1.create_window(entry_x, entry_y + 495, window=sat_enter)

    def redeem():

        if sat_enter.get() != "" and addr_enter.get() != "":

            if sender_exists == True:

                with open("sender_files/sender_wallet.txt", "r") as f:

                    f.seek(0)
                    lines = f.readlines()

                    t = lines[0]
                    txid = t[6:].rstrip()

                    p = lines[2]
                    private_key = p[13:].rstrip()

                    ad = lines[4]
                    address = ad[16:].rstrip()

                satoshis = Decimal(sat_enter.get())
                which_addr = addr_enter.get()

                sweep_wallet(which_addr, txid, satoshis, private_key, address)

                label1 = Label(
                    root,
                    bg="white",
                    text="                 Success!                   ",
                )
                canvas1.create_window(entry_x + 3, entry_y + 565, window=label1)

            if rec_exists == True and sender_exists == False:

                with open("receiver_files/receiver_wallet.txt", "r") as f:

                    f.seek(0)
                    lines = f.readlines()

                    t = lines[0]
                    txid = t[6:].rstrip()

                    p = lines[2]
                    private_key = p[13:].rstrip()

                    ad = lines[4]
                    address = ad[16:].rstrip()

                satoshis = Decimal(sat_enter.get())

                which_addr = addr_enter.get()

                sweep_wallet(which_addr, txid, satoshis, private_key, address)

                label1 = Label(
                    root,
                    bg="white",
                    text="                 Success!                   ",
                )
                canvas1.create_window(entry_x + 3, entry_y + 565, window=label1)

            if rec_exists == False and sender_exists == False:

                label1 = Label(
                    root,
                    bg="white",
                    text="Missing wallet. Move wallet to this \nfolder and restart BTCapsule",
                )
                canvas1.create_window(entry_x + 3, entry_y + 575, window=label1)

    send = Button(text="Send", command=redeem)
    send.pack()

    canvas1.create_window(entry_x, entry_y + 540, window=send)

    root.title("Bitcoin Time Capsule")

    root.mainloop()


if __name__ == "__main__":
    main()
