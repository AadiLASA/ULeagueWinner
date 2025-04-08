const features = ["death","respawn"]
//subscribing to game events
app.overwolf.packages.gep.setRequiredFeatures(features, response => {
    if(repsonse.success){
        console.log("successfully subscribed to game events", features);
    }
    else{
        console.error("unsuccessful in subscribing to game events", response.error);
    }
});
//simple logs respawns
overwolf.games.events.onNewEvents.addListener((event)=> {
    event.events.forEach(e => {
        console.log("New Events:", e.name, e.data);
        if(e.name=="death"){
            console.log("Player is dead.");
        }
        else if(e.name=="respawn"){
            console.log("player has respawned!");
        }
    });
});



function updateChar(name){
    document.getElementById("champion-name").innerHTML = `<i class="fas fa-dragon icon"></i> Champion: ${data.champion}`;
}
//  cs/min calculator
const cs=document.getElementById("cs");


overwolf.games.events.onNewEvents.addListener((event)=>{
    event.events.forEach(e=>{
        console.log("New Char:",e.summoner_info);
        if(e.summoner_info){
            updateChar(e.summoner_info);
        }
    });
});




overwolf.games.getRunningInfo((gameInfo) => {
    if(gameInfo && gameInfo.isRunning && gameInfo.classId == 5426){
        console.log("League of Legends Detected");
    }
});

