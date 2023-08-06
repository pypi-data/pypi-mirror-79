import discord, boto3, configparser, os, sys

version = "0.0.0"

# Get token at: https://discord.com/developers/applications/
config = configparser.ConfigParser()
config_path = "discord_config.ini"

if not os.path.exists(config_path):
    with open(config_path, "w") as file_writer:
        file_writer.write("""[discord]
        token = {PUT TOKEN HERE}
        ignore_user = {PUT USERNAME HERE}
        [aws]
        topic = {PUT TOPIC HERE}
        profile = default""".replace("    ",""))
    print(f"Please update '{config_path}'!")
    sys.exit(0)

config.read(config_path)
session = boto3.session.Session(profile_name=config["aws"]["profile"])
bot_token = config["discord"]["token"]
sns = session.resource('sns').Topic(config["aws"]["topic"])
if sns == None:
    print("SNS was configured poorly!")
    sys.exit(0)

class Notifier(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

        guilds = ""
        for guild in self.guilds:
            guilds = guilds + ", " + str(guild)
        print(f"Watching servers: {guilds[2:]}")

    async def on_message(self, message):
        if "do you see me?" in message.content.lower():
            print(f"I see {message.author}")
            await message.channel.send(":eye: You have been seen! :eye:")

        if str(message.author) in [str(self.user), "The Genuine Wonder#2859"]:
            return
        
        # Format and print mesage
        formatted_message = f"<{message.author}> \"{message.content}\" from #{message.channel} on {message.guild}"
        print(formatted_message)

        # Send notification to SNS
        sns.publish(Message=formatted_message)


def main():
    client = Notifier()
    client.run(bot_token)

if __name__ == "__main__":
    main()
