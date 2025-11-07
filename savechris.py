import tkinter as tk
from PIL import ImageTk
from random import choice
import collections
import time
import webbrowser
import json
import tkinter.scrolledtext as st
import re
class Application(tk.Frame):
	def __init__(self,master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.menu()
	def cls(self):
		for widget in self.winfo_children():
			widget.destroy()
	def menu(self):
		self.cls()
		self.hm = tk.Label(self,text="Can you save Computer Science Chris???")
		self.playbtn = tk.Button(self,text="Play Now!",command=self.start_animation)
		self.playbtnai = tk.Button(self,text="AI Mode",command=self.start_animation_ai)
		self.htpbtn = tk.Button(self,text="How to Play",command=lambda: webbrowser.open("https://www.wikihow.com/Play-Hangman"))
		self.hm.grid(row=0,column=0)
		self.playbtn.grid(row=1,column=0)
		self.playbtnai.grid(row=2,column=0)
		self.htpbtn.grid(row=3,column=0)
	def animate(self,directory):
		self.cls()
		lengths = json.loads(open(directory+"/lengths.json").read())
		for i in lengths:
			self.cls()
			self.i = ImageTk.PhotoImage(file=f"{directory}/{i[0]}")
			self.cont = tk.Label(self,image=self.i)
			self.cont.grid(row=0,column=0)
			time.sleep(i[1])
	def start_animation_ai(self):
		self.start_animation(ai=True)
	def start_animation(self,ai=False):
		self.animate("savechris/frames/start_animation")
		self.make_difficulty(ai)
	def make_difficulty(self,ai):
		self.cls()
		self.dlabel = tk.Label(self,text="Choose Difficulty:")
		self.easy = tk.Button(self,text="Easy",command=lambda: self.play('easy',ai))
		self.medium = tk.Button(self,text="Medium",command=lambda: self.play('medium',ai))
		self.hard = tk.Button(self,text="Hard",command=lambda: self.play('hard',ai))
		self.dlabel.grid(row=0,column=0)
		self.easy.grid(row=1,column=0)
		self.medium.grid(row=2,column=0)
		self.hard.grid(row=3,column=0)
		if not ai:
			self.impossible = tk.Button(self,text="Impossible",command=lambda: self.play('impossible',ai))
			self.impossible.grid(row=4,column=0)
	def play(self,mode,ai):
		self.cls()
		self.mode = mode
		self.ai = ai
		self.wlist = open(f'savechris/words/{mode}.txt').read().split("\n")
		self.word = choice(self.wlist)
		self.right = ['' for i in self.word]
		self.wrong = []
		self.frames = {}
		self.imgframe = tk.Frame(self)
		self.rightFrame = tk.Frame(self)
		self.wrongFrame = tk.Frame(self)
		self.guessFrame = tk.Frame(self)
		self.aiFrame = tk.Frame(self)
		self.i = ImageTk.PhotoImage(file="savechris/frames/main/0.jpg")
		self.img = tk.Label(self.imgframe,image=self.i)
		self.img.grid(row=0,column=0)
		self.imgframe.grid(row=0,column=0)
		self.rightbuttons = []
		c = 0
		for i in self.word:
			self.rightbuttons.append(tk.Button(self.rightFrame,text=" ",width=3,height=1,font=("Arial", 16)))
			self.rightbuttons[-1].grid(row=0,column=c)
			c += 1
		self.rightFrame.grid(row=1,column=0)
		self.wrongbuttons = []
		for c in range(0,7):
			self.wrongbuttons.append(tk.Button(self.wrongFrame,text=" ",width=3,height=1,font=("Arial", 16)))
			self.wrongbuttons[-1].grid(row=c,column=0)
		self.wrongFrame.grid(row=0,column=1)
		if ai:
			self.aiLabel = tk.Label(self.aiFrame,text="AI Thoughts: ")
			self.aiText = st.ScrolledText(self.aiFrame,height=17,width=25,state=tk.DISABLED)
			self.aiBtn = tk.Button(self.aiFrame,text="Start AI!",command=self.aiClick)
			self.aiLabel.grid(row=0,column=0)
			self.aiText.grid(row=1,column=0)
			self.aiBtn.grid(row=2,column=0)
			self.aiFrame.grid(row=0,column=2)
			self.setVal(self.aiText,"Click Button to Start!\n")
		else:
			self.guessBox = tk.Entry(self.guessFrame,width=2)
			self.guessBox.grid(row=0,column=0)
			self.guessBtn = tk.Button(self.guessFrame,text='Guess!',command=self.callGuess)
			self.guessBtn.grid(row=0,column=1)
			self.guessFrame.grid(row=2,column=0)
			self.bind("<Key>", self.keyLog)
			self.guessBox.bind("<Key>", self.keyLog)
	def setVal(self,obj,text):
		obj.config(state="normal")
		obj.insert(tk.END,text)
		obj.config(state="disabled")
	def aiClick(self):
		if self.aiBtn['text'] == "Start AI!":
			self.reg = ['.' for i in self.word]
			self.setVal(self.aiText,f"Hello User!\nI will start by removing all words in my dictionary that are not of length ({len(self.word)}).\n")
			for i in self.wlist:
				if len(i) != len(self.word):
					self.wlist.remove(i)
			self.setVal(self.aiText,f"There are now {len(self.wlist)} possible words left.\n")
			self.aiBtn['text'] = "Guess"
		wf = False
		for i in self.right:
			if i != '':
				wf = True
				break
		if not wf:
			joined = ''.join(self.wlist)
			self.setVal(self.aiText,"I will now search for the most common letter to guess.\n")
			mostCommon = collections.Counter(joined).most_common(1)[0][0]
			self.setVal(self.aiText,f"The most common letter is '{mostCommon}'.\nGuessing...\n")
			v = self.guess(mostCommon)
			if v:
				self.setVal(self.aiText,f"'{mostCommon}' is in the word!\nAdding to RegEx.\n")
				c = 0
				for i in self.right:
					if i == mostCommon:
						self.reg[c] = i
					c += 1
				self.setVal(self.aiText,f"The new regex is: '{''.join(self.reg)}'!\nRemoving all words that don't contain {mostCommon}.\n")
				for i in self.wlist:
					if not mostCommon in i:
						self.wlist.remove(i)
				self.setVal(self.aiText,f"There are now {len(self.wlist)} possible words.\n")
			else:
				self.setVal(self.aiText,f"'{mostCommon}' is not in the word.\nRemoving all words containing {mostCommon}.\n")
				for i in self.wlist:
					if mostCommon in i:
						self.wlist.remove(i)
				self.setVal(self.aiText,f"There are now {len(self.wlist)} possible words.\n")
		else:
			self.setVal(self.aiText,f"Finding all words that fit regex '{''.join(self.reg)}'\n")
			r = re.compile('^'+''.join(self.reg)+'$')
			for i in self.wlist:
				if not re.match(r,i):
					self.wlist.remove(i)
			self.setVal(self.aiText,f"There are now {len(self.wlist)} possible words.\nFinding most common not-guessed letter.\n")
			joined = ''.join(self.wlist)
			for i in self.right:
				joined = joined.replace(i,'')
			mostCommon = collections.Counter(joined).most_common(1)[0][0]
			self.setVal(self.aiText,f"The most common letter is '{mostCommon}'.\nGuessing...\n")
			v = self.guess(mostCommon)
			if v:
				self.setVal(self.aiText,f"'{mostCommon}' is in the word!\nAdding to RegEx.\n")
				c = 0
				for i in self.right:
					if i == mostCommon:
						self.reg[c] = i
					c += 1
				self.setVal(self.aiText,f"The new regex is: '{''.join(self.reg)}'!\nRemoving all words that don't contain {mostCommon}.\n")
				for i in self.wlist:
					if not mostCommon in i:
						self.wlist.remove(i)
				self.setVal(self.aiText,f"There are now {len(self.wlist)} possible words.\n")
			else:
				self.setVal(self.aiText,f"'{mostCommon}' is not in the word.\nRemoving all words containing {mostCommon}.\n")
				for i in self.wlist:
					if mostCommon in i:
						self.wlist.remove(i)
				self.setVal(self.aiText,f"There are now {len(self.wlist)} possible words.\n")
	def keyLog(self,event):
		if event.keysym == 'Return':
			self.guess(self.guessBox.get()[0])
			self.guessBox.delete(0,tk.END)
	def callGuess(self):
		self.guess(self.guessBox.get()[0])
		self.guessBox.delete(0,tk.END)
	def guess(self,t):
		t = t.lower()
		if t in self.word:
			if not t in self.right:
				count = 0
				for char in self.word:
					if char == t:
						self.right[count] = t
						self.rightbuttons[count]['text'] = t.upper()
					count += 1
				if ''.join(self.right) == self.word:
					outcome = tk.Tk()
					outcome.title("You Win!")
					outcome.l = tk.Label(outcome,text="You Win!\nWhat Next?")
					outcome.l.grid(row=0,column=0)
					outcome.pag = tk.Button(outcome,text="Play Again",command=lambda: self.killAnd(outcome,0))
					outcome.pag.grid(row=1,column=0)
					outcome.menu = tk.Button(outcome,text="Main Menu",command=lambda: self.killAnd(outcome,1))
					outcome.menu.grid(row=1,column=1)
					outcome.q = tk.Button(outcome,text="Quit",command=lambda: self.killAnd(outcome,2))
					outcome.q.grid(row=1,column=2)
					outcome.mainloop()
			return True
		else:
			if len(self.wrong) != 6:
				if not t in self.wrong:
					self.wrong.append(t)
					self.wrongbuttons[len(self.wrong)-1]['text'] = t.upper()
					self.i = ImageTk.PhotoImage(file=f"savechris/frames/main/{len(self.wrong)}.jpg")
					self.img['image'] = self.i
			else:
				outcome = tk.Tk()
				outcome.title("You Loose!")
				outcome.l = tk.Label(outcome,text="You Loose!\nWhat Next?")
				outcome.l.grid(row=0,column=0)
				outcome.pag = tk.Button(outcome,text="Play Again",command=lambda: self.killAnd(outcome,0))
				outcome.pag.grid(row=1,column=0)
				outcome.menu = tk.Button(outcome,text="Main Menu",command=lambda: self.killAnd(outcome,1))
				outcome.menu.grid(row=1,column=1)
				outcome.q = tk.Button(outcome,text="Quit",command=lambda: self.killAnd(outcome,2))
				outcome.q.grid(row=1,column=2)
				outcome.mainloop()
			return False
	def killAnd(self,outcome,next):
		outcome.destroy()
		if next == 0:
			self.play(self.mode,self.ai)
		elif next == 1:
			self.menu()
		else:
			quit()
root = tk.Tk()
root.title("Save Computer Science Chris")
app = Application(master=root)
app.mainloop()
