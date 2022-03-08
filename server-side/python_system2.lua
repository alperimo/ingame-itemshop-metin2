--[[

TR: Tüm özel sistemler, fonksiyonlar, methodlar, ve yol...
TRL : All Special Systems, funcs, method, the way to...

Geliþtirici : .. Fatihbab34™ ..
Paketler ; LuaToPython, PythonToLua, PythonIslem
Fonksiyonlar ; "split('#blabla#blabla#', '#'), python_system2.getinput('PythonIslem'), io funcs(open, remove, write, read, readline, readlines), table forms, pc.getqf(), pc.setqf()"

--]]

quest python_system2 begin
	state start begin
	
		function nesnemarket_satinal(sira,yer,kod,menu)
			local yerimiz = ""
			local bedava = 0
			if yer == "bedavaedit" then
				yerimiz = NESNEMARKET_BEDAVAITEMLER["Menu"..menu]
			elseif yer == "normaledit" then
				bedava = 1
				yerimiz = NESNEMARKET_NORMALITEMLER["Menu"..menu]
			end
			
			for val,keys in yerimiz do
				local bol = python_system2.split(keys, "#")
				local item = python_system2.split(keys, "#")
				--local itemTab = item[3]..'#'..item[4]..'#'..item[5]..'#'..item[6]..'#'..item[7]..'#'..item[8]..'#'..item[9]..'#'..item[10]..'#'..item[11]..'#'..item[12]..'#'..item[13]..'#'..item[14]..'#'..item[15]..'#'..item[16]..'#'..item[17]..'#'..item[18]..'#'..item[19]..'#'..item[20]..'#'..item[21]..'#'..item[22]..'#'..item[23]..'#'..item[24]..'#'..item[25]..'#'..item[26]..'#'
				local itemTab = keys
				if bol[2] == sira and bol[3] == kod then
					if not pc.enough_inventory(tonumber(bol[3])) then
						syschat("<Nesne Market>: Ýtemi satin almak envanterde yeterli boþluk yok.")
						return
					end
					local ep = game.mysql_query("SELECT cash FROM account.account WHERE id = '"..pc.get_account_id().."' LIMIT 1")[1][1]
					if tonumber(ep) >= tonumber(bol[26]) then
						local fiyat = tonumber(bol[26])
						python_system2.nesnemarket_itemiver(itemTab, bedava)
						
						--mysql.execute("UPDATE account.account SET cash = cash - "..fiyat.." WHERE id = '"..pc.get_account_id().."' LIMIT 1;")
						game.mysql_query("UPDATE account.account SET cash = cash - "..tonumber(fiyat).." WHERE id = "..tonumber(pc.get_account_id())..";")
						cmdchat("LuaToPython |itemshop_itemler_yang|"..tonumber(ep)-tonumber(fiyat))
						
						
						--pc.give_item2(tonumber(bol[3]), tonumber(bol[4]))
					else
						--syschat('<ItemShop> : Yeterli ep yok.')
						cmdchat("LuaToPython |itemshop_itemler|!#yeterliepyok#!")
					end
				end
			end
		end
		
		function nesnemarket_itemiver(itemTab, bedava)
			
			local bol = python_system2.split(itemTab, "#")
			pc.give_item2_select(tonumber(python_system2.split(itemTab, "#")[3]),tonumber(python_system2.split(itemTab, "#")[4]))
			local attr,socket = {},{}
			for i = 12,25 do table.insert(attr,{python_system2.split(itemTab, "#")[i],python_system2.split(itemTab,"#")[i+1]}) i = i+1 end
			for i = 6,8 do table.insert(socket,python_system2.split(itemTab, "#")[i]) end
			for i = 1, table.getn(attr) do
				item.set_value(i-1, tonumber(attr[i][1]), tonumber(attr[i][2]))  
			end 
			
			for i = 1, table.getn(socket) do if tonumber(socket[i]) > 0 then item.set_socket(i-1, socket[i]) end end
			if bedava == 0 then
				return
			end
			local login = game.mysql_query("SELECT login FROM account.account WHERE id = '"..pc.get_account_id().."' LIMIT 1")[1][1]
			local sifir = 0
			--game.mysql_query('INSERT INTO nesnemarket (owner_id,item_vnum,price) VALUES (\\"'..tostring(pc.get_player_id())..'\\", \\"'..tostring(number(1,7))..'\\", \\"'..tostring(sifir)..'\\" )')
			game.mysql_query('INSERT INTO nesnemarket (id,account_id,login,vnum,kristal,adet,item_sure,item_id,tarih) VALUES (\\"'..pc.get_player_id()..'\\", \\"'..pc.get_account_id()..'\\", \\"'..login..'\\", \\"'..item.get_vnum()..'\\", \\"'..bol[26]..'\\", \\"'..bol[4]..'\\", \\"'..sifir..'\\", \\"'..tostring(item.get_id())..'\\", \\"'..os.date("%d/%m/%Y, %H:%m")..'\\" )') 
			
			local nesnemarket_itemlist = {}
			local sira = 1
			local itemTabBol = python_system2.split(itemTab, "#")
			local itemTabLine = itemTabBol[3]..'#'..itemTabBol[4]..'#'..itemTabBol[5]..'#'..itemTabBol[6]..'#'..itemTabBol[7]..'#'..itemTabBol[8]..'#'..itemTabBol[9]..'#'..itemTabBol[10]..'#'..itemTabBol[11]..'#'..itemTabBol[12]..'#'..itemTabBol[13]..'#'..itemTabBol[14]..'#'..itemTabBol[15]..'#'..itemTabBol[16]..'#'..itemTabBol[17]..'#'..itemTabBol[18]..'#'..itemTabBol[19]..'#'..itemTabBol[20]..'#'..itemTabBol[21]..'#'..itemTabBol[22]..'#'..itemTabBol[23]..'#'..itemTabBol[24]..'#'..itemTabBol[25]..'#'..itemTabBol[26]..'#'
					
			local nesnemarket_ac = io.open('/usr/game/share/locale/turkey/quest/systems/nesnemarket_kayitlari/'..pc.get_name()..'_satinaldiklarim.cfg', "r")
			if nesnemarket_ac then
				for nesnemarketline in nesnemarket_ac:lines() do
					local item = python_system2.split(nesnemarketline, "#")
					local nesnemarketline2 = item[3]..'#'..item[4]..'#'..item[5]..'#'..item[6]..'#'..item[7]..'#'..item[8]..'#'..item[9]..'#'..item[10]..'#'..item[11]..'#'..item[12]..'#'..item[13]..'#'..item[14]..'#'..item[15]..'#'..item[16]..'#'..item[17]..'#'..item[18]..'#'..item[19]..'#'..item[20]..'#'..item[21]..'#'..item[22]..'#'..item[23]..'#'..item[24]..'#'..item[25]..'#'..item[26]..'#'..item[27]..'#'
					table.insert(nesnemarket_itemlist, nesnemarketline2)
				end
				
				local nesnemarket_itemyaz = io.open('/usr/game/share/locale/turkey/quest/systems/nesnemarket_kayitlari/'..pc.get_name()..'_satinaldiklarim.cfg', "w+")
				for i=1, table.getn(nesnemarket_itemlist) do
					nesnemarket_itemyaz:write("#"..i.."#"..nesnemarket_itemlist[i].."\\n")
					sira = sira+1
				end
				nesnemarket_itemyaz:close()
				
				local nesnemarket_itemyaz = io.open('/usr/game/share/locale/turkey/quest/systems/nesnemarket_kayitlari/'..pc.get_name()..'_satinaldiklarim.cfg', "a+")
				nesnemarket_itemyaz:write("#"..sira.."#"..itemTabLine..string.gsub(os.date("%d/%m/%Y, %H:%m"), ' ', '').."#\\n")
				nesnemarket_itemyaz:close()
			else
				local nesnemarket_itemyaz = io.open('/usr/game/share/locale/turkey/quest/systems/nesnemarket_kayitlari/'..pc.get_name()..'_satinaldiklarim.cfg', "a+")
				nesnemarket_itemyaz:write("#"..sira.."#"..itemTabLine..string.gsub(os.date("%d/%m/%Y, %H:%m"), ' ', '').."#\\n")
				nesnemarket_itemyaz:close()
			end
			
			local satinaldiklarim = {}
			local satinaldiklarim_ac = io.open('/usr/game/share/locale/turkey/quest/systems/nesnemarket_kayitlari/'..pc.get_name()..'_satinaldiklarim.cfg', "r")
			if satinaldiklarim_ac then
				for satinaldiklarimLine in satinaldiklarim_ac:lines() do
					table.insert(satinaldiklarim, satinaldiklarimLine)
				end
			end
			for i=1, table.getn(satinaldiklarim) do cmdchat("LuaToPython |itemshop_itemler!satinaldiklarim!|"..satinaldiklarim[i]) end
			
			--game.mysql_query('INSERT INTO nesnemarket (id,account_id,login,vnum,kristal,adet,item_sure,item_id,tarih) VALUES (\\"'..pc.get_player_id()..'\\", \\"'..pc.get_account_id()..'\\", \\"'..login..'\\", \\"'..item.get_vnum()..'\\", \\"'..bol[26]..'\\", \\"'..bol[4]..'\\", \\"'..sifir..'\\", \\"'..item.get_id()..'\\" )')
		end

		when login begin
			cmdchat("PythonToLua "..q.getcurrentquestindex())
		end

		when button begin
			local gelen = python_system2.getinput("PYTHONISLEM")

			if string.find(gelen, "#itemshop_itemleri_al#") then
				local bol = python_system2.split(gelen, "#")
				local bedavaitemler_menu_sayisi = 0
				local bedavaitemler_menu1 = {}
				local bedavaitemler_menu2 = {}
				local bedavaitemler_menu3 = {}
				local bedavaitemler_menu4 = {}		
				local bedavaitemler_menu5 = {}
				local bedavaitemler_menu6 = {}
				local bedavaitemler_menu7 = {}
				local bedavaitemler_menu8 = {}
				local bedavaitemler_menu9 = {}
				local bedavaitemler_menu10 = {}
				local bedavaitemler_menu11 = {}
				local bedavaitemler_menu12 = {}
				
				local normalitemler_menu1 = {}
				local normalitemler_menu2 = {}
				local normalitemler_menu3 = {}
				local normalitemler_menu4 = {}		
				local normalitemler_menu5 = {}
				local normalitemler_menu6 = {}
				local normalitemler_menu7 = {}
				local normalitemler_menu8 = {}
				local normalitemler_menu9 = {}
				local normalitemler_menu10 = {}
				local normalitemler_menu11 = {}
				local normalitemler_menu12 = {}
				
				local satinaldiklarim = {}
				
				local item_armors = {}
				local item_ears = {}
				local item_ups = {}
				local item_shield_heads = {}
				local item_other = {}
				
				local bedavaitemler = {["Menu1"] = bedavaitemler_menu1,["Menu2"] = bedavaitemler_menu2,["Menu3"] = bedavaitemler_menu3,["Menu4"] = bedavaitemler_menu4,
					["Menu5"] = bedavaitemler_menu5, ["Menu6"] = bedavaitemler_menu6, ["Menu7"] = bedavaitemler_menu7, ["Menu8"] = bedavaitemler_menu8, ["Menu9"] = bedavaitemler_menu9,
					["Menu10"] = bedavaitemler_menu10, ["Menu11"] = bedavaitemler_menu11, ["Menu12"] = bedavaitemler_menu12,
				}
				local normalitemler = {["Menu1"] = normalitemler_menu1,["Menu2"] = normalitemler_menu2,["Menu3"] = normalitemler_menu3,["Menu4"] = normalitemler_menu4,
					["Menu5"] = normalitemler_menu5, ["Menu6"] = normalitemler_menu6, ["Menu7"] = normalitemler_menu7, ["Menu8"] = normalitemler_menu8, ["Menu9"] = normalitemler_menu9,
					["Menu10"] = normalitemler_menu10, ["Menu11"] = normalitemler_menu11, ["Menu12"] = normalitemler_menu12,
				}
					
				for valx, keysx in NESNEMARKET_BEDAVAITEMLER do
					for val, keys in NESNEMARKET_BEDAVAITEMLER[valx] do table.insert(bedavaitemler[valx], keys) end	
				end
				for valx, keysx in NESNEMARKET_NORMALITEMLER do
					for val, keys in NESNEMARKET_NORMALITEMLER[valx] do table.insert(normalitemler[valx], keys) end	
				end
				local satinaldiklarim_ac = io.open('/usr/game/share/locale/turkey/quest/systems/nesnemarket_kayitlari/'..pc.get_name()..'_satinaldiklarim.cfg', "r")
				if satinaldiklarim_ac then
					for satinaldiklarimLine in satinaldiklarim_ac:lines() do
						table.insert(satinaldiklarim, satinaldiklarimLine)
					end
				end
				

				if bol[3] == "0" then
					local ep = game.mysql_query("SELECT cash FROM account.account WHERE id = '"..pc.get_account_id().."' LIMIT 1")[1][1]
					cmdchat("LuaToPython |itemshop_itemler_yang|"..ep)
					for i=1, table.getn(bedavaitemler_menu1) do cmdchat("LuaToPython |itemshop_itemler!bedavamenu1!|"..bedavaitemler_menu1[i]) end
					for i=1, table.getn(bedavaitemler_menu2) do cmdchat("LuaToPython |itemshop_itemler!bedavamenu2!|"..bedavaitemler_menu2[i]) end
					for i=1, table.getn(bedavaitemler_menu3) do cmdchat("LuaToPython |itemshop_itemler!bedavamenu3!|"..bedavaitemler_menu3[i]) end
					for i=1, table.getn(bedavaitemler_menu4) do cmdchat("LuaToPython |itemshop_itemler!bedavamenu4!|"..bedavaitemler_menu4[i]) end
					for i=1, table.getn(bedavaitemler_menu5) do cmdchat("LuaToPython |itemshop_itemler!bedavamenu5!|"..bedavaitemler_menu5[i]) end
					for i=1, table.getn(bedavaitemler_menu6) do cmdchat("LuaToPython |itemshop_itemler!bedavamenu6!|"..bedavaitemler_menu6[i]) end
					for i=1, table.getn(bedavaitemler_menu7) do cmdchat("LuaToPython |itemshop_itemler!bedavamenu7!|"..bedavaitemler_menu7[i]) end
					for i=1, table.getn(bedavaitemler_menu8) do cmdchat("LuaToPython |itemshop_itemler!bedavamenu8!|"..bedavaitemler_menu8[i]) end
					for i=1, table.getn(bedavaitemler_menu9) do cmdchat("LuaToPython |itemshop_itemler!bedavamenu9!|"..bedavaitemler_menu9[i]) end
					for i=1, table.getn(bedavaitemler_menu10) do cmdchat("LuaToPython |itemshop_itemler!bedavamenu10!|"..bedavaitemler_menu10[i]) end
					for i=1, table.getn(bedavaitemler_menu11) do cmdchat("LuaToPython |itemshop_itemler!bedavamenu11!|"..bedavaitemler_menu11[i]) end
					for i=1, table.getn(bedavaitemler_menu12) do cmdchat("LuaToPython |itemshop_itemler!bedavamenu12!|"..bedavaitemler_menu12[i]) end
					
					for i=1, table.getn(normalitemler_menu1) do cmdchat("LuaToPython |itemshop_itemler!normalmenu1!|"..normalitemler_menu1[i]) end
					for i=1, table.getn(normalitemler_menu2) do cmdchat("LuaToPython |itemshop_itemler!normalmenu2!|"..normalitemler_menu2[i]) end
					for i=1, table.getn(normalitemler_menu3) do cmdchat("LuaToPython |itemshop_itemler!normalmenu3!|"..normalitemler_menu3[i]) end
					for i=1, table.getn(normalitemler_menu4) do cmdchat("LuaToPython |itemshop_itemler!normalmenu4!|"..normalitemler_menu4[i]) end
					for i=1, table.getn(normalitemler_menu5) do cmdchat("LuaToPython |itemshop_itemler!normalmenu5!|"..normalitemler_menu5[i]) end
					for i=1, table.getn(normalitemler_menu6) do cmdchat("LuaToPython |itemshop_itemler!normalmenu6!|"..normalitemler_menu6[i]) end
					for i=1, table.getn(normalitemler_menu7) do cmdchat("LuaToPython |itemshop_itemler!normalmenu7!|"..normalitemler_menu7[i]) end
					for i=1, table.getn(normalitemler_menu8) do cmdchat("LuaToPython |itemshop_itemler!normalmenu8!|"..normalitemler_menu8[i]) end
					for i=1, table.getn(normalitemler_menu9) do cmdchat("LuaToPython |itemshop_itemler!normalmenu9!|"..normalitemler_menu9[i]) end
					for i=1, table.getn(normalitemler_menu10) do cmdchat("LuaToPython |itemshop_itemler!normalmenu10!|"..normalitemler_menu10[i]) end
					for i=1, table.getn(normalitemler_menu11) do cmdchat("LuaToPython |itemshop_itemler!normalmenu11!|"..normalitemler_menu11[i]) end
					for i=1, table.getn(normalitemler_menu12) do cmdchat("LuaToPython |itemshop_itemler!normalmenu12!|"..normalitemler_menu12[i]) end
					
					for i=1, table.getn(satinaldiklarim) do cmdchat("LuaToPython |itemshop_itemler!satinaldiklarim!|"..satinaldiklarim[i]) end
					--for i=1, table.getn(bedavaitemler_menu1) do cmdchat("LuaToPython |itemshop_itemler_bedavamenu1_|"..bedavaitemler_menu1[i]) end
				
				else
					local sira = bol[4]
					local yer = bol[5]
					local kod = bol[6]
					local menu = bol[7]
					
					python_system2.nesnemarket_satinal(sira,yer,kod,menu)
					
					--elseif xxx then
						---
					--end
				end
				
			end

		end

		function getinput(gelen)
			local input1 = "#quest_input#"
			local input0 = "#quest_inputbitir#"
			cmdchat("LuaToPython "..input1)
			local al = input(cmdchat("PythonIslem "..gelen))
			cmdchat("LuaToPython "..input0)
			return al
		end

		function split(command_, ne)
			return python_system2.split_(command_,ne)
		end
		
		function split_(string_,delimiter)
			local result = { }
			local from  = 1
			local delim_from, delim_to = string.find( string_, delimiter, from  )
			while delim_from do
				table.insert( result, string.sub( string_, from , delim_from-1 ) )
				from  = delim_to + 1
				delim_from, delim_to = string.find( string_, delimiter, from  )
			end
			table.insert( result, string.sub( string_, from  ) )
			return result
		end
	end
end