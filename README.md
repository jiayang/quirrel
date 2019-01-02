## Quirrel

A Discord bot with super cool commands!

## Running

1. **Clone the repo**

`git clone https://github.com/jiayang/quirrel.git`

2. **Install the requirements**

`pip install -r requirements.txt`

3. **Create your own bot**

Head over to https://discordapp.com/developers and create a new application.
Invite the bot to your Discord server.

4. **Keep your information private**

Create a file `mkdir secret`
Copy your bot's token into `secret/token.txt`

5. **Rest API keys**

- Get your BING MAPS API key from https://www.microsoft.com/en-us/maps/choose-your-bing-maps-api
- Get your DarkSky API key from https://darksky.net/dev

Enter your keys in `secret/keys.json`
```json
{
 "bing_api" : "YOUR KEY HERE",
 "dark_sky" : "YOUR KEY HERE"
}
```
6. **Run the Bot**

Finally, run `python main.py` to complete the process.



<pre>
________        .__                      .__   
\_____  \  __ __|__|_____________   ____ |  |  
 /  / \  \|  |  \  \_  __ \_  __ \_/ __ \|  |  
/   \_/.  \  |  /  ||  | \/|  | \/\  ___/|  |__
\_____\ \_/____/|__||__|   |__|    \___  >____/
       \__>                            \/      
</pre>
