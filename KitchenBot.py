import os
import time
import re
from slackclient import SlackClient
import random

BotAuth = input("Enter Bot Auth Code: ")

slack_client = SlackClient(BotAuth)
starterbot_id = None

RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

Sammich = ", make me a sandwich." , ", make me a sandwich"
ChocCookie = ", give me a cookie." , ", give me a cookie"
Wooder = ", I'm thirsty." , ", I'm thirsty"
Covfefe = ", I'm tired." , ", I'm tired"
CommandHelp = "Help"
Quote = ", tell me a quote." , ", tell me a quote"
HelloWorld = ", say something generic."
SongRequest = ", I want to listen to some music." , ", I want to listen to some music"
SelfDepricatingCommand = ", do my homework for me." , ", do my homework for me"
PingPong = ", think fast!" , ", think fast"

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    default_response = "Not sure what you mean. Try *{}*.".format(CommandHelp)

    response = None

    if command.startswith(Sammich):
        response = "Here's your sandwich! :Sandwich:"

    if command.startswith(ChocCookie):
        response = "Here's your cookie! :Cookie:"

    if command.startswith(Wooder):
        response = "Here, have a nice cold cup of water! :cup_with_straw:"

    if command.startswith(Covfefe):
        response = "Here, enjoy a nice cup of coffee! :coffee:"

    if command.startswith(CommandHelp):
        response = """MENU (All Commands require KitchenBot to be mentioned with no space between the comma and mention.)
        --------------------------------------------
        Ham Sandwich | , make me a sandwich.
        Chocolate Chip Cookie | , give me a cookie.
        Water | , I'm thirsty.
        Coffee | , I'm tired.
        Quotes | , tell me a quote.
        Music | , I want to listen to some music.
        YEET | , think fast!
        Programmed by Colin Gideon, 2018"""

    if command.startswith(Quote):
        quotelist = [
            '''<Mr. Brown> Mikey, where'd I leave the screwdriver?
<Michael Frilles> Over there, go foward...no, your other foward''',
            '''We transport the robot via several carrier pigeons.
~Michael Frilles''',
            '''I surprisingly still don't have a quote yet.
~Chad Nivens''',
            '''<to Lauren> Duuuude Dean Kamen created FIRST, but then Woodie Flowers came along, took FIRST, and made it gooder
~Naomi Gorley''',
            '''*waving finger*
Fiddle, fiddle, fiddle, FOOOM!
~Ellery Newcomer''',
            '''If you are careful, and don't get addicted to drugs, you're going to have a great life.
~Woodie Flowers''',
            '''(2011) <Joy Clark> A lot of people think I'm a creeper and in some ways I agree with them.
(2015) <Richard Davey> joy you are a creeper at times.
<Joy Clark> Lol at least I've improved from 2011.
~Joy Clark''',
            '''The general guideline is don't be stupid.
~Brayden Banks''',
            '''Stop microwaving sacred texts.
~Kevin Richmond''',
            '''Life needs improvements. Unfortunately, they never come.
~Ethan Rugg''',
        ]
        response = (random.choice(quotelist))

    if command.startswith(SongRequest):
        songlist = [
            '''Here you go!
Modest Mouse - Float On
https://www.youtube.com/watch?v=88XhEqgmRhM''',
            '''Here you go!
Modest Mouse - Lampshades On Fire
https://www.youtube.com/watch?v=D0Pcu1ECIj0''',
            '''Here you go!
Muse - Resistance
https://www.youtube.com/watch?v=ywpJACWd0dA''',
            '''Here you go!
Modest Mouse - Dashboard
https://www.youtube.com/watch?v=21euaOPVneM''',
            '''Here you go!
Jimmy Eat World - The Middle
https://www.youtube.com/watch?v=pmoEvb0OHLg''',
            '''Here you go!
The Killers - Mr. Brightside
https://www.youtube.com/watch?v=ll8icmGWzMY''',
            '''Here you go!
alt-J - Breezeblocks
https://www.youtube.com/watch?v=WMOd6jz548Y''',
            '''Here you go!
alt-J - Left Hand Free
https://www.youtube.com/watch?v=DbhsJnDEF9g''',
            '''Here you go!
Queen - Bohemian Rhapsody
https://www.youtube.com/watch?v=kPbbfmILrQo''',
            '''Here you go!
Queen & David Bowie - Under Pressure
https://www.youtube.com/watch?v=o8DW-QolX5s''',
            '''Here you go!
Led Zeppelin - Black Dog
https://www.youtube.com/watch?v=yBuub4Xe1mw''',
            '''Here you go!
Foster The People - Don't Stop
https://www.youtube.com/watch?v=VONvSk9qEu8''',
            '''Here you go!
David Bowie - Moonage Daydream
https://www.youtube.com/watch?v=RPUAldgS7Sg''',
            '''Here you go!
Electric Light Orchestra - Mr. Blue Sky
https://www.youtube.com/watch?v=wuJIqmha2Hk''',
            '''Here you go!
Portugal. The Man - Feel It Still
https://www.youtube.com/watch?v=bra_jlITzmI''',
            '''Here you go!
Vampire Weekend - A-Punk
https://www.youtube.com/watch?v=7yINQ_iszOg''',
            '''Here you go!
The Black Keys - Everlasting Light
https://www.youtube.com/watch?v=pIngadE1GCI''',
            '''Here you go!
I Fight Dragons - The Geeks Will Inherit The Earth
https://www.youtube.com/watch?v=YV84nSLr0JU''',
            '''Here you go!
Soundgarden - Spoonman
https://www.youtube.com/watch?v=il0wlnqq3V8''',
        ] 
        response = (random.choice(songlist))

    if command.startswith(SelfDepricatingCommand):
        response = "Pfft. Do it yourself lazy!"

    if command.startswith(HelloWorld):
        response = '''Hello World!
        https://youtu.be/Yw6u6YkTgQ4'''

    if command.startswith(PingPong):
        response = "*Dodges Bits and Bytes*"

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("KitchenBot connected and running!")
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Doh! That wasn't supposed to happen! Check nohup logs either above or below for info on crash.")