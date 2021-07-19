# BalanceBot
Make some 5v5 teams that are balanced in League of Legends.
Judging Balance with player's tier.

## Requirements
1. Python
2. Bs4
3. discord api
4. itertools?(Doesn't it already exists? I'm confusing)
5. discord bot token

## Warning
The worst part of this program is it just doesn't work.
To specifically it, It worked 1 year before but get_member(id) is making trouble because of update of discord.
Maybe [this](https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents) will solve it, but I don't have enough time to fix it :(
+ The command "!참가" doesn't work because of my bad "if" statement.
+ The program's purpose was to use in my private server, so it won't multi-task<br />

## How does it work(If the error has been fixed)
1. When player executes command "!닉네임 (Username)", The program will save summoner's username, tier, and discord's id in tier.txt and id.txt with crawling [fow.kr](fow.kr)(which is korean version of op.gg)
2. Using command "!참가", The program will add Player's information(which we saved in txt files) in list.
3. If there are 10 players and someone executes the "!밸런스 (int)", (int=<5), the program will make the team with using combination function and add the team which are balanced(When value of each team's tier are similar) in list named "finalteam".
4. The bot will print "finalteam" with an embed style.