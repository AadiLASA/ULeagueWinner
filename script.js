// const features = ["death","respawn"]
// //subscribing to game events
// app.overwolf.packages.gep.setRequiredFeatures(features, response => {
//     if(repsonse.success){
//         console.log("successfully subscribed to game events", features);
//     }
//     else{
//         console.error("unsuccessful in subscribing to game events", response.error);
//     }
// });
// //simple logs respawns
// overwolf.games.events.onNewEvents.addListener((event)=> {
//     event.events.forEach(e => {
//         console.log("New Events:", e.name, e.data);
//         if(e.name=="death"){
//             console.log("Player is dead.");
//         }
//         else if(e.name=="respawn"){
//             console.log("player has respawned!");
//         }
//     });
// });




// overwolf.games.events.onNewEvents.addListener((event)=>{
//     event.events.forEach(e=>{
//         console.log("New Char:",e.summoner_info);
//         if(e.summoner_info){
//             updateChar(e.summoner_info);
//         }
//     });
// });




// overwolf.games.getRunningInfo((gameInfo) => {
//     if(gameInfo && gameInfo.isRunning && gameInfo.classId == 5426){
//         console.log("League of Legends Detected");
//     }
// });

function updateStats(data) {
    document.getElementById("champ").innerHTML= `<b>Champion: </b> ${data.champ}`;
    document.getElementById("role").innerHTML =`<b>Role: </b> ${data.role}`;;
    document.getElementById("kda").innerHTML = `<b>KDA: </b> ${data.kda}`;;
    document.getElementById("csmin").innerHTML = `<b>CS/MIN: </b> ${data.csmin}`;;
    //document.getElementById("level").innerText = data.level;
    //document.getElementById("gold-diff").innerText = data.goldDiff;
   // document.getElementById("win-diff").innerText = data.winDiff;
}

setInterval(() => {
    const sampleData = {
        champ: "Yone",
        role: Math.floor(Math.random() * 200),
        kda: Math.floor(Math.random() * 15000),
        csmin: Math.floor(Math.random() * 10)
       // level: Math.floor(Math.random() * 18) + 1,
      //  goldDiff: Math.floor(Math.random() * 5000) - 2500,
      //  winDiff: Math.floor(Math.random() * 100)
    };
    updateStats(sampleData);
}, 1000);
