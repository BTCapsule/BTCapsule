import os
import os.path
import cryptography
import tkinter as tk
from os.path import exists
from cryptography.fernet import Fernet
import base64
import ntplib
import random as r
import datetime
import socket
from bitcoincli import Bitcoin
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import time





root= tk.Tk()


	

	











def numConcat(num1, num2, num3, num4): 
	num1 = str(num1) 
	num2 = str(num2) 
	num3 = str(num3)
	num4 = str(num4)

	num3 += num4
	num2 += num3
	num1 += num2

	return int(num1) 



def numCheck(num1, num2, num3): 
	num1 = str(num1) 
	num2 = str(num2) 
	num3 = str(num3)
		

		
	num2 += num3
	num1 += num2

	return int(num1) 


		






def main():





	

	global bitcoin_year


	




	keys_exists = exists('keys.txt')
	year_exists= exists('year.txt')


	


	# THIS IS YOUR ENCRYPTION KEY AND MUST BE GENERATED SEPARATELY

	n=b""
	          

		





	if (keys_exists == True and year_exists == False):


		canvas1 = tk.Canvas(root, width = 400, 
			height = 240,
			bg = 'white',
			highlightthickness=0
			)


		canvas1.pack()

		canvas1.create_text(200,110,
			width= 350,
				
			fill="black",
			font="Arial 10",
			text="Missing Year")

		root.title('Bitcoin Time Capsule')


		
		
		root.mainloop()



	if (keys_exists == False and year_exists == True):

			


		canvas1 = tk.Canvas(root, width = 400, 
			height = 240,
			bg = 'white',
			highlightthickness=0
			)


		canvas1.pack()

		canvas1.create_text(200,110,
			width= 350,
				
			fill="black",
			font="Arial 10",
			text="Missing Year")

		root.title('Bitcoin Time Capsule')


		
		
		root.mainloop()












	if (keys_exists == False and year_exists == False):


		canvas1 = tk.Canvas(root, width = 400, 
		height = 100,
		bg = 'white',
		highlightthickness=0
		)


		canvas1.pack()

		entry1 = tk.Entry (root)

		canvas1.create_window(200, 60, window=entry1)

		canvas1.create_text(200,35,fill="black",
		font="Arial 10",
		text="Enter a year")






		canvas2 = tk.Canvas(root, width = 400, 
		height = 140,
		bg = 'white',
		highlightthickness=0
		)

		canvas2.pack()


		entry2 = tk.Entry (root)

		canvas2.create_window(200, 40, window=entry2)



		canvas2.create_text(200,15,fill="black",
		font="Arial 10",
		text="Enter your keys")

		rand = r.randint(100, 999)
		pair = str(rand)
	

		def get_keys(event=None):
			global private_keys
			private_keys = entry2.get()


			file2 = open('keys.txt', 'w')
			file2.write(pair + private_keys)
			file2.close()

			with open('keys.txt', 'rb') as file:
				original = file.read()

			fernet= Fernet(n)

			encrypted = fernet.encrypt(original)

			with open('keys.txt', 'wb') as encrypted_file:
				encrypted_file.write(encrypted)





		

		def get_year(event=None):
			global year
			year = entry1.get()



			try:
				global year_num
				year_num=int(year)
			except ValueError:

				label1 = tk.Label(root, bg='white', text= 'Please choose a valid year')
				canvas2.create_window(200, 115, window=label1)



			if (year_num<2009 or year_num>9999):
				label1 = tk.Label(root, bg='white', text= 'Please choose a future year')
				canvas2.create_window(200, 115, window=label1)







			else:



				label1 = tk.Label(root, bg='white', text= '                 Success!                   ')
				canvas2.create_window(200, 115, window=label1)

				file1 = open('year.txt', 'w')
				file1.write(year + pair)
				file1.close()

				
				

				with open('year.txt', 'rb') as file:
					original = file.read()


				fernet = Fernet(n)





				encrypted = fernet.encrypt(original)

				with open('year.txt', 'wb') as encrypted_file:
					encrypted_file.write(encrypted)






		button1 = tk.Button(text='Enter',command= lambda: [get_year(), get_keys()])
		root.bind("<Return>", lambda x: [get_year(), get_keys()])			






		canvas2.create_window(200, 80, window=button1)




		
		root.title('Bitcoin Time Capsule')


		
		
		root.mainloop()



		






	if (keys_exists == True and year_exists == True):

		

		
		
		
		try:


		

			bitcoin = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%("user","pass"))

			info = bitcoin.getblockchaininfo()
			date = info['mediantime']


			datem = datetime.datetime.fromtimestamp(date)

					
					
			year = datem.year
			
			
						
		
			

			canvas1 = tk.Canvas(root, width = 400, 
				height = 240,
				bg = 'white',
				highlightthickness=0
				)


			canvas1.pack()



			fernet = Fernet(n)
			
			with open('year.txt', 'rb') as enc_file:
				encrypted = enc_file.read()

			decrypted = fernet.decrypt(encrypted)

			with open ('year.txt', 'wb') as dec_file:
				dec_file.write(decrypted)

		
			with open('year.txt', 'r') as f:
				num = f.read()
				check_year = num[4:]
			
				user = [ int(x) for x in num.split() ]

				s = [str(integer) for integer in user]
				a_string = "".join(s)

				res = int(a_string)

				year_list = list(map(int, str(res)))

				a = year_list[0]
				b = year_list[1]
				c = year_list[2]
				d = year_list[3]

				user_year = (numConcat(a,b,c,d))
				f.close()

			
			

		


				if year < user_year:

				
			


					canvas1.create_text(200,110,fill="black",
					font="Arial 10",
					text="Please wait until " + f"{user_year}" + "\n\nIf current year is " + f"{user_year}" + ", please wait until Bitcoin Core is updated.")




					with open('year.txt', 'rb') as file:
						original = file.read()
					fernet = Fernet(n)
					encrypted = fernet.encrypt(original)

					with open('year.txt', 'wb') as encrypted_file:
						encrypted_file.write(encrypted)


					


				elif year >= user_year:

					fernet = Fernet(n)
				
					with open('keys.txt', 'rb') as enc_file:
						encrypted = enc_file.read()

					decrypted = fernet.decrypt(encrypted)

					with open ('keys.txt', 'wb') as dec_file:
						dec_file.write(decrypted)


					file2 = open("keys.txt", "r")
					orig = file2.read()
				

					e = orig[0]
					f = orig[1]
					g = orig[2]
				

					check_keys = str(numCheck(e,f,g))
				


					keys = orig[3:]
					file2.close()

					if (check_keys != check_year):


					

						canvas1.create_text(200,110,fill="black",
						font="Arial 10",
						text="Invalid Key")
					
						os.remove('keys.txt')
						os.remove('year.txt')

						
					elif (check_keys == check_year):

					
				
					

						canvas1.create_text(200,110,
						width= 350,
				
						fill="black",
						font="Arial 10",
						text=f"{keys}")

						with open('year.txt', 'rb') as file:
							original = file.read()

						with open('keys.txt', 'rb') as file:
							original2 = file.read()


						fernet = Fernet(n)





						encrypted = fernet.encrypt(original)
						encrypted2 = fernet.encrypt(original2)

						with open('keys.txt', 'wb') as encrypted_file:
							encrypted_file.write(encrypted2)

						with open('year.txt', 'wb') as encrypted_file:
							encrypted_file.write(encrypted)


			root.title('Bitcoin Time Capsule')


			root.mainloop()

		except:
			
			canvas1 = tk.Canvas(root, width = 400, 
				height = 240,
				bg = 'white',
				highlightthickness=0
				)


			canvas1.pack()
			
			canvas1.create_text(200,110,fill="black",
			font="Arial 10",
			text="Please open Bitcoin Core and restart BTCapsule")

			

			root.title('Bitcoin Time Capsule')


			root.mainloop()

		

if __name__ == "__main__":
	main()


