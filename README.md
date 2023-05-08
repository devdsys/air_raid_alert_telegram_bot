# air_raid_alert_telegram_bot
Here I'm sharing my solution to a real problem I encountered

At the beginning of the full-scale war launched by russia against Ukraine, there was a problem with air raid alert in my village. Especially, there was no option to turn on and off the siren remotely. For example, if an air raid started at night, a responsible person should go from their home to a place where hardware is installed, open the building with a key, and turn on the siren. Then wait in a shelter for the end of the alert and turn off the siren.

So, they proposed me to create some solution for remote control of alert in a village. 

As a result, my solution provides turning on and off the siren takes no more than 2 seconds remotely from any device with access to the internet and a Telegram bot. After a few months, my solution was replaced with a new system, but it did its job well.

**Let's take more details.**

In the beginning, for air raid alert in the village was used a laptop connected to the audio amplifier, which connected to the speaker.

During those months I tried different approaches for different devices:

 <img src="https://github.com/devdsys/air_raid_alert_telegram_bot/blob/main/visualization.png" width="725" height="500"> 

1. Raspberry Pi. I needed a quick solution, so I wrote a simple [Python script](https://github.com/devdsys/air_raid_alert_telegram_bot/blob/main/1_air_raid_alert_Raspberry_Pi.py) for my Rapsberry PI and set it up instead of a laptop. 
Principe: Raspberry Pi plays an air raid alert on repeat, but the sound is muted. When a telegram user sends a specific word from a list to the chat system volume changes to 100% and the speaker produces a sound. When the telegram bot receives a stop word from a list, the system volume changes to 0%.

Advantage: quick solution for remote controlling.
Disadvantage: everyone with access to the bot and who knows words from a list can control the system.

2. Laptop on Windows. I needed my Raspberry Pi for another project, so I wrote [the script](https://github.com/devdsys/air_raid_alert_telegram_bot/blob/main/2_air_raid_alert_Windows.py) for Windows with the disadvantages fixing. In this script were provided division on users and admins. Everyone can check the status of the system (whether is air raid alert active or not), but only admins can control the system. Also, the admin can remotely add another admin using the same chat.

Advantage: access is distributed based on the status of the user (user / admin).
Disadvantage: over time the laptop was used for other tasks, so different people could have access to the laptop, the system, and the script. 

3. ESP8266. For this solution laptop was replaced with an old mobile phone, which functioned just as a media player with the siren on repeat. As a server was using an ESP8266 module, for which was written [a script](https://github.com/devdsys/air_raid_alert_telegram_bot/blob/main/3_air_raid_alert_ESP8266.ino) in the Arduino app. When ESP8266 receives an "ON" message via telegram bot API, a high-level signal sends from pin to relay and an audio signal comes to the speaker. When the message is "OFF" the wire connection between the audio amplifier and speaker breaks on the relay and the speaker mutes. 

Advantages: cheap (don't need to use a laptop of Raspberry Pi); if the power is turned off, the system will restart itself after the power is restored due to a hardware feature.
Disadvantages: system includes more hardware elements; setting up requires some engineering skills.
