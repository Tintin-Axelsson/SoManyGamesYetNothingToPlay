import requests
import json

print("Lol welcome to the amazing 'what games do we have in common' finder")

key = input("Input your SteamAPI-Key: ")
steam_id_your = input("Input your SteamID64: ")

url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={0}&steamid={1}&relationship=friend"\
    .format(key, steam_id_your)
r = requests.get(url)
steam_friends_data = r.json()["friendslist"]["friends"]

print("Retrieving your friendslist... (This may take some time)")
friends = []
for (i, steam_friend) in enumerate(steam_friends_data):
    steam_id = steam_friend["steamid"]
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={0}&steamids={1}"\
        .format(key, steam_id)

    r = requests.get(url)
    username = r.json()["response"]["players"][0]["personaname"]
    friends.append([steam_id, username])
    print("[{0}] Name: {1}".format(i, username))

selection = [int(item) for item in input("Index of friend selection (space separated) : ").split()]

steam_ids = [steam_id_your]
for index in selection:
    steam_ids.append(friends[index][0])

print("Checking for games you all own...\n")

users = []
for steam_id in steam_ids:
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={0}&steamid={1}&format=json" \
        .format(key, steam_id)
    r = requests.get(url)
    data = r.json()

    game_count = data["response"]["game_count"]
    games = data["response"]["games"]
    appid = []
    for game in games:
        appid.append(game["appid"])
    users.append([game_count, appid])

appid_shared = list(set(users[0][1]) & set(users[1][1]))
for i in range(2, len(steam_ids)):
    appid_shared = list(set(appid_shared) & set(users[i][1]))

games_shared = []
with open('appid_index.json', 'r') as f:
    data = json.load(f)
    data = data["applist"]["apps"]

    # Kinda garbage
    for game in data:
        for appid in appid_shared:
            if appid == game["appid"]:
                games_shared.append(game["name"])
                appid_shared.remove(appid)  # Saving time

for game in games_shared:
    print(game)

input("\nPress any key to exit")

