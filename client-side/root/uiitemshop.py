import ui
import dbg
import constInfo
import player
import event
import playerSettingModule
import uiToolTip
import net
import os
import item
import chat
import grp
import uiCommon
import app
import time
import gameInfo
import webbrowser

FACE_IMAGE_DICT = {
	playerSettingModule.RACE_WARRIOR_M	: "icon/face/warrior_m.tga",
	playerSettingModule.RACE_WARRIOR_W	: "icon/face/warrior_w.tga",
	playerSettingModule.RACE_ASSASSIN_M	: "icon/face/assassin_m.tga",
	playerSettingModule.RACE_ASSASSIN_W	: "icon/face/assassin_w.tga",
	playerSettingModule.RACE_SURA_M		: "icon/face/sura_m.tga",
	playerSettingModule.RACE_SURA_W		: "icon/face/sura_w.tga",
	playerSettingModule.RACE_SHAMAN_M	: "icon/face/shaman_m.tga",
	playerSettingModule.RACE_SHAMAN_W	: "icon/face/shaman_w.tga",
}

PATH = "locale/tr/ui/config/"
EK_X = 130
EK_X2 = 94

class ItemShopWindow(ui.Window):

	SPECIAL_TITLE_COLOR = 0xffFFB96D

	def __init__(self):
		ui.Window.__init__(self)
		self.sayfa = 1
		self.toplam = 0
		self.yer = ""
		self.tek = 0
		self.refresh = 0

		self.full = 0
		self.loading = 0
		self.zaman = app.GetTime()

		self.yers = {}
		self.icons = {}
		self.texts = {}
		self.thinboards = {}
		self.buttons = {}
		self.item = gameInfo.ITEMSHOP_SILAHLAR
		self.item_zirhlar = gameInfo.ITEMSHOP_ZIRHLAR
		self.item_takilar = gameInfo.ITEMSHOP_TAKILAR
		self.item_kalkan_kask = gameInfo.ITEMSHOP_KALKAN_KASK
		self.item_basma = gameInfo.ITEMSHOP_BASMA
		self.item_diger = gameInfo.ITEMSHOP_DIGER
		self.GetItemInfos()
		self.SilahlarGUI()

	def GetItemInfos(self):
		for i in xrange(1,13):
			gameInfo.ITEMSHOP_BEDAVAITEMLER["bedavamenu"+str(i)]={}
			gameInfo.ITEMSHOP_NORMALITEMLER["normalmenu"+str(i)]={}
			gameInfo.ITEMSHOP_SATINALDIKLARIM={}
	
		gameInfo.PYTHONISLEM = "#itemshop_itemleri_al#0#"
		event.QuestButtonClick(gameInfo.PYTHONTOLUA)

	def menuBul(self, gelen):
		for c in xrange(1,13):
			self.menubuttons["button_"+str(c)].Hide()
			
		x = 1
		path = None
		path2= ""
		if gelen=="bedavaedit":
			path=gameInfo.ITEMSHOP_BEDAVAITEMLER
			path2="bedavamenu"
		elif gelen=="normaledit":
			path=gameInfo.ITEMSHOP_NORMALITEMLER
			path2="normalmenu"
		
		for i in xrange(1,13):
			if len(path[str(path2)+str(i)]) > 0:		
				self.menubuttons["button_"+str(x)].SetText(str(path[str(path2)+str(i)+"_isim"]))
				self.menubuttons["button_"+str(x)].SetEvent(ui.__mem_func__(self.ChangeToMenu), self.yer, int(i))
				self.menubuttons["button_"+str(x)].Show()
				x+=1
		
	def __del__(self):
		ui.Window.__del__(self)

	def SilahlarGUI(self):
		global PATH
		global EK_X
		global EK_X2
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetSize(776-8 + EK_X, 528)
		self.Board.SetCenterPosition()
		self.Board.AddFlag('movable')
		self.Board.AddFlag('float')
		self.Board.SetTitleName('Item Shop New Interface')
		self.Board.SetCloseEvent(self.Close)
		self.Board.Show()
		self.__BuildKeyDict()
		self.comp = Component()
		self.toolTip = uiToolTip.ItemToolTip()

		self.sayfa = 1
		self.yer = ""
		self.yer_menu = ""
		self.yers = {}
		self.icons = {}
		self.texts = {}
		self.thinboards = {}
		self.buttons = {}
		self.menubuttons = {}
		self.item = gameInfo.ITEMSHOP_SILAHLAR
		self.item_zirhlar = gameInfo.ITEMSHOP_ZIRHLAR
		self.item_takilar = gameInfo.ITEMSHOP_TAKILAR
		self.item_kalkan_kask = gameInfo.ITEMSHOP_KALKAN_KASK
		self.item_basma = gameInfo.ITEMSHOP_BASMA
		self.item_diger = gameInfo.ITEMSHOP_DIGER
		
		race = net.GetMainActorRace()
		faceImageName = FACE_IMAGE_DICT[race]
		
		self.HesabimThinBoard = self.comp.ThinBoard(self.Board, FALSE, 261, 35, 245, 76, FALSE)
		self.EjderParanThinBoard = self.comp.ThinBoard(self.Board, FALSE, 504, 35, 244, 77, FALSE)
		self.RiotLogoBoard = self.comp.ThinBoard(self.Board, FALSE, 18, 35, 244, 77, FALSE)
		self.MenulerThinBoard = self.comp.ThinBoard(self.Board, FALSE, 140, 112, 514, 65, FALSE)
		self.SilahlarThinBoard = self.comp.ThinBoard(self.Board, FALSE, 34 + EK_X, 179, 692, 337, FALSE)
		
		
		self.KarakterResim = self.comp.ExpandedImage(self.Board , 274, 47, faceImageName)
		self.Epicon = self.comp.ExpandedImage(self.Board , 525, 45, str(PATH)+'itemshop_epicon.tga')
		self.RiotLogo = self.comp.ExpandedImage(self.Board , 26, 34, str(PATH)+'itemshop_logo.tga')
		self.Anasayfa = self.comp.ExpandedImage(self.Board , 134, 198, str(PATH)+'itemshop_giris.tga')
		self.Anasayfa.Hide()
		
		#Giris Butonlari#
		x_giris = 198
		x_arti = 100
		self.BedavaEdit = self.comp.Button(self.Board, 'Bedava Edit', '', x_giris, 130, lambda : self.ChangeToMenu("bedavaedit"), 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.NormalEdit = self.comp.Button(self.Board, 'Normal Edit', '', x_giris + x_arti, 130, lambda : self.ChangeToMenu("normaledit"), 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.SatinAldiklarim = self.comp.Button(self.Board, 'Satýn Aldýklarým', '', x_giris + x_arti*2, 130, lambda : self.ChangeToMenu("satinaldiklarim"), 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.KristalAl = self.comp.Button(self.Board, 'Kristal Al', '', x_giris + x_arti*3, 130, lambda : self.ChangeToMenu("kristalal"), 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		
		self.yukleniyor = self.comp.TextLine(self.Board, '%0', 342-15, 283+8, self.comp.RGB(255, 255, 255))
		self.yukleniyor.SetFontName("Tahoma:60")
		
		x = 19
		y = 12
		y_ek = 24
		self.MenulerThinBoard2 = self.comp.ThinBoard(self.Board, FALSE, 20, 179, 129, 329, FALSE)
		self.MenuButton1 = self.comp.Button(self.MenulerThinBoard2, '', '', x, y, self.bosButton, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.MenuButton2 = self.comp.Button(self.MenulerThinBoard2, '', '', x, y + y_ek, self.bosButton, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.MenuButton3 = self.comp.Button(self.MenulerThinBoard2, '', '', x, y + y_ek*2, self.bosButton, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.MenuButton4 = self.comp.Button(self.MenulerThinBoard2, '', '', x, y + y_ek*3, self.bosButton, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.MenuButton5 = self.comp.Button(self.MenulerThinBoard2, '', '', x, y + y_ek*4, self.bosButton, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.MenuButton6 = self.comp.Button(self.MenulerThinBoard2, '', '', x, y + y_ek*5, self.bosButton, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.MenuButton7 = self.comp.Button(self.MenulerThinBoard2, '', '', x, y + y_ek*6, self.bosButton, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.MenuButton8 = self.comp.Button(self.MenulerThinBoard2, '', '', x, y + y_ek*7, self.bosButton, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.MenuButton9 = self.comp.Button(self.MenulerThinBoard2, '', '', x, y + y_ek*8, self.bosButton, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.MenuButton10 = self.comp.Button(self.MenulerThinBoard2, '', '', x, y + y_ek*9, self.bosButton, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.MenuButton11 = self.comp.Button(self.MenulerThinBoard2, '', '', x, y + y_ek*10, self.bosButton, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.MenuButton12 = self.comp.Button(self.MenulerThinBoard2, '', '', x, y + y_ek*11, self.bosButton, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
	
		self.Epsatinal = self.comp.Button(self.Board, 'Satin al', '', 649, 82, self.Epsatinal_func, 'd:/ymir work/ui/public/small_button_01.sub', 'd:/ymir work/ui/public/small_button_02.sub', 'd:/ymir work/ui/public/small_button_03.sub')
		self.Cikis = self.comp.Button(self.Board, 'Çýkýþ', '', 694, 82, self.Cikis_func, 'd:/ymir work/ui/public/small_button_01.sub', 'd:/ymir work/ui/public/small_button_02.sub', 'd:/ymir work/ui/public/small_button_03.sub')
		#self.EnCokOylu = self.comp.Button(self.Board, 'Aldiklarim', '', 576, 129, self.Aldiklarim_func, 'd:/ymir work/ui/public/middle_button_01.sub', 'd:/ymir work/ui/public/middle_button_02.sub', 'd:/ymir work/ui/public/middle_button_03.sub')
		
		self.EjderhaParamText = self.comp.TextLine(self.Board, 'Ejderha Parasý (EP) : 0', 581, 61, self.comp.RGB(255, 255, 255))
		self.EjderhaParamText.SetText("Ejderha Parasý (EP) : 0")
		self.Merhabatext = self.comp.TextLine(self.Board, 'Merhaba', 354, 49, self.comp.RGB(255, 255, 255))
		self.Merhabatext.SetText("Merhaba " + player.GetName() + "...")
		self.Levelin = self.comp.TextLine(self.Board, 'Levelin :', 354, 63, self.comp.RGB(255, 255, 255))
		self.Levelin.SetText("Levelin : " + str(player.GetStatus(player.LEVEL)))
		self.Songiris = self.comp.TextLine(self.Board, 'Markete en son :', 354-18, 78, self.comp.RGB(255, 255, 255))
		if os.path.exists(str(gameInfo.CLIENT_YOL)+"itemshop_songiris.kf"):
			bugun = time.strftime("%d:%m:%Y")
			bak = open(str(gameInfo.CLIENT_YOL)+"itemshop_songiris.kf", "r").readlines()
			self.Songiris.SetText("Markete en son : " + str(bak) + " girdin.")
			bakyaz = open(str(gameInfo.CLIENT_YOL)+"itemshop_songiris.kf", "w").write(bugun)
		else:
			bugun = time.strftime("%d:%m:%Y")
			ac = open(str(gameInfo.CLIENT_YOL)+"itemshop_songiris.kf", "w").write(str(bugun))
			self.Songiris.SetText("Markete ilk defa girdin.")
		
		self.Ileri = self.comp.Button(self.Board, '>>>', '', 408 + EK_X, 463, self.Ileri_func, 'd:/ymir work/ui/public/small_button_01.sub', 'd:/ymir work/ui/public/small_button_02.sub', 'd:/ymir work/ui/public/small_button_03.sub')
		self.Geri = self.comp.Button(self.Board, '<<<', '', 315 + EK_X, 464, self.Geri_func, 'd:/ymir work/ui/public/small_button_01.sub', 'd:/ymir work/ui/public/small_button_02.sub', 'd:/ymir work/ui/public/small_button_03.sub')
		self.slotbar_SayfaNo, self.SayfaNo = self.comp.EditLine(self.Board, '  1', 365 + EK_X, 466, 35, 15, 5)

		self.yer = "anasayfa"

		# Button's
		self.SatinAl1 = self.comp.Button(self.Board, 'Satýn Al', '', 72 + EK_X, 283, self.SatinAl1, 'd:/ymir work/ui/public/middle_button_01.sub', 'd:/ymir work/ui/public/middle_button_02.sub', 'd:/ymir work/ui/public/middle_button_03.sub')
		self.SatinAl2 = self.comp.Button(self.Board, 'Satýn Al', '', 209 + EK_X, 283, self.SatinAl2, 'd:/ymir work/ui/public/middle_button_01.sub', 'd:/ymir work/ui/public/middle_button_02.sub', 'd:/ymir work/ui/public/middle_button_03.sub')
		self.SatinAl3 = self.comp.Button(self.Board, 'Satýn Al', '', 342 + EK_X, 283, self.SatinAl3, 'd:/ymir work/ui/public/middle_button_01.sub', 'd:/ymir work/ui/public/middle_button_02.sub', 'd:/ymir work/ui/public/middle_button_03.sub')
		self.SatinAl4 = self.comp.Button(self.Board, 'Satýn Al', '', 480 + EK_X, 283, self.SatinAl4, 'd:/ymir work/ui/public/middle_button_01.sub', 'd:/ymir work/ui/public/middle_button_02.sub', 'd:/ymir work/ui/public/middle_button_03.sub')
		self.SatinAl5 = self.comp.Button(self.Board, 'Satýn Al', '', 621 + EK_X, 283, self.SatinAl5, 'd:/ymir work/ui/public/middle_button_01.sub', 'd:/ymir work/ui/public/middle_button_02.sub', 'd:/ymir work/ui/public/middle_button_03.sub')
		self.SatinAl6 = self.comp.Button(self.Board, 'Satýn Al', '', 72 + EK_X, 405, self.SatinAl6, 'd:/ymir work/ui/public/middle_button_01.sub', 'd:/ymir work/ui/public/middle_button_02.sub', 'd:/ymir work/ui/public/middle_button_03.sub')
		self.SatinAl7 = self.comp.Button(self.Board, 'Satýn Al', '', 204 + EK_X, 405, self.SatinAl7, 'd:/ymir work/ui/public/middle_button_01.sub', 'd:/ymir work/ui/public/middle_button_02.sub', 'd:/ymir work/ui/public/middle_button_03.sub')
		self.SatinAl8 = self.comp.Button(self.Board, 'Satýn Al', '', 341 + EK_X, 405, self.SatinAl8, 'd:/ymir work/ui/public/middle_button_01.sub', 'd:/ymir work/ui/public/middle_button_02.sub', 'd:/ymir work/ui/public/middle_button_03.sub')
		self.SatinAl9 = self.comp.Button(self.Board, 'Satýn Al', '', 481 + EK_X, 405, self.SatinAl9, 'd:/ymir work/ui/public/middle_button_01.sub', 'd:/ymir work/ui/public/middle_button_02.sub', 'd:/ymir work/ui/public/middle_button_03.sub')
		self.SatinAl10 = self.comp.Button(self.Board, 'Satýn Al', '', 625 + EK_X, 405, self.SatinAl10, 'd:/ymir work/ui/public/middle_button_01.sub', 'd:/ymir work/ui/public/middle_button_02.sub', 'd:/ymir work/ui/public/middle_button_03.sub')

		# Thinboard's
		self.Thin1 = self.comp.ThinBoard(self.Board, FALSE, 44 + EK_X, 191, 119, 86, FALSE)
		self.Thin2 = self.comp.ThinBoard(self.Board, FALSE, 175 + EK_X, 191, 123, 86, FALSE)
		self.Thin3 = self.comp.ThinBoard(self.Board, FALSE, 310 + EK_X, 191, 123, 88, FALSE)
		self.Thin4 = self.comp.ThinBoard(self.Board, FALSE, 448 + EK_X, 191, 122, 87, FALSE)
		self.Thin5 = self.comp.ThinBoard(self.Board, FALSE, 587 + EK_X, 191, 123, 87, FALSE)
		self.Thin6 = self.comp.ThinBoard(self.Board, FALSE, 45 + EK_X, 311, 120, 87, FALSE)
		self.Thin7 = self.comp.ThinBoard(self.Board, FALSE, 175 + EK_X, 310, 122, 88, FALSE)
		self.Thin8 = self.comp.ThinBoard(self.Board, FALSE, 310 + EK_X, 310, 124, 90, FALSE)
		self.Thin9 = self.comp.ThinBoard(self.Board, FALSE, 448 + EK_X, 310, 126, 91, FALSE)
		self.Thin10 = self.comp.ThinBoard(self.Board, FALSE, 591 + EK_X, 309, 123, 92, FALSE)
		
		self.thinPos = {
			"1": [44,191], "2": [175,191], "3": [310,191], "4": [448,191], "5": [587,191], "6": [44,311], "7": [175,310], "8": [310,310], "9": [448,310], "10": [587,309]
		}
		self.iconPos = {
			"1": [87,194], "2": [220,194], "3": [357,194], "4": [498,194], "5": [636,194], "6": [84,312], "7": [218,312], "8": [352,312], "9": [492,312], "10": [638,312]
		}
		self.textPos = {
			"1": [75-19,255], "2": [201,255], "3": [342-16,255], "4": [484-21,255], "5": [619-20,255], "6": [75-19,377], "7": [201,377], "8": [342,377], "9": [484,377], "10": [639,377]
		}
		
		# Icon's
		self.Icon1 = self.comp.ExpandedImage(self.Board , 87 + EK_X, 194, 'icon/item/00140.tga')
		self.Icon2 = self.comp.ExpandedImage(self.Board , 220 + EK_X, 195, 'icon/item/00140.tga')
		self.Icon3 = self.comp.ExpandedImage(self.Board , 357 + EK_X, 194, 'icon/item/00140.tga')
		self.Icon4 = self.comp.ExpandedImage(self.Board , 498 + EK_X, 195, 'icon/item/00140.tga')
		self.Icon5 = self.comp.ExpandedImage(self.Board , 636 + EK_X, 197, 'icon/item/00140.tga')
		self.Icon6 = self.comp.ExpandedImage(self.Board , 84 + EK_X, 312, 'icon/item/00140.tga')
		self.Icon7 = self.comp.ExpandedImage(self.Board , 218 + EK_X, 312, 'icon/item/00140.tga')
		self.Icon8 = self.comp.ExpandedImage(self.Board , 352 + EK_X, 312, 'icon/item/00140.tga')
		self.Icon9 = self.comp.ExpandedImage(self.Board , 492 + EK_X, 312, 'icon/item/00140.tga')
		self.Icon10 = self.comp.ExpandedImage(self.Board , 638 + EK_X, 313, 'icon/item/00140.tga')

		# Text's
		self.Text1 = self.comp.TextLine(self.Board, "", 75-19 + EK_X, 255, self.comp.RGB(255, 255, 255))
		self.Text2 = self.comp.TextLine(self.Board, '', 201 + EK_X, 257, self.comp.RGB(255, 255, 255))
		self.Text3 = self.comp.TextLine(self.Board, '', 342-16 + EK_X, 258, self.comp.RGB(255, 255, 255))
		self.Text4 = self.comp.TextLine(self.Board, '', 484-21 + EK_X, 258, self.comp.RGB(255, 255, 255))
		self.Text5 = self.comp.TextLine(self.Board, '', 619-20 + EK_X, 258, self.comp.RGB(255, 255, 255))
		self.Text6 = self.comp.TextLine(self.Board, '', 65 + EK_X, 377, self.comp.RGB(255, 255, 255))
		self.Text7 = self.comp.TextLine(self.Board, '', 204-14 + EK_X, 377, self.comp.RGB(255, 255, 255))
		self.Text8 = self.comp.TextLine(self.Board, '', 334-2 + EK_X, 377, self.comp.RGB(255, 255, 255))
		self.Text9 = self.comp.TextLine(self.Board, '', 483-16 + EK_X, 377, self.comp.RGB(255, 255, 255))
		self.Text10 = self.comp.TextLine(self.Board, '', 614 + EK_X, 378, self.comp.RGB(255, 255, 255))

		self.thinboards["thinboard_1"] = self.Thin1
		self.thinboards["thinboard_2"] = self.Thin2
		self.thinboards["thinboard_3"] = self.Thin3
		self.thinboards["thinboard_4"] = self.Thin4
		self.thinboards["thinboard_5"] = self.Thin5
		self.thinboards["thinboard_6"] = self.Thin6
		self.thinboards["thinboard_7"] = self.Thin7
		self.thinboards["thinboard_8"] = self.Thin8
		self.thinboards["thinboard_9"] = self.Thin9
		self.thinboards["thinboard_10"] = self.Thin10
		
		self.icons["icon_1"] = self.Icon1
		self.icons["icon_2"] = self.Icon2
		self.icons["icon_3"] = self.Icon3
		self.icons["icon_4"] = self.Icon4
		self.icons["icon_5"] = self.Icon5
		self.icons["icon_6"] = self.Icon6
		self.icons["icon_7"] = self.Icon7
		self.icons["icon_8"] = self.Icon8
		self.icons["icon_9"] = self.Icon9
		self.icons["icon_10"] = self.Icon10

		self.buttons["button_1"] = self.SatinAl1
		self.buttons["button_2"] = self.SatinAl2
		self.buttons["button_3"] = self.SatinAl3
		self.buttons["button_4"] = self.SatinAl4
		self.buttons["button_5"] = self.SatinAl5
		self.buttons["button_6"] = self.SatinAl6
		self.buttons["button_7"] = self.SatinAl7
		self.buttons["button_8"] = self.SatinAl8
		self.buttons["button_9"] = self.SatinAl9
		self.buttons["button_10"] = self.SatinAl10
		
		self.texts = {}
		self.texts["text_1"] = self.Text1
		self.texts["text_2"] = self.Text2
		self.texts["text_3"] = self.Text3
		self.texts["text_4"] = self.Text4
		self.texts["text_5"] = self.Text5
		self.texts["text_6"] = self.Text6
		self.texts["text_7"] = self.Text7
		self.texts["text_8"] = self.Text8
		self.texts["text_9"] = self.Text9
		self.texts["text_10"] = self.Text10
		
		self.menubuttons["button_1"] = self.MenuButton1
		self.menubuttons["button_2"] = self.MenuButton2
		self.menubuttons["button_3"] = self.MenuButton3
		self.menubuttons["button_4"] = self.MenuButton4
		self.menubuttons["button_5"] = self.MenuButton5
		self.menubuttons["button_6"] = self.MenuButton6
		self.menubuttons["button_7"] = self.MenuButton7
		self.menubuttons["button_8"] = self.MenuButton8
		self.menubuttons["button_9"] = self.MenuButton9
		self.menubuttons["button_10"] = self.MenuButton10
		self.menubuttons["button_11"] = self.MenuButton11
		self.menubuttons["button_12"] = self.MenuButton12

		for c in xrange(1, 11):
			self.icons["icon_"+str(c)].Hide()
			self.buttons["button_"+str(c)].Hide()
			self.texts["text_"+str(c)].Hide()
			self.thinboards["thinboard_"+str(c)].Hide()
			
		for menu in xrange(1, 13):
			self.MenulerThinBoard2.Hide()
			self.menubuttons["button_"+str(menu)].Hide()

		self.yers["yer_bedavaitem"] = self.item
		self.yers["yer_zirhlar"] = self.item_zirhlar
		self.yers["yer_takilar"] = self.item_takilar
		self.yers["yer_kalkan_kask"] = self.item_kalkan_kask
		self.yers["yer_basma"] = self.item_basma
		self.yers["yer_diger"] = self.item_diger

		self.icons["icon_1"].SAFE_SetStringEvent("MOUSE_OVER_IN", self.ShowToolTips)
		self.icons["icon_1"].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.HideToolTips)
	
		self.icons["icon_2"].SAFE_SetStringEvent("MOUSE_OVER_IN", self.ShowToolTips2)
		self.icons["icon_2"].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.HideToolTips)

		self.icons["icon_3"].SAFE_SetStringEvent("MOUSE_OVER_IN", self.ShowToolTips3)
		self.icons["icon_3"].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.HideToolTips)

		self.icons["icon_4"].SAFE_SetStringEvent("MOUSE_OVER_IN", self.ShowToolTips4)
		self.icons["icon_4"].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.HideToolTips)

		self.icons["icon_5"].SAFE_SetStringEvent("MOUSE_OVER_IN", self.ShowToolTips5)
		self.icons["icon_5"].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.HideToolTips)

		self.icons["icon_6"].SAFE_SetStringEvent("MOUSE_OVER_IN", self.ShowToolTips6)
		self.icons["icon_6"].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.HideToolTips)

		self.icons["icon_7"].SAFE_SetStringEvent("MOUSE_OVER_IN", self.ShowToolTips7)
		self.icons["icon_7"].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.HideToolTips)

		self.icons["icon_8"].SAFE_SetStringEvent("MOUSE_OVER_IN", self.ShowToolTips8)
		self.icons["icon_8"].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.HideToolTips)

		self.icons["icon_9"].SAFE_SetStringEvent("MOUSE_OVER_IN", self.ShowToolTips9)
		self.icons["icon_9"].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.HideToolTips)

		self.icons["icon_10"].SAFE_SetStringEvent("MOUSE_OVER_IN", self.ShowToolTips10)
		self.icons["icon_10"].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.HideToolTips)
		
		self.ChangeToMenu("anasayfa")
		
	def bosButton(self):
		pass
		
	def itemBul(self, gelen, gelen_menu):
		if gelen=="bedavaedit":
			return gameInfo.ITEMSHOP_BEDAVAITEMLER["bedavamenu"+str(gelen_menu)]
		elif gelen=="normaledit":
			return gameInfo.ITEMSHOP_NORMALITEMLER["normalmenu"+str(gelen_menu)]
		elif gelen=="satinaldiklarim":
			return gameInfo.ITEMSHOP_SATINALDIKLARIM

	def Ileri_func(self):
		self.sayfa = self.sayfa+1
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10
		siram2 = siram+11
		self.toplam = 0
		self.pos = 0
		self.tek = 0
		
		x2 = self.itemBul(self.yer, self.yer_menu)
		sayfax = self.sayfa
		siramx = sayfax*10+1
		if "item_"+str(siramx) in x2.keys():
			self.Ileri.SetUp()
			self.Ileri.SetUp()
		else:
			self.Ileri.Down()
			self.Ileri.Down()

		for i in xrange(int(siram)+1, int(siram2)):
			self.pos += 1
			if "item_"+str(i) in x2.keys():
				#if self.yer == "silahlar":
				x = self.itemBul(self.yer, self.yer_menu)
				bol = x["item_"+str(i)].split("#")
				item.SelectItem(int(bol[2]))
				item_icon_path = item.GetIconImageFileName()
				#chat.AppendChat(chat.CHAT_TYPE_INFO, "x : " + str(item.GetItemName()))
				ad = item.GetItemName()
				self.texts["text_"+str(self.pos)].SetText(str(item.GetItemName()))

				self.icons["icon_"+str(self.pos)].Show()
				if self.yer!="satinaldiklarim":
					self.buttons["button_"+str(self.pos)].Show()
				else:
					self.buttons["button_"+str(self.pos)].Hide()
				self.texts["text_"+str(self.pos)].Show()
				self.thinboards["thinboard_"+str(self.pos)].Show()

				self.icons["icon_"+str(self.pos)].LoadImage(item_icon_path)
			else:
				self.icons["icon_"+str(self.pos)].Hide()
				self.buttons["button_"+str(self.pos)].Hide()
				self.texts["text_"+str(self.pos)].Hide()
				self.thinboards["thinboard_"+str(self.pos)].Hide()
			
	def Geri_func(self):
		self.sayfa = self.sayfa-1
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10
		siram2 = siram+11
		self.pos = 0
		self.tek = 0
		
		x2 = self.itemBul(self.yer, self.yer_menu)
		if sayfa2 == 0:
			siram = 0
			siram2 = 11
		else:
			sayfax = self.sayfa
			siramx = sayfax*10+1-1
			if "item_"+str(siramx) in x2.keys():
				self.Geri.SetUp()
			else:
				self.Geri.Down()
		

		for i in xrange(int(siram)+1, int(siram2)):
			if self.pos != 10:
				self.pos += 1
			if "item_"+str(i) in x2.keys():
				#if self.yer == "silahlar":
				x = self.itemBul(self.yer, self.yer_menu)
				bol = x["item_"+str(i)].split("#")
				item.SelectItem(int(bol[2]))
				item_icon_path = item.GetIconImageFileName()
				#chat.AppendChat(chat.CHAT_TYPE_INFO, "x : " + str(item.GetItemName()))
				self.texts["text_"+str(self.pos)].SetText(str(item.GetItemName()))

				self.icons["icon_"+str(self.pos)].Show()
				if self.yer!="satinaldiklarim":
					self.buttons["button_"+str(self.pos)].Show()
				else:
					self.buttons["button_"+str(self.pos)].Hide()
				self.texts["text_"+str(self.pos)].Show()
				self.thinboards["thinboard_"+str(self.pos)].Show()

				self.icons["icon_"+str(self.pos)].LoadImage(item_icon_path)
			else:
				self.icons["icon_"+str(self.pos)].Hide()
				self.buttons["button_"+str(self.pos)].Hide()
				self.texts["text_"+str(self.pos)].Hide()
				self.thinboards["thinboard_"+str(self.pos)].Hide()
	
	def normalPosition(self):
		self.SilahlarThinBoard.SetPosition(34, 179)
		self.Board.SetSize(776-8, 528)
		self.HesabimThinBoard.SetPosition(261, 35)
		self.EjderParanThinBoard.SetPosition(504, 35)
		self.RiotLogoBoard.SetPosition(18, 35)
		self.MenulerThinBoard.SetPosition(140, 112)
		self.KarakterResim.SetPosition(274, 47)
		self.Epicon.SetPosition(525, 45)
		self.RiotLogo.SetPosition(26, 34)
		self.Epsatinal.SetPosition(649+9000, 82)
		self.Cikis.SetPosition(694, 82)
		self.EjderhaParamText.SetPosition(581, 61)
		self.Merhabatext.SetPosition(354, 49)
		self.Levelin.SetPosition(354, 63)
		self.Songiris.SetPosition(354-18, 78)
		x_giris = 198
		x_arti = 100
		self.BedavaEdit.SetPosition(x_giris, 130)
		self.NormalEdit.SetPosition(x_giris + x_arti, 130)
		self.SatinAldiklarim.SetPosition(x_giris + x_arti*2, 130)
		self.KristalAl.SetPosition(x_giris + x_arti*3, 130)
	
	def ChangeToMenu(self, gelen, gelen_menu=1):
		global EK_X
		global EK_X2
		
		if gelen=="kristalal":
			webbrowser.open(str(gameInfo.ITEMSHOP_SITE))
			return
			
		self.Ileri.Hide()
		self.Geri.Hide()
		self.SayfaNo.Hide()
		self.slotbar_SayfaNo.Hide()
		self.Anasayfa.Hide()
		
		for i in xrange(1, 11):
			self.icons["icon_"+str(i)].Hide()
			self.buttons["button_"+str(i)].Hide()
			self.texts["text_"+str(i)].Hide()
			self.thinboards["thinboard_"+str(i)].Hide()
			
		if gelen=="anasayfa":
			self.SilahlarThinBoard.SetPosition(34, 179)
			self.Board.SetSize(776-8, 528)
			self.Anasayfa.Show()
			self.normalPosition()
			return
		
		
		
		x_giris = 198
		x_arti = 100
		self.SilahlarThinBoard.SetPosition(34+EK_X, 179)
		self.Board.SetSize(776-8 + EK_X, 528)
		self.HesabimThinBoard.SetPosition(261 + EK_X2, 35)
		self.EjderParanThinBoard.SetPosition(504 + EK_X2, 35)
		self.RiotLogoBoard.SetPosition(18 + EK_X2, 35)
		self.MenulerThinBoard.SetPosition(140 + EK_X2, 112)
		self.KarakterResim.SetPosition(274 + EK_X2, 47)
		self.Epicon.SetPosition(525 + EK_X2, 45)
		self.RiotLogo.SetPosition(26 + EK_X2, 34)
		self.Epsatinal.SetPosition(649 + EK_X2 + 9000, 82)
		self.Cikis.SetPosition(694 + EK_X2, 82)
		self.EjderhaParamText.SetPosition(581 + EK_X2, 61)
		self.Merhabatext.SetPosition(354 + EK_X2, 49)
		self.Levelin.SetPosition(354 + EK_X2, 63)
		self.Songiris.SetPosition(354-18 + EK_X2, 78)
		
		self.BedavaEdit.SetPosition(x_giris + EK_X2, 130)
		self.NormalEdit.SetPosition(x_giris + x_arti + EK_X2, 130)
		self.SatinAldiklarim.SetPosition(x_giris + x_arti*2 + EK_X2, 130)
		self.KristalAl.SetPosition(x_giris + x_arti*3 + EK_X2, 130)
		
		
		if gelen=="satinaldiklarim":
			self.normalPosition()
			self.MenulerThinBoard2.Hide()
			self.SilahlarThinBoard.SetPosition(34, 179)
			self.Board.SetSize(776-8, 528)
			for i in xrange(1,13):
				self.menubuttons["button_"+str(i)].Hide()
			self.Ileri.SetPosition(408,463)
			self.Geri.SetPosition(315,464)
			#self.SayfaNo.SetPosition(365,466)
			self.slotbar_SayfaNo.SetPosition(365,466)
			for c in xrange(1, 11):
				self.icons["icon_"+str(c)].SetPosition(self.iconPos[str(c)][0], self.iconPos[str(c)][1])
				self.texts["text_"+str(c)].SetPosition(self.textPos[str(c)][0], self.textPos[str(c)][1])
				self.thinboards["thinboard_"+str(c)].SetPosition(self.thinPos[str(c)][0], self.thinPos[str(c)][1])
		else:
			for menu in xrange(1, 13):
				self.MenulerThinBoard2.Show()
				self.menubuttons["button_"+str(menu)].Show()
			
		self.Ileri.Show()
		self.Geri.Show()
		self.SayfaNo.Show()
		self.slotbar_SayfaNo.Show()
		
		self.yer = gelen
		self.yer_menu = gelen_menu
		self.pos = 0
		self.toplam = 0
		self.sayfa = 1
		
		x=None
		
		if gelen == "satinaldiklarim":
			x = gameInfo.ITEMSHOP_SATINALDIKLARIM
		else:
			self.Ileri.SetPosition(408+EK_X,463)
			self.Geri.SetPosition(315+EK_X,464)
			#self.SayfaNo.SetPosition(365+EK_X,466)
			self.slotbar_SayfaNo.SetPosition(365+EK_X,466)
			for c in xrange(1, 11):
				self.icons["icon_"+str(c)].SetPosition(self.iconPos[str(c)][0] + EK_X, self.iconPos[str(c)][1])
				self.texts["text_"+str(c)].SetPosition(self.textPos[str(c)][0] + EK_X, self.textPos[str(c)][1])
				self.thinboards["thinboard_"+str(c)].SetPosition(self.thinPos[str(c)][0] + EK_X, self.thinPos[str(c)][1])
			
			x = self.itemBul(gelen, gelen_menu)
			self.menuBul(gelen)
			
		for i in xrange(1, 11):
			if "item_"+str(i) in x.keys():
				
				x2 = self.itemBul(self.yer, self.yer_menu)
				bol = x2["item_"+str(i)].split("#")
				item.SelectItem(int(bol[2]))
				item_icon_path = item.GetIconImageFileName()
				self.texts["text_"+str(i)].SetText(str(item.GetItemName()))

				self.icons["icon_"+str(i)].Show()
				if gelen!="satinaldiklarim":
					self.buttons["button_"+str(i)].Show()
				else:
					self.buttons["button_"+str(i)].Hide()
				self.texts["text_"+str(i)].Show()
				self.thinboards["thinboard_"+str(i)].Show()

				self.icons["icon_"+str(i)].LoadImage(item_icon_path)
				self.toplam += 1
			else:
				self.icons["icon_"+str(i)].Hide()
				self.buttons["button_"+str(i)].Hide()
				self.texts["text_"+str(i)].Hide()
				self.thinboards["thinboard_"+str(i)].Hide()
				
		self.SetCenterPosition()

	def Pass_func(self):
		pass
	def Pass_func2(self):
		pass
	def Pass_func3(self):
		pass
	def Pass_func4(self):
		pass
	def Pass_func5(self):
		pass
	def Pass_func6(self):
		pass
	def Pass_func7(self):
		pass
	def Pass_func8(self):
		pass
	def Pass_func9(self):
		pass
	def Pass_func10(self):
		pass
	def PassFunc(self):
		pass

	def Yap(self):
		self.EjderhaParamText.SetText("Ejderha Parasý (EP) : 0")
	
	def ShowToolTips(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10
		siram = siram+1
	
		#chat.AppendChat(chat.CHAT_TYPE_INFO, str(siram))

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		self.toolTip.ClearToolTip()

		#self.toolTip.AddRefineItemData(int(bol[2]), [int(bol[4]),int(bol[5]),int(bol[6]),int(bol[7]),int(bol[8]),int(bol[9])],  [(int(bol[10]),int(bol[11])),(int(bol[12]),int(bol[13])),(int(bol[14]),int(bol[15])),(int(bol[16]),int(bol[17])),(int(bol[18]),int(bol[19])),(int(bol[20]),int(bol[21])),(int(bol[22]),int(bol[23]))])
		self.toolTip.AppendTextLine(str(bol[25]) + " EP")
		if self.yer == "satinaldiklarim":
			self.toolTip.AppendTextLine("Tarihi : " + str(bol[26]))
		self.toolTip.AddRefineItemData(int(bol[2]), [int(bol[5]),int(bol[6]),int(bol[7]),int(bol[8]),int(bol[9]),int(bol[10])],  [(int(bol[11]),int(bol[12])),(int(bol[13]),int(bol[14])),(int(bol[15]),int(bol[16])),(int(bol[17]),int(bol[18])),(int(bol[19]),int(bol[20])),(int(bol[21]),int(bol[22])),(int(bol[23]),int(bol[24]))])

		#metinSlot = [player.GetItemMetinSocket(int(bol[2]), i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		#attrSlot = [player.GetItemAttribute(int(bol[2]), i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
		#self.toolTip.AddRefineItemData(int(bol[2]), metinSlot, attrSlot)

		#self.toolTip.AppendSpace(3)
		#SPECIAL_TITLE_COLOR = 0xffFFB96D
		#self.toolTip.AppendTextLine("10 EP")

	
	def ShowToolTips2(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10
		siram = siram+2
	
		#chat.AppendChat(chat.CHAT_TYPE_INFO, str(siram))

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		self.toolTip.ClearToolTip()

		self.toolTip.AppendTextLine(str(bol[25]) + " EP")
		if self.yer == "satinaldiklarim":
			self.toolTip.AppendTextLine("Tarihi : " + str(bol[26]))
		self.toolTip.AddRefineItemData(int(bol[2]), [int(bol[5]),int(bol[6]),int(bol[7]),int(bol[8]),int(bol[9]),int(bol[10])],  [(int(bol[11]),int(bol[12])),(int(bol[13]),int(bol[14])),(int(bol[15]),int(bol[16])),(int(bol[17]),int(bol[18])),(int(bol[19]),int(bol[20])),(int(bol[21]),int(bol[22])),(int(bol[23]),int(bol[24]))])

	
	def ShowToolTips3(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10
		siram = siram+3
	
		#chat.AppendChat(chat.CHAT_TYPE_INFO, str(siram))

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		self.toolTip.ClearToolTip()

		self.toolTip.AppendTextLine(str(bol[25]) + " EP")
		if self.yer == "satinaldiklarim":
			self.toolTip.AppendTextLine("Tarihi : " + str(bol[26]))
		self.toolTip.AddRefineItemData(int(bol[2]), [int(bol[5]),int(bol[6]),int(bol[7]),int(bol[8]),int(bol[9]),int(bol[10])],  [(int(bol[11]),int(bol[12])),(int(bol[13]),int(bol[14])),(int(bol[15]),int(bol[16])),(int(bol[17]),int(bol[18])),(int(bol[19]),int(bol[20])),(int(bol[21]),int(bol[22])),(int(bol[23]),int(bol[24]))])

	
	def ShowToolTips4(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10
		siram = siram+4
	
		#chat.AppendChat(chat.CHAT_TYPE_INFO, str(siram))

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		self.toolTip.ClearToolTip()

		self.toolTip.AppendTextLine(str(bol[25]) + " EP")
		if self.yer == "satinaldiklarim":
			self.toolTip.AppendTextLine("Tarihi : " + str(bol[26]))
		self.toolTip.AddRefineItemData(int(bol[2]), [int(bol[5]),int(bol[6]),int(bol[7]),int(bol[8]),int(bol[9]),int(bol[10])],  [(int(bol[11]),int(bol[12])),(int(bol[13]),int(bol[14])),(int(bol[15]),int(bol[16])),(int(bol[17]),int(bol[18])),(int(bol[19]),int(bol[20])),(int(bol[21]),int(bol[22])),(int(bol[23]),int(bol[24]))])

	def ShowToolTips5(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10
		siram = siram+5
	
		#chat.AppendChat(chat.CHAT_TYPE_INFO, str(siram))

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		self.toolTip.ClearToolTip()

		self.toolTip.AppendTextLine(str(bol[25]) + " EP")
		if self.yer == "satinaldiklarim":
			self.toolTip.AppendTextLine("Tarihi : " + str(bol[26]))
		self.toolTip.AddRefineItemData(int(bol[2]), [int(bol[5]),int(bol[6]),int(bol[7]),int(bol[8]),int(bol[9]),int(bol[10])],  [(int(bol[11]),int(bol[12])),(int(bol[13]),int(bol[14])),(int(bol[15]),int(bol[16])),(int(bol[17]),int(bol[18])),(int(bol[19]),int(bol[20])),(int(bol[21]),int(bol[22])),(int(bol[23]),int(bol[24]))])

	def ShowToolTips6(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10
		siram = siram+6
	
		#chat.AppendChat(chat.CHAT_TYPE_INFO, str(siram))

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		self.toolTip.ClearToolTip()

		self.toolTip.AppendTextLine(str(bol[25]) + " EP")
		if self.yer == "satinaldiklarim":
			self.toolTip.AppendTextLine("Tarihi : " + str(bol[26]))
		self.toolTip.AddRefineItemData(int(bol[2]), [int(bol[5]),int(bol[6]),int(bol[7]),int(bol[8]),int(bol[9]),int(bol[10])],  [(int(bol[11]),int(bol[12])),(int(bol[13]),int(bol[14])),(int(bol[15]),int(bol[16])),(int(bol[17]),int(bol[18])),(int(bol[19]),int(bol[20])),(int(bol[21]),int(bol[22])),(int(bol[23]),int(bol[24]))])

	def ShowToolTips7(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10
		siram = siram+7
	
		#chat.AppendChat(chat.CHAT_TYPE_INFO, str(siram))

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		self.toolTip.ClearToolTip()

		self.toolTip.AppendTextLine(str(bol[25]) + " EP")
		if self.yer == "satinaldiklarim":
			self.toolTip.AppendTextLine("Tarihi : " + str(bol[26]))
		self.toolTip.AddRefineItemData(int(bol[2]), [int(bol[5]),int(bol[6]),int(bol[7]),int(bol[8]),int(bol[9]),int(bol[10])],  [(int(bol[11]),int(bol[12])),(int(bol[13]),int(bol[14])),(int(bol[15]),int(bol[16])),(int(bol[17]),int(bol[18])),(int(bol[19]),int(bol[20])),(int(bol[21]),int(bol[22])),(int(bol[23]),int(bol[24]))])

	def ShowToolTips8(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10
		siram = siram+8
	
		#chat.AppendChat(chat.CHAT_TYPE_INFO, str(siram))

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		self.toolTip.ClearToolTip()

		self.toolTip.AppendTextLine(str(bol[25]) + " EP")
		if self.yer == "satinaldiklarim":
			self.toolTip.AppendTextLine("Tarihi : " + str(bol[26]))
		self.toolTip.AddRefineItemData(int(bol[2]), [int(bol[5]),int(bol[6]),int(bol[7]),int(bol[8]),int(bol[9]),int(bol[10])],  [(int(bol[11]),int(bol[12])),(int(bol[13]),int(bol[14])),(int(bol[15]),int(bol[16])),(int(bol[17]),int(bol[18])),(int(bol[19]),int(bol[20])),(int(bol[21]),int(bol[22])),(int(bol[23]),int(bol[24]))])

	def ShowToolTips9(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10
		siram = siram+9
	
		#chat.AppendChat(chat.CHAT_TYPE_INFO, str(siram))

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		self.toolTip.ClearToolTip()

		self.toolTip.AppendTextLine(str(bol[25]) + " EP")
		if self.yer == "satinaldiklarim":
			self.toolTip.AppendTextLine("Tarihi : " + str(bol[26]))
		self.toolTip.AddRefineItemData(int(bol[2]), [int(bol[5]),int(bol[6]),int(bol[7]),int(bol[8]),int(bol[9]),int(bol[10])],  [(int(bol[11]),int(bol[12])),(int(bol[13]),int(bol[14])),(int(bol[15]),int(bol[16])),(int(bol[17]),int(bol[18])),(int(bol[19]),int(bol[20])),(int(bol[21]),int(bol[22])),(int(bol[23]),int(bol[24]))])

	
	def ShowToolTips10(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10
		siram = siram+10
	
		#chat.AppendChat(chat.CHAT_TYPE_INFO, str(siram))

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		self.toolTip.ClearToolTip()

		self.toolTip.AppendTextLine(str(bol[25]) + " EP")
		if self.yer == "satinaldiklarim":
			self.toolTip.AppendTextLine("Tarihi : " + str(bol[26]))
		self.toolTip.AddRefineItemData(int(bol[2]), [int(bol[5]),int(bol[6]),int(bol[7]),int(bol[8]),int(bol[9]),int(bol[10])],  [(int(bol[11]),int(bol[12])),(int(bol[13]),int(bol[14])),(int(bol[15]),int(bol[16])),(int(bol[17]),int(bol[18])),(int(bol[19]),int(bol[20])),(int(bol[21]),int(bol[22])),(int(bol[23]),int(bol[24]))])

	def HideToolTips(self):
		self.toolTip.Hide()
		
	def SatinAl1(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10
		siram = siram+1

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		itemadi = item.GetItemName()
		self.itemBuyQuestionDialog2 = uiCommon.QuestionDialog()
		self.itemBuyQuestionDialog2.SetText(itemadi + "'u " + str(bol[25]) + " EP'e satin almak istiyormusun?")
		self.itemBuyQuestionDialog2.SetAcceptEvent(lambda : self.SatinAl_ToQuest(siram))
		self.itemBuyQuestionDialog2.SetCancelEvent(self.CloseWindow)
		self.itemBuyQuestionDialog2.Open()
	
	def SatinAl2(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10+2

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		itemadi = item.GetItemName()
		self.itemBuyQuestionDialog2 = uiCommon.QuestionDialog()
		self.itemBuyQuestionDialog2.SetText(itemadi + "'u " + str(bol[25]) + " EP'e satin almak istiyormusun?")
		self.itemBuyQuestionDialog2.SetAcceptEvent(lambda : self.SatinAl_ToQuest(siram))
		self.itemBuyQuestionDialog2.SetCancelEvent(self.CloseWindow)
		self.itemBuyQuestionDialog2.Open()

	def SatinAl3(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10+3

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		itemadi = item.GetItemName()
		self.itemBuyQuestionDialog2 = uiCommon.QuestionDialog()
		self.itemBuyQuestionDialog2.SetText(itemadi + "'u " + str(bol[25]) + " EP'e satin almak istiyormusun?")
		self.itemBuyQuestionDialog2.SetAcceptEvent(lambda : self.SatinAl_ToQuest(siram))
		self.itemBuyQuestionDialog2.SetCancelEvent(self.CloseWindow)
		self.itemBuyQuestionDialog2.Open()

	def SatinAl4(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10+4

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		itemadi = item.GetItemName()
		self.itemBuyQuestionDialog2 = uiCommon.QuestionDialog()
		self.itemBuyQuestionDialog2.SetText(itemadi + "'u " + str(bol[25]) + " EP'e satin almak istiyormusun?")
		self.itemBuyQuestionDialog2.SetAcceptEvent(lambda : self.SatinAl_ToQuest(siram))
		self.itemBuyQuestionDialog2.SetCancelEvent(self.CloseWindow)
		self.itemBuyQuestionDialog2.Open()

	def SatinAl5(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10+5

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		itemadi = item.GetItemName()
		self.itemBuyQuestionDialog2 = uiCommon.QuestionDialog()
		self.itemBuyQuestionDialog2.SetText(itemadi + "'u " + str(bol[25]) + " EP'e satin almak istiyormusun?")
		self.itemBuyQuestionDialog2.SetAcceptEvent(lambda : self.SatinAl_ToQuest(siram))
		self.itemBuyQuestionDialog2.SetCancelEvent(self.CloseWindow)
		self.itemBuyQuestionDialog2.Open()

	def SatinAl6(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10+6

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		itemadi = item.GetItemName()
		self.itemBuyQuestionDialog2 = uiCommon.QuestionDialog()
		self.itemBuyQuestionDialog2.SetText(itemadi + "'u " + str(bol[25]) + " EP'e satin almak istiyormusun?")
		self.itemBuyQuestionDialog2.SetAcceptEvent(lambda : self.SatinAl_ToQuest(siram))
		self.itemBuyQuestionDialog2.SetCancelEvent(self.CloseWindow)
		self.itemBuyQuestionDialog2.Open()

	def SatinAl7(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10+7

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		itemadi = item.GetItemName()
		self.itemBuyQuestionDialog2 = uiCommon.QuestionDialog()
		self.itemBuyQuestionDialog2.SetText(itemadi + "'u " + str(bol[25]) + " EP'e satin almak istiyormusun?")
		self.itemBuyQuestionDialog2.SetAcceptEvent(lambda : self.SatinAl_ToQuest(siram))
		self.itemBuyQuestionDialog2.SetCancelEvent(self.CloseWindow)
		self.itemBuyQuestionDialog2.Open()

	def SatinAl8(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10+8

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		itemadi = item.GetItemName()
		self.itemBuyQuestionDialog2 = uiCommon.QuestionDialog()
		self.itemBuyQuestionDialog2.SetText(itemadi + "'u " + str(bol[25]) + " EP'e satin almak istiyormusun?")
		self.itemBuyQuestionDialog2.SetAcceptEvent(lambda : self.SatinAl_ToQuest(siram))
		self.itemBuyQuestionDialog2.SetCancelEvent(self.CloseWindow)
		self.itemBuyQuestionDialog2.Open()

	def SatinAl9(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10+9

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		itemadi = item.GetItemName()
		self.itemBuyQuestionDialog2 = uiCommon.QuestionDialog()
		self.itemBuyQuestionDialog2.SetText(itemadi + "'u " + str(bol[25]) + " EP'e satin almak istiyormusun?")
		self.itemBuyQuestionDialog2.SetAcceptEvent(lambda : self.SatinAl_ToQuest(siram))
		self.itemBuyQuestionDialog2.SetCancelEvent(self.CloseWindow)
		self.itemBuyQuestionDialog2.Open()

	def SatinAl10(self):
		sayfa = self.sayfa
		sayfa2 = self.sayfa-1
		siram = sayfa2*10+10

		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(siram)].split("#")

		item.SelectItem(int(bol[2]))
		itemadi = item.GetItemName()
		self.itemBuyQuestionDialog2 = uiCommon.QuestionDialog()
		self.itemBuyQuestionDialog2.SetText(itemadi + "'u " + str(bol[25]) + " EP'e satin almak istiyormusun?")
		self.itemBuyQuestionDialog2.SetAcceptEvent(lambda : self.SatinAl_ToQuest(siram))
		self.itemBuyQuestionDialog2.SetCancelEvent(self.CloseWindow)
		self.itemBuyQuestionDialog2.Open()
	
	def SatinAl_ToQuest(self, sira):
		if gameInfo.ITEMSHOP_OPEN == 0:
			gameInfo.ITEMSHOP_OPEN=1
			gameInfo.ITEMSHOP_TIME=app.GetTime()+gameInfo.ITEMSHOP_SATINALMA_SURESI
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Tekrardan item satýn alabilmek için " + str(gameInfo.ITEMSHOP_SATINALMA_SURESI) + " saniye beklemelisin.")
			self.itemBuyQuestionDialog2.Close()
			return
			
		x = self.itemBul(self.yer, self.yer_menu)
		bol = x["item_"+str(sira)].split("#")

		if self.yer != "bedavaedit":
			gameInfo.ITEMSHOP_SATINALDIKLARIM = {}
		
		gameInfo.PYTHONISLEM = "#itemshop_itemleri_al#1#"+str(sira)+"#"+str(self.yer)+"#"+str(bol[2])+"#"+str(self.yer_menu)
		event.QuestButtonClick(gameInfo.PYTHONTOLUA)
		
		#chat.AppendChat(chat.CHAT_TYPE_INFO, "Satýn almak istediðin item sýrasý : " + str(sira))
		self.itemBuyQuestionDialog2.Close()
		
	def CloseWindow(self):
		self.itemBuyQuestionDialog2.Close()
	
	def Epsatinal_func(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Gerekli bilgiler metin2 klasörüne,itemshop.txt adli dosya olarak kaydedildi.")
		bankatxtac = open("itemshop.txt", "w+")
		bankatxtac.write("ItemShop - Ep Fiyatlari"+"\n")
		bankatxtac.write("10EP - 10TL"+"\n")
		bankatxtac.write("15EP - 15TL"+"\n")
		bankatxtac.write("20EP - 20TL"+"\n")
		bankatxtac.write("30EP - 30TL"+"\n")
		bankatxtac.write("40EP - 40TL"+"\n")
		bankatxtac.write("50EP - 50TL"+"\n")
		bankatxtac.write("60EP - 60TL"+"\n")
		bankatxtac.write("70EP - 70TL"+"\n")
		bankatxtac.write("80EP - 80TL"+"\n")
		bankatxtac.write("90EP - 85TL"+"\n")
		bankatxtac.write("100EP - 90TL"+"\n")
		bankatxtac.write("150EP - 140TL"+"\n")
		bankatxtac.write("170EP - 160TL"+"\n")
		bankatxtac.write("200EP - 180TL"+"\n")
		bankatxtac.write("250EP - 240TL"+"\n")
		bankatxtac.write("500EP - 450TL"+"\n"+"\n"+"\n")
		bankatxtac.write("Riot2 - Banka Numaralari"+"\n"+"\n")
		bankatxtac.write("GARANTÝ VSVS.V.S.VS.V.SVS."+"\n")
		bankatxtac.write("Parayi yolladiktan sonra siteden bildirim yapabilirsiniz."+"\n"+"\n"+"\n")
		bankatxtac.write("RIOT2 - IYI SATÝÞLAR DÝLER.")
	
	def Cikis_func(self):
		self.Close()

	def __BuildKeyDict(self):
		onPressKeyDict = {}
		onPressKeyDict[app.DIK_F6]	= lambda : self.OpenWindow()
		self.onPressKeyDict = onPressKeyDict
	
	def OnKeyDown(self, key):
		try:
			self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise
		return TRUE
	
	def OpenWindow(self):
		if self.Board.IsShow():
			self.Board.Hide()
		else:
			self.Board.Show()
	
	def Close(self):
		gameInfo.ITEMSHOP_ACIK = 0
		self.Board.Hide()
	
	def OnUpdate(self):
		if gameInfo.ITEMSHOP_ACIK == 2:
			self.Close()
		self.SayfaNo.SetText("	  "+str(self.sayfa))
		if self.sayfa == 1:
			self.Geri.Down()
			self.Geri.Disable()
		else:
			if self.tek == 0:
				self.Geri.SetUp()
				self.Geri.Enable()
				self.tek = 1
		
		if self.full < 102:
			self.yukleniyor.Hide()
			#self.yukleniyor.SetFontName("Tahoma:60")
			#self.yukleniyor.SetText("%"+str(self.full))
			#self.full += 1

		if self.full == 101 and self.loading == 0:
			self.yukleniyor.Hide()
			self.loading = 1
			
		if self.yer != "anasayfa":
			if app.GetTime() < self.zaman + 2:
				self.Ileri.Hide()
				self.Geri.Hide()
				self.SayfaNo.Hide()
				self.slotbar_SayfaNo.Hide()
			else:
				self.Ileri.Show()
				self.Geri.Show()
				self.SayfaNo.Show()
				self.slotbar_SayfaNo.Show()
				

		self.EjderhaParamText.SetText("Ejderha Parasý (EP) : " + str(gameInfo.ITEMSHOP_EP))

class Component:
	def Button(self, parent, buttonName, tooltipText, x, y, func, UpVisual, OverVisual, DownVisual):
		button = ui.Button()
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(UpVisual)
		button.SetOverVisual(OverVisual)
		button.SetDownVisual(DownVisual)
		button.SetText(buttonName)
		button.SetToolTipText(tooltipText)
		button.Show()
		button.SetEvent(func)
		return button

	def Button_Tool(self, parent, buttonName, tooltipText, x, y, func, UpVisual, OverVisual, DownVisual):
		button = ui.Button_Alisveris()
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(UpVisual)
		button.SetOverVisual(OverVisual)
		button.SetDownVisual(DownVisual)
		button.SetText(buttonName)
		#button.SetToolTipImage(tooltipText)
		button.Show()
		button.SetEvent(func)
		return button

	def ToggleButton(self, parent, buttonName, tooltipText, x, y, funcUp, funcDown, UpVisual, OverVisual, DownVisual):
		button = ui.ToggleButton()
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(UpVisual)
		button.SetOverVisual(OverVisual)
		button.SetDownVisual(DownVisual)
		button.SetText(buttonName)
		button.SetToolTipText(tooltipText)
		button.Show()
		button.SetToggleUpEvent(funcUp)
		button.SetToggleDownEvent(funcDown)
		return button

	def EditLine(self, parent, editlineText, x, y, width, heigh, max):
		SlotBar = ui.SlotBar()
		if parent != None:
			SlotBar.SetParent(parent)
		SlotBar.SetSize(width, heigh)
		SlotBar.SetPosition(x, y)
		SlotBar.Show()
		Value = ui.EditLine()
		Value.SetParent(SlotBar)
		Value.SetSize(width, heigh)
		Value.SetPosition(1, 1)
		Value.SetMax(max)
		Value.SetLimitWidth(width)
		Value.SetMultiLine()
		Value.SetText(editlineText)
		Value.Show()
		return SlotBar, Value

	def TextLine(self, parent, textlineText, x, y, color):
		textline = ui.TextLine()
		if parent != None:
			textline.SetParent(parent)
		textline.SetPosition(x, y)
		if color != None:
			textline.SetFontColor(color[0], color[1], color[2])
		textline.SetText(textlineText)
		textline.Show()
		return textline

	def RGB(self, r, g, b):
		return (r*255, g*255, b*255)

	def SliderBar(self, parent, sliderPos, func, x, y):
		Slider = ui.SliderBar()
		if parent != None:
			Slider.SetParent(parent)
		Slider.SetPosition(x, y)
		Slider.SetSliderPos(sliderPos / 100)
		Slider.Show()
		Slider.SetEvent(func)
		return Slider

	def ExpandedImage(self, parent, x, y, img):
		image = ui.ImageBox()
		if parent != None:
			image.SetParent(parent)
		image.SetPosition(x, y)
		image.LoadImage(img)
		image.Show()
		return image

	def Button_Tool33(self, parent, x, y, img):
		image = ui.Button_Alisveris()
		if parent != None:
			image.SetParent(parent)
		image.SetPosition(x, y)
		image.SetUpVisual(img)
		image.SetOverVisual(img)
		image.SetDownVisual(img)
		image.Show()
		return image
		
	#def ExpandedImage(self, parent, x, y, img):
		#image = ui.ExpandedImageBox()
		#if parent != None:
			#image.SetParent(parent)
		#image.SetPosition(x, y)
		#image.LoadImage(img)
		#image.Show()
		#return image

	def ComboBox(self, parent, text, x, y, width):
		combo = ui.ComboBox()
		if parent != None:
			combo.SetParent(parent)
		combo.SetPosition(x, y)
		combo.SetSize(width, 15)
		combo.SetCurrentItem(text)
		combo.Show()
		return combo

	def ThinBoard(self, parent, moveable, x, y, width, heigh, center):
		thin = ui.ThinBoard()
		if parent != None:
			thin.SetParent(parent)
		if moveable == TRUE:
			thin.AddFlag('movable')
			thin.AddFlag('float')
		thin.SetSize(width, heigh)
		thin.SetPosition(x, y)
		if center == TRUE:
			thin.SetCenterPosition()
		thin.Show()
		return thin

	def Gauge(self, parent, width, color, x, y):
		gauge = ui.Gauge()
		if parent != None:
			gauge.SetParent(parent)
		gauge.SetPosition(x, y)
		gauge.MakeGauge(width, color)
		gauge.Show()
		return gauge

	def ListBoxEx(self, parent, x, y, width, heigh):
		bar = ui.Bar()
		if parent != None:
			bar.SetParent(parent)
		bar.SetPosition(x, y)
		bar.SetSize(width, heigh)
		bar.SetColor(0x77000000)
		bar.Show()
		ListBox=ui.ListBoxEx()
		ListBox.SetParent(bar)
		ListBox.SetPosition(0, 0)
		ListBox.SetSize(width, heigh)
		ListBox.Show()
		scroll = ui.ScrollBar()
		scroll.SetParent(ListBox)
		scroll.SetPosition(width-15, 0)
		scroll.SetScrollBarSize(heigh)
		scroll.Show()
		ListBox.SetScrollBar(scroll)
		return bar, ListBox

#ShopMarketAnaMenu().Show()
