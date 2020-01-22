import discord
import os
import random
import asyncio
from urllib.request import urlopen, Request
from datetime import datetime as dt
import urllib
import urllib.request
import bs4




from discord.ext import commands

now = dt.now()

class MyClient(discord.Client):
    async def on_ready(self):
        print(client.user.id)
        print(client.user.name)
        print("on ready")
        game = discord.Game(",도움말로 확인")
        await client.change_presence(status=discord.Status.online, activity=game)

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = '{1.name}에 {0.mention}님이 새로 오셨어요!'.format(member, guild)
            await guild.system_channel.send(to_send)

    async def on_member_remove(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = '{1.name}에 {0.mention}님께서 나가버리셨어요 ㅜㅜ'.format(member, guild)
            await guild.system_channel.send(to_send)

    async def on_message(self, message):
    # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith(',숫자맞추기'):
            embed = discord.Embed(ttitle="식량이가 좋아하는 랜덤 게임!", description="숫자맞추기!!", color=0xff80c0)
            embed.add_field(name="^-^ ^-^ ^-^", value="10초안에 1~10의 숫자를 찍어서 맞혀주세요!", inline=False)
            embed.add_field(name="ex) 1", value="만약 1 이외에 글자를 덧붙여서 사용하실 경우 답으로 인정되지 않습니다.", inline=False)
            embed.add_field(name="ex) 1이여, 1ㄱㄱ", value="그럼 게임 스타트! 게임 스타트!", inline=False)
            embed.set_image(url="https://postfiles.pstatic.net/MjAyMDAxMjJfMjEx/MDAxNTc5Njk3NDU2MDUy.gksqsCsB0W__r4gnqtEZ2eas0Ou5BymlPOR75IkAjcAg.o8XVvgE02na8T7MIcATWz5zykJO-qGi8vpPpAoXFPWAg.PNG.1ngyoe/20200122_213553_01.png?type=w773")
            await message.channel.send(embed=embed)

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=10.0)
            except asyncio.TimeoutError:
                return await message.channel.send('ㅋ 시간 초과 답은 {}.'.format(answer))

            if int(guess.content) == answer:
                await message.channel.send('정답입니다!')
            else:
                await message.channel.send('땡!! 답은 {}.'.format(answer))




        elif message.content.startswith(",도움말"):
            await message.channel.send("```해당 봇은 사운드클라우드 노래 서칭 및 재생을 위한 봇 입니다.```"
                                       "　"
                                       "노래 재생 관련"
                                       "　"
                                       "```,재생 (노래제목) - 해당 제목의 첫 번째 곡을 재생합니다.```"
                                       "```,스킵 - 노래를 스킵합니다.```"
                                       "```,입장 - 해당 채널에 봇을 입장시킵니다.```"
                                       "```,퇴장 - 해당 채널에서 봇을 퇴장시킵니다.```"
                                       "```,정지 - 노래를 일시 정지 시킵니다.```"
                                       "```,재생 - 노래를 다시 재생 시킵니다.```"
                                       "```,재생목록 - 재생 목록을 확인 합니다.```"
                                       "　"
                                       "기타"
                                       "　"
                                       "```.숫자맞추기 - 숫자 맞추기 게임을 시작합니다.```"
                                       "```,룰렛 - 1 부터 100 까지 나오는 룰렛을 돌립니다.```"
                                       "```,날씨 (지역명) - 현재 해당 지역의 날씨를 알려줍니다.```"
                                       "```,투표 (투표주제)/(대상1)/(대상2) ... - 해당 주제로 투표를 진행합니다. 이모지를 통해 찬성을 하실 수 있습니다.```"
                                       "```,청소 - 모두가 평등하게! 99개의 메세지를 삭제할 수 있습니다."
                                       "-------------------------------------------------"
                                       "```버그 문의는 식량 메이플2 귓보내셈 수고뽕따리```")


        elif message.content.startswith(",날씨"):
            learn = message.content.split(" ")
            location = learn[1]
            enc_location = urllib.parse.quote(location+'날씨')
            hdr = {'User-Agent': 'Mozilla/5.0'}
            url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location
            print(url)
            req = Request(url, headers=hdr)
            html = urllib.request.urlopen(req)
            bsObj = bs4.BeautifulSoup(html, "html.parser")
            todayBase = bsObj.find('div', {'class': 'main_info'})

            todayTemp1 = todayBase.find('span', {'class': 'todaytemp'})
            todayTemp = todayTemp1.text.strip()  # 온도
            print(todayTemp)

            todayValueBase = todayBase.find('ul', {'class': 'info_list'})
            todayValue2 = todayValueBase.find('p', {'class': 'cast_txt'})
            todayValue = todayValue2.text.strip()  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
            print(todayValue)

            todayFeelingTemp1 = todayValueBase.find('span', {'class': 'sensible'})
            todayFeelingTemp = todayFeelingTemp1.text.strip()  # 체감온도
            print(todayFeelingTemp)

            todayMiseaMongi1 = bsObj.find('div', {'class': 'sub_info'})
            todayMiseaMongi2 = todayMiseaMongi1.find('div', {'class': 'detail_box'})
            todayMiseaMongi3 = todayMiseaMongi2.find('dd')
            todayMiseaMongi = todayMiseaMongi3.text  # 미세먼지
            print(todayMiseaMongi)

            tomorrowBase = bsObj.find('div', {'class': 'table_info weekly _weeklyWeather'})
            tomorrowTemp1 = tomorrowBase.find('li', {'class': 'date_info'})
            tomorrowTemp2 = tomorrowTemp1.find('dl')
            tomorrowTemp3 = tomorrowTemp2.find('dd')
            tomorrowTemp = tomorrowTemp3.text.strip()  # 오늘 오전,오후온도
            print(tomorrowTemp)

            tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
            tomorrowMoring1 = tomorrowAreaBase.find('div', {'class': 'main_info morning_box'})
            tomorrowMoring2 = tomorrowMoring1.find('span', {'class': 'todaytemp'})
            tomorrowMoring = tomorrowMoring2.text.strip()  # 내일 오전 온도
            print(tomorrowMoring)

            tomorrowValue1 = tomorrowMoring1.find('div', {'class': 'info_data'})
            tomorrowValue = tomorrowValue1.text.strip()  # 내일 오전 날씨상태, 미세먼지 상태
            print(tomorrowValue)

            tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
            tomorrowAllFind = tomorrowAreaBase.find_all('div', {'class': 'main_info morning_box'})
            tomorrowAfter1 = tomorrowAllFind[1]
            tomorrowAfter2 = tomorrowAfter1.find('p', {'class': 'info_temperature'})
            tomorrowAfter3 = tomorrowAfter2.find('span', {'class': 'todaytemp'})
            tomorrowAfterTemp = tomorrowAfter3.text.strip()  # 내일 오후 온도
            print(tomorrowAfterTemp)

            tomorrowAfterValue1 = tomorrowAfter1.find('div', {'class': 'info_data'})
            tomorrowAfterValue = tomorrowAfterValue1.text.strip()

            print(tomorrowAfterValue)  # 내일 오후 날씨상태,미세먼지

            embed = discord.Embed(title=now.strftime('%Y-%m-%d' + ' ' + ' ' + '%p %I:%M:%S') + " " + learn[1] ,description=learn[1] + "," + " " + '오늘의 날씨를 한 번 알아보아요!',colour=discord.Colour.gold())
            embed.add_field(name='현재 온도는?', value=todayTemp+'˚', inline=False)  # 현재온도
            embed.add_field(name='체감 온도는?', value=todayFeelingTemp, inline=False)  # 체감온도
            embed.add_field(name='현재 상태는?', value=todayValue, inline=False)  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
            embed.add_field(name='현재 미세먼지 상태는?', value=todayMiseaMongi, inline=False)  # 오늘 미세먼지
            embed.add_field(name='오늘 오전과 오후의 날씨는?', value=tomorrowTemp, inline=False)  #오늘날씨 # color=discord.Color.blue()

            await message.channel.send(embed=embed)


        elif message.content.startswith(",룰렛"):
            await message.channel.send("1~100 까지의 숫자가 랜덤으로 나옵니다.")
            dice = random.randint(1, 100)

            def ppp(m):
                return m.author == message.author and m.channel == message.channel
            try:
                msg = await client.wait_for('message', check=ppp, timeout=0.5)
            except asyncio.TimeoutError:
                await message.channel.send("룰렛 결과, 나온 숫자는" " " + "`" + format(dice) + "`" + " " "입니다.")
            
        elif message.content.startswith(",투표"):
            vote = message.content[4:].split("/")
            user = message.author
            await message.channel.send(":japanese_goblin: 속보!! 현재 진행중인 투표가 있습니다 :japanese_goblin:")
            def pp(m):
                return m.author == message.author and m.channel == message.channel
            try:
                msg = await client.wait_for('message', check=pp, timeout=0.5)
            except asyncio.TimeoutError:
                await message.channel.send(f"현재 이 투표의 주최자는 {user.mention} 입니다.")
                await message.channel.send("-----------------------------------------------------------")
                await message.channel.send("```투표 주제 -" + " " + " " + vote[0] + "```")
                await message.channel.send("-----------------------------------------------------------")
                for i in range(1, len(vote)):
                    choose1 = await message.channel.send("```" + vote[i] + "```")
                    await choose1.add_reaction('✋')


client = MyClient()
client.run('NjY5NDcxNjI4OTY2NjI1Mjgx.XijQHQ.fgeS-a6IPdJDs71m7bEfHiEtJWg')
