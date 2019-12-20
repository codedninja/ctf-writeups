const Discord = require('discord.js');
const client = new Discord.Client();

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
    
    // Loop through Guilds
    client.guilds.forEach((value, key, map) => {

        // Only when we guild Toy factory
        if (value.name === "Toy Factory") {
            // Loop through channels in guild
            value.channels.forEach((v, k, m) => {
                // Only need text channels
                if (v.type === "text") {
                    // Fetch Messages from Channel
                    v.messages.fetch({limit: 100}).then(messages => {
                        messages.forEach((msg, k1, m1) => {
                            console.log('Channel: #'+msg.channel.name+' User: '+msg.author.username+' Message: '+msg.content)
                        });
                    }).catch(console.error);
                }
            });
        }
        console.log(value.name);
    });
});

client.on('guildCreate', guild => {
    console.log("Joined new Guild:"+guild.name);
});

client.on('message', msg => {
    console.log('Guild: '+msg.channel.guild.name+' Channel: #'+msg.channel.name+' User: '+msg.author.username+' Message: '+msg.content)
  
  if (msg.content === 'ping') {
    msg.reply('pong');
  }
});

client.login('NTUxNTcxMjI4ODc2NDcyMzMx.Xfbwag.6m58RqlHgSbX9KDoOSt28FYuznQ');
