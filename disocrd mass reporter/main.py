import discord

def get_bot_token():
    return input("Please enter your Discord bot token: ")

def display_menu():
    print("wh1te mass reporter menu ")
    print("1. run mass reporter")
    print("2. Exit")
    choice = input("choose an option (1 or 2): ")
    return choice

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')  

async def mass_report(channel_id, user_id, reason):
    try:
        channel = client.get_channel(channel_id)  
        if channel is None:
            print("Channel not found.")
            return

        user = await client.fetch_user(user_id)  
        if user is None:
            print("User not found.")
            return

        report_message = f'/report {user.id} - Reason: {reason}'
        await channel.send(report_message)  
        print(f'Reported {user.name} in {channel.name} for: {reason}')

    except Exception as e:
        print(f'An error occurred: {e}')

@client.event
async def on_message(message):
    if message.content.startswith('!massreport'):
        try:
        
            _, channel_id, user_id, *reason = message.content.split()
            reason = ' '.join(reason)  
            await mass_report(int(channel_id), int(user_id), reason)
        except ValueError:
            await message.channel.send("Invalid command format. Use: !massreport <channel_id> <user_id> <reason>")

if __name__ == "__main__":
    while True:
        choice = display_menu()
        if choice == '1':
            TOKEN = get_bot_token()  
            try:
                client.run(TOKEN)  
            except Exception as e:
                print(f"Failed to run the bot: {e}")
        elif choice == '2':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please choose 1 or 2.")