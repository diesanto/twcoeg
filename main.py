#!/usr/bin/python3
# ##################################################
# Tugas dari Pak Herdisel dab bahan learning by doing
# Date   : 25 Desember 2018
# Author : @zetc0de
# Blog	 : https://zetc0de.github.io/
# Remove a credit doesn't make you look like a coder
####################################################

import tweepy
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from keys import keys
import json
from pymongo import MongoClient
import datetime


CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']
DB_USER = keys["db_user"]
DB_PASS = keys["db_pass"]

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
c = MongoClient('192.168.33.10')
db = c.twcoeg

# if db.authenticate(DB_USER,DB_PASS):
# 	print("Conected")

# # for i in tweepy.Cursor(api.search,q="#2019gantipresiden",lang="en",since="2018-11-01").items():
# # 		z = json.dumps({"data":[{
# # 			"Text":i.text,
# # 			"Username":i.user.screen_name,
# # 			"Lokasi":i.user.location
# # 			}]},sort_keys=True,indent=4)
		
# # 		print(z)
# # # print(len(tweets))
# # 		# print(i.user.screen_name)
# # 		# print(i.user.location)
# Clear placeholder
def clear_E1(event):
	E1.delete(0,tk.END)

def clear_E2(event):
	E2.delete(0,tk.END)


root = tk.Tk()

root.configure(background="black")
root.geometry("500x600")
title = "Hashtag Analyzer"
root.title(title)

# Frame
MainFrame = tk.Frame(root, width=385, height=660, relief='raised', borderwidth=2)
LabelTag = tk.Frame(MainFrame, width=375, height=315, relief='raised', borderwidth=2,padx=10,pady=10)
LabelTagatas = tk.Frame(LabelTag, width=355, height=50, relief='raised', borderwidth=2,padx=10,pady=10)
LabelTagbawah = tk.Frame(LabelTag, width=355, height=50, relief='raised', borderwidth=2,padx=10,pady=10)
LabelTagproc = tk.Frame(LabelTag, width=355, height=10, relief='raised', borderwidth=2,padx=10,pady=10)
ButtonFrame = tk.Frame(MainFrame, width=375, height=330, relief='raised', borderwidth=2)

judul = Label(MainFrame,text = title)
judul.config(font=("Hack",20),fg="white")
judul.pack(fill="both")


# Label Tanggal
dari = tk.Label(LabelTagatas,text="Dari Tanggal (yyyy-mm-dd)",anchor='w')
dari.config(font=("Arial",12),fg="white",)
dari.pack(expand=True, fill=X)

# Form Tanggal
E1 = tk.Entry(LabelTagatas)
E1.insert(0,"Dari Tanggal")
E1.pack()
E1.bind("<Button-1>",clear_E1)

# Label Hashtag
search = tk.Label(LabelTagbawah,text="Input Hashtag (#jomblo)",anchor='w')
search.config(font=("Arial",12),fg="white")
search.pack(expand=True, fill=X)

# Form Hashtag
E2 = tk.Entry(LabelTagbawah)
E2.insert(0,"Masukkan Hashtag")
E2.pack()
E2.bind("<Button-1>",clear_E2)

# Objek Progress Bar
progress = ttk.Progressbar(LabelTagproc, length=385)
progress.pack(side=BOTTOM)

# tweets=[]
# mentions=[]
# users=[]
# lokasi=[]

# Time
waktu = datetime.datetime.now()
waktu = waktu.strftime("%Y-%m-%d")
tw = []

def analize():
	with open("data.json","w") as js:
		for i in tweepy.Cursor(api.search,q={E2.get()},lang="en",since=E1.get()).items():
			# x = json.dumps({"data":{
			# 		"text":i.text,
			# 		"username":i.user.screen_name,
			# 		"lokasi":i.user.location
			# 		}},sort_keys=True,indent=4)
			created_at = str(i.created_at)
			tweets = {
				"created_at":created_at,
				"text":i.text,
				"username":i.user.screen_name,
				"lokasi":i.user.location
				}
			tw.append(tweets)

		# db.waktu.insertOne(tw)
		data = {waktu:tw}
		json.dump(data,js,indent=4)
		# print(data)
		progress['value']=100



	# print(len(tweets))
	messagebox.showinfo("Info","Selesai")

def resetData():
	tw.clear()
	messagebox.showinfo("Info","Data Reset OK")

def countTweet():
	jumlahTweet = len(tw)
	messagebox.showinfo("Jumlah Tweet",jumlahTweet)

def saveDb():
	with open("data.json","r") as d:
		data = json.load(d)
		db.tweets.insert_many(data[waktu])
	
	messagebox.showinfo("Info","Saved!")

# Button Analyze!
B1 = tk.Button(LabelTag,text="Analyze!",command=analize,padx=100)
B1.pack(side=BOTTOM)


# Button Menu
jumlah_tweet = tk.Button(ButtonFrame, text='Show Tweets Count', command=countTweet)
save_DB = tk.Button(ButtonFrame, text='Save Into Database', command=saveDb)
reset = tk.Button(ButtonFrame,text="Reset Data",command=resetData)
quit = tk.Button(ButtonFrame, text='Quit', command=root.destroy)

# Cinfig frame dan menu
for frame in [MainFrame,LabelTag, LabelTagatas,LabelTagbawah,LabelTagproc,ButtonFrame]:
    frame.pack(expand=True, fill='both')
    frame.pack_propagate(0)

for menu in [jumlah_tweet,reset,save_DB,quit]:
    menu.pack(expand=True, fill='both')

# for settag in [dari,search]:
# 	settag.config(font=("Hack",12),fg="white")
# 	settag.pack(expand=True, fill='y')

# for entri in [dari,E1]:
# 	entri.pack()

# for entri in [search,E2]:
# 	entri.pack()

root.mainloop()