import fortnitepy

async def event_friend_add(client: fortnitepy.Client, friend: fortnitepy.Friend):
    try:
        await friend.send('Thanks for using this Bot\nIf you wan\'t to get your own bot *Join my Discord*: https://discord.gg/GPSPwh6\n and check out my Youtube: LupusLeaks,\nTwitter: LupusLeaks,\nInsta: LupusLeaks')
    except: pass

    #if client.settings["friend"]["invite_on_add"]:
    if True:
        try:
            await friend.invite()
        except: pass

async def event_friend_remove(client: fortnitepy.Client, friend: fortnitepy.Friend):
    # if client.settings["friend"]["add_on_remove"]:
    if True:
        try:
            await client.add_friend(friend.id)
        except:
            pass

async def event_friend_request(client: fortnitepy.Client, request: fortnitepy.PendingFriend):
    # if client.settings["friend"]["accept_request"]:
    if True:
        try:
            await request.accept()
        except:
            pass