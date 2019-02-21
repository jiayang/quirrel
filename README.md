## Quirrel

A Discord bot with super cool commands!

## Add to your server
To add this bot to your server, click [here](https://discordapp.com/api/oauth2/authorize?client_id=528275565434896394&permissions=37088336&scope=bot) and follow the instructions! 



## Self Download (not recommended)

1. **Clone the repo**

`git clone https://github.com/jiayang/quirrel.git`

2. **Install the requirements**

`pip install -r requirements.txt`

3. **Create your own bot**

Head over to https://discordapp.com/developers and create a new application. <br>
Invite the bot to your Discord server.

4. **Keep your information private**

Create a file `mkdir secret` <br>
Copy your bot's token into `secret/token.txt`

5. **Rest API keys**

- Get your BING MAPS API key from https://www.microsoft.com/en-us/maps/choose-your-bing-maps-api
- Get your DarkSky API key from https://darksky.net/dev
- Get your YouTube Search v3 key from https://console.developers.google.com/apis/dashboard

Enter your keys in `secret/keys.json`
```json
{
 "bing_api" : "YOUR KEY HERE",
 "dark_sky" : "YOUR KEY HERE",
 "youtube" : "YOUR KEY HERE"
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
