import gameInfo
import uiitemshop

	## Call Button ##
	def OpenItemShop(self):
		if gameInfo.ITEMSHOP_ACIK == 0:
			import uiitemshop
			self.ac = uiitemshop.ItemShopWindow()
			self.ac.Show()
			gameInfo.ITEMSHOP_ACIK = 1

	
	def __ServerCommand_Build(self):
		serverCommandList={

			## New System Plugin ##
			"PythonToLua"			: self.__PythonToLua, # .python to Quest
			"PythonIslem"			: self.__PythonIslem, # .python to Quest
			"LuaToPython"			: self.__LuaToPython, # Quest to .python
			## END - New System Plugin - END ##

		}

	##replace the funtion##
	def OpenQuestWindow(self, skin, idx):
		if gameInfo.INPUT == 1:
			return
		self.interface.OpenQuestWindow(skin, idx)

	##add the new funtions##
	
	def OnUpdate(self):
		if gameInfo.ITEMSHOP_OPEN == 1:
			if gameInfo.ITEMSHOP_TIME < app.GetTime():
				gameInfo.ITEMSHOP_OPEN = 0
				gameInfo.ITEMSHOP_TIME = 0
	
	def __PythonToLua(self, id):
		gameInfo.PYTHONTOLUA = int(id)

	def __PythonIslem(self, PythonIslem):
		if PythonIslem == "PYTHONISLEM":
			net.SendQuestInputStringPacket(gameInfo.PYTHONISLEM)

	def __LuaToPython(self, LuaToPython):
		if LuaToPython.find("#quest_input#") != -1:
			gameInfo.INPUT = 1
		elif LuaToPython.find("#quest_inputbitir#") != -1:
			gameInfo.INPUT = 0

		elif LuaToPython.find("itemshop_itemler") != -1:
			bol = LuaToPython.split("#")
			bol2 = LuaToPython.split("|")
			bol3 = LuaToPython.split("!")
			
			if LuaToPython.find("bedavamenu") != -1: gameInfo.ITEMSHOP_BEDAVAITEMLER[str(bol3[1])]["item_"+str(bol[1])] = bol2[2]
			elif LuaToPython.find("normalmenu") != -1: gameInfo.ITEMSHOP_NORMALITEMLER[str(bol3[1])]["item_"+str(bol[1])] = bol2[2]
			elif LuaToPython.find("satinaldiklarim") != -1: gameInfo.ITEMSHOP_SATINALDIKLARIM["item_"+str(bol[1])] = bol2[2]
			
			elif LuaToPython.find("yeterliepyok") != -1:
				self.parayok = uiCommon.PopupDialog()
				self.parayok.SetText("Yeterli ep yok.")
				self.parayok.Open()
			
			elif LuaToPython.find("yang") != -1:
				gameInfo.ITEMSHOP_EP = int(bol2[2])