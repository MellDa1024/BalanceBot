import asyncio
import discord
import time
import requests
import ast
from bs4 import BeautifulSoup
from itertools import combinations
from copy import deepcopy
from copy import copy
nowtime=0
helpembed = discord.Embed(colour=discord.Colour(0xffffff))
helpembed.add_field(name="☑️명령어☑️", value="""!명령어 - 현제 장면을 보여줍니다.
!참가인원 - 참가한 인원을 보여줍니다.
!참가/제외 (닉네임) - 자신을 참가/제외합니다, 뒤에 닉네임을 입력 시 그 소환사를 참가/제외시킵니다. (사용 전 !닉네임으로 닉네임을 정해야합니다)
!참가 초기화 - 모든 참가 현황을 초기화합니다.
!닉네임 (닉네임) - fow.kr에서 닉네임을 검색해, 존재할 시 채팅 친 유저의 소환사명을 닉네임으로 설정합니다(티어는 자유랭과 솔랭중에서 높은걸로 자동설정)
!티어 설정 (티어) - 자신의 티어를 임의로 변경합니다 (티어 예시 : G2, I3)
!내닉네임 - 자신의 닉네임과 티어를 보여줍니다.
!밸런스 (숫자) - 참가 인원이 10명일때 티어에 점수를 매겨 각 팀의 점수의 평균이 가장 비슷한 배치를 (숫자)만큼 표시합니다.""")
tierlist={"IRON I" : "I1", "IRON II" : "I2", "IRON III" : "I3", "IRON IV" : "I4",
"BRONZE I" : "B1", "BRONZE II" : "B2", "BRONZE III" : "B3", "BRONZE IV" : "B4",
"SILVER I" : "S1", "SILVER II" : "S2", "SILVER III" : "S3", "SILVER IV" : "S4",
"GOLD I" : "G1", "GOLD II" : "G2", "GOLD III" : "G3", "GOLD IV" : "G4",
"PLATINUM I" : "P1", "PLATINUM II" : "P2", "PLATINUM III" : "P3", "PLATINUM IV" : "P4",
"DIAMOND I" : "D1", "DIAMOND II" : "D2", "DIAMOND III" : "D3", "DIAMOND IV" : "D4",
"MASTER I" : "M1", "GRANDMASTER I" : "GM1", "CHALLENGER I" : "C1", "배치" : "UNRANKED"}
tierpoint={"I1" : -1, "I2" : -2, "I3" : -3, "I4" : -4,
"B1" : 4, "B2" : 3, "B3" : 2, "B4" : 1,
"S1" : 8, "S2" : 7, "S3" : 6, "S4" : 5,
"G1" : 12, "G2" : 11, "G3" : 10, "G4" : 9,
"P1" : 16, "P2" : 15, "P3" : 14, "P4" : 13,
"D1" : 20, "D2" : 19, "D3" : 18, "D4" : 17,
"M1" : 22, "GM1" : 25, "C1" : 27, "UNRANKED" : 0}
tierlistname=["I1","I2","I3","I4","B1","B2","B3","B4","S1","S2","S3","S4","G1","G2","G3","G4","P1","P2","P3","P4","D1","D2","D3","D4","M1","GM1","C1","UNRANKED"]
devlist=[665987712922288139]
summonerlist=[]
def aavg(a,b,c,d,e):
	return a+b+c+d+e/5
app = discord.Client()
token = ""#Token
@app.event
async def on_ready():
	print("BalanceBot")
	game = discord.Game("Type !명령어 in chat to see the command.")
	await app.change_presence(status=discord.Status.online, activity=game)
@app.event
async def on_message(message):
	global summonerlist
	global nowtime
	global devlist
	id = message.author.id 
	channel = message.channel
	playersaid = (str(message.author)+' said "'+str(message.content)+'" in '+str(channel))
	print(playersaid)
	if message.content.strip() == "!명령어":
		await message.channel.send(embed=helpembed)
	elif message.content.strip() == "!참가인원":
		sending=""
		for i in summonerlist:
			sending=sending+"{0} : {1}  ///  티어 : {2}\n".format(i[0], i[1], i[2])
		if sending=="":
			embed = discord.Embed(colour=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
			embed.add_field(name="🎫참가 인원🎫", value="참가한 유저가 없습니다.")
			await message.channel.send(embed=embed)
		else:
			embed = discord.Embed(colour=discord.Colour(0xffffff))
			embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
			embed.add_field(name="🎫참가 인원🎫", value=sending)
			await message.channel.send(embed=embed)
	elif message.content.startswith("!참가 "):
		file = open("id.txt", 'r')
		contents=file.read()
		print(contents)
		data = ast.literal_eval(contents)
		file.close()
		file = open("tier.txt", 'r')
		contents=file.read()
		Tierdata = ast.literal_eval(contents)
		file.close()
		if message.content.strip() == "!참가":
			if id in data:
				cnt=0
				flag=0
				for i in summonerlist:
					if i[3] == id:
						summonerlist[cnt][1] = data[id]
						summonerlist[cnt][2] = Tierdata[data[id]]
						flag=1
						await message.channel.send("<@"+str(id)+">님, '"+str(data[id])+"'(으)로 참가되었습니다.")
					cnt=cnt+1
				if flag==0:
					if len(summonerlist) == 10:
						await message.channel.send("<@"+str(id)+">님, 이미 10명이 참가했습니다.")
					else:
						summonerlist.append([str(message.author.name),data[id],Tierdata[data[id]],id])
						await message.channel.send("<@"+str(id)+">님, '"+str(data[id])+"'(으)로 참가되었습니다.")
			else:
				await message.channel.send("<@"+str(id)+">님, 닉네임이 설정되어 있지 않습니다. !닉네임으로 설정해주세요.")
		else:
			_cnt=0
			_flag=0
			for i in list(data.items()):
				if i[1].lower() == message.content[4:].lower():
					_flag=1
				if _flag==0:
					_cnt=_cnt+1
			if _flag==1:
				_id=list(data.items())[_cnt][0]
				cnt=0
				flag=0
				for i in summonerlist:
					if i[3] == _id:
						summonerlist[cnt][1] = data[_id]
						summonerlist[cnt][2] = Tierdata[data[_id]]
						flag=1
						await message.channel.send("<@"+str(id)+">님, '"+str(data[_id])+"'(으)로 참가되었습니다.")
					cnt=cnt+1
				if flag==0:
					if len(summonerlist) == 10:
						await message.channel.send("<@"+str(id)+">님, 이미 10명이 참가했습니다.")
					else:
						summonerlist.append([str(message.guild.get_member(_id).name),data[_id],Tierdata[data[_id]],_id])
						await message.channel.send("<@"+str(id)+">님, '"+str(data[_id])+"'(으)로 참가되었습니다.")
			else:
				await message.channel.send("<@"+str(id)+">님,"+message.content[4:]+"님은 닉네임이 설정되어 있지 않습니다. !닉네임으로 설정해주세요.")
	elif message.content.startswith("!제외 "):
		if message.content.strip()=="!제외":
			cnt=0
			flag=0
			for i in summonerlist:
				if i[3] == id:
					flag=1
				if flag==0:
					cnt=cnt+1
			if flag==1:
				await message.channel.send("<@"+str(id)+">님을 제외했습니다.")
				del summonerlist[cnt]
			else:
				await message.channel.send("<@"+str(id)+">님은 참가하시지 않았습니다.")
		else:
			cnt=0
			flag=0
			for i in summonerlist:
				if i[1] == message.content[4:]:
					flag=1
				if flag==0:
					cnt=cnt+1
			if flag==1:
				await message.channel.send("<@"+str(id)+">님, '"+str(message.content[4:])+"'님을 제외했습니다.")
				del summonerlist[cnt]
			else:
				await message.channel.send("<@"+str(id)+">님, '"+str(message.content[4:])+"'님은 참가하시지 않았습니다.")
	elif message.content.startswith("!닉네임"):
		if message.content.strip()!="!닉네임":
			if nowtime+10>time.time():
				await message.channel.send("<@"+str(id)+">님, 잠시 후 다시 시도해주시기 바랍니다. (fow.kr를 크롤링하는거라 단시간에 많이 사용하면 안되요)")
				nowtime=time.time()
			elif message.content.find('_') != -1 or message.content.find('(') != -1 or message.content.find(')') != -1 or message.content.find('"') != -1 or message.content.find("'") != -1:
				await message.channel.send("<@"+str(id)+">님, 특수문자를 지워주시기 바랍니다.")
			else:
				req = requests.get('http://fow.kr/find/'+message.content.strip()[5:])
				html = req.text
				soup = BeautifulSoup(html, 'html.parser')
				Tier1 = soup.select(
				'body > div:nth-child(4) > div:nth-child(2) > div:nth-child(2) > div.table_summary > div:nth-child(4) > div:nth-child(2) > b > font' #자유랭
				)
				Tier2 = soup.select(
				'body > div:nth-child(4) > div:nth-child(2) > div:nth-child(2) > div.table_summary > div:nth-child(2) > div:nth-child(2) > b > font' #솔랭
				)
				Name = soup.select(
				'body > div:nth-child(4) > div:nth-child(2) > div:nth-child(2) > div.profile > div:nth-child(2) > span'
				)
				if Name:
					if Name[0].text.lower() == message.content.strip()[5:].lower():
						file = open("id.txt", 'r')
						contents=file.read()
						data = ast.literal_eval(contents)
						print(data)
						data[id] = Name[0].text
						file.close()
						file = open("id.txt", "w")
						file.write(str(data))
						file.close()

						file = open("tier.txt", 'r')
						contents=file.read()
						Tierdata = ast.literal_eval(contents)
						print(Tierdata)
						if Tier1 and not Tier2:
							Tierdata[Name[0].text] = tierlist[Tier1[0].text]
						if not Tier1 and Tier2:
							Tierdata[Name[0].text] = tierlist[Tier2[0].text]
						if Tier1 and Tier2:
							if tierpoint[tierlist[Tier1[0].text]] >= tierpoint[tierlist[Tier2[0].text]]:
								Tierdata[Name[0].text] = tierlist[Tier1[0].text]
							else:
								Tierdata[Name[0].text] = tierlist[Tier2[0].text]
						else:
							Tierdata[Name[0].text] = "UNRANKED"
						file.close()
						file = open("tier.txt", "w")
						file.write(str(Tierdata))
						file.close()
						await message.channel.send("<@"+str(id)+">님, "+Name[0].text+"라는 닉네임으로 추가되었습니다.")
					else:
						await message.channel.send("<@"+str(id)+">님, "+message.content.strip()[5:]+"라는 닉네임을 찾을 수 없습니다.")
				else:
					await message.channel.send("<@"+str(id)+">님, "+message.content.strip()[5:]+"라는 닉네임을 찾을 수 없습니다.")
				nowtime=time.time()
		else:
			await message.channel.send("<@"+str(id)+">님, !닉네임 옆에 소환사명을 입력해주세요.")
	elif message.content.strip() == "!참가 초기화":
		summonerlist=[]
		await message.channel.send("<@"+str(id)+">, 초기화되었습니다.")
	elif message.content.strip() == "!내닉네임":
		file = open("id.txt", 'r')
		contents=file.read()
		data = ast.literal_eval(contents)
		print(data)
		file.close()
		if id in data:
			file = open("tier.txt", 'r')
			contents=file.read()
			Tierdata = ast.literal_eval(contents)
			file.close()
			await message.channel.send("<@"+str(id)+">님의 닉네임은 '"+data[id]+"', 티어는 '"+Tierdata[data[id]]+"'입니다.")
	elif message.content.startswith("!티어 설정"):
		if message.content[7:] in tierlistname:
			file = open("id.txt", 'r')
			contents=file.read()
			data = ast.literal_eval(contents)
			file.close()
			if id in data:
				file = open("tier.txt", 'r')
				contents=file.read()
				Tierdata = ast.literal_eval(contents)
				print(Tierdata)
				Tierdata[data[id]] = message.content[7:]
				file.close()
				file = open("tier.txt", "w")
				file.write(str(Tierdata))
				file.close()
				await message.channel.send("<@"+str(id)+">님, '"+data[id]+"'의 티어를 '"+Tierdata[data[id]]+"'(으)로 설정했습니다.")
		else: 
			await message.channel.send("<@"+str(id)+">님, 티어를 형식에 맞게 적어주세요(Ex : I2, G4 ,GM1")
	elif message.content.startswith("!밸런스"):
		flag=0
		if len(summonerlist)==10:
			try:
				saylimit = int(message.content[5:])
			except:
				await message.channel.send("<@"+str(id)+">님, 표시할 팀의 개수를 입력해주세요.")
				flag=1
			if saylimit>5:
				await message.channel.send("<@"+str(id)+">님, 도배 방지를 위해 최대 5개까지 확인이 가능합니다.")
				flag=1
			if flag == 0:
				a = combinations([0,1,2,3,4,5,6,7,8,9], 5)
				finalteam=[]
				for i in a:
					redteam=[]
					blueteam=[]
					for j in range(0,10):
						if j in i:
							redteam.append(summonerlist[j])
						else:
							blueteam.append(summonerlist[j])
					avgdiff = aavg(tierpoint[redteam[0][2]],tierpoint[redteam[1][2]],tierpoint[redteam[2][2]],tierpoint[redteam[3][2]],tierpoint[redteam[4][2]]) - aavg(tierpoint[blueteam[0][2]],tierpoint[blueteam[1][2]],tierpoint[blueteam[2][2]],tierpoint[blueteam[3][2]],tierpoint[blueteam[4][2]])
					if avgdiff < 0 : avgdiff=avgdiff*-1
					if avgdiff < 2:
						finalteam.append([deepcopy(redteam),deepcopy(blueteam),copy(avgdiff)])
				if finalteam:
					finalteam.sort(key=lambda finalteam: finalteam[2])
					cnt=1
					for i in finalteam:
						if cnt<=int(saylimit):
							avgdiffer="티어 차이 : {0:0.2f}".format(i[2])
							embedsaying=""
							for j in range(0,5):
								embedsaying=embedsaying+"{0}({1}) : {2}\n".format(i[0][j][1],i[0][j][0],i[0][j][2])
							embed = discord.Embed(colour=discord.Colour(0x990507))
							embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
							embed.set_author(name="🟥레드 팀🟥", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
							embed.add_field(name=avgdiffer, value=embedsaying)
							await message.channel.send(embed=embed)
							embedsaying=""
							for j in range(0,5):
								embedsaying=embedsaying+"{0}({1}) : {2}\n".format(i[1][j][1],i[1][j][0],i[1][j][2])
							embed = discord.Embed(colour=discord.Colour(0x331673))
							embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
							embed.set_author(name="🟦블루 팀🟦", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
							embed.add_field(name=avgdiffer, value=embedsaying)
							await message.channel.send(embed=embed)
							if cnt!=int(saylimit):
								await message.channel.send("--------------------------------")
							cnt=cnt+1
					finalteam=[]
				else:
					await message.channel.send("<@"+str(id)+">님, 밸런스가 맞는 팀 편성을 찾을 수가 없습니다.")
		else:
			await message.channel.send("<@"+str(id)+">님, 인원수가 10명이 아닙니다.")
app.run(token)