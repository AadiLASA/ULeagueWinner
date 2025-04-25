let model, dmatrix;
let gameState = {
  blue_gold: 0,
  blue_xp: 0,
  blue_barons: 0,
  blue_dragons: 0,
  blue_towers: 0,
  blue_inhibitors: 0,
  blue_riftHeralds: 0,
  blue_champions: 0,
  blue_atakhans: 0,
  blue_hordes: 0,
  red_gold: 0,
  red_xp: 0,
  red_barons: 0,
  red_dragons: 0,
  red_towers: 0,
  red_inhibitors: 0,
  red_riftHeralds: 0,
  red_champions: 0,
  red_atakhans: 0,
  red_hordes: 0,
};

// 🔁 Update the display and run the model
function updatePrediction() {
  const input = [[
    gameState.blue_gold,
    gameState.blue_xp,
    gameState.blue_barons,
    gameState.blue_dragons,
    gameState.blue_towers,
    gameState.blue_inhibitors,
    gameState.blue_riftHeralds,
    gameState.blue_champions,
    gameState.blue_atakhans,
    gameState.blue_hordes,
    gameState.red_gold,
    gameState.red_xp,
    gameState.red_barons,
    gameState.red_dragons,
    gameState.red_towers,
    gameState.red_inhibitors,
    gameState.red_riftHeralds,
    gameState.red_champions,
    gameState.red_atakhans,
    gameState.red_hordes,
  ]];

  dmatrix = new xgboost.DMatrix(input);
  const prediction = model.predict(dmatrix);
  const prob = (prediction[0] * 100).toFixed(2);
  document.getElementById('prediction').innerText = `${prob}%`;
}

// 🚀 Load the model
async function initModel() {
  model = await xgboost.loadModel('model.json');
  console.log("Model loaded");
}

// 📡 Connect Overwolf Events
function initOverwolfListeners() {
  overwolf.games.events.onNewEvents.addListener(e => {
    for (const event of e.events) {
      switch (event.name) {
        case "gold":
          gameState[event.data.team === "blue" ? "blue_gold" : "red_gold"] = parseInt(event.data.value);
          break;
        case "xp":
          gameState[event.data.team === "blue" ? "blue_xp" : "red_xp"] = parseInt(event.data.value);
          break;
        case "dragon_kill":
          gameState[event.data.team === "blue" ? "blue_dragons" : "red_dragons"] += 1;
          break;
        case "baron_kill":
          gameState[event.data.team === "blue" ? "blue_barons" : "red_barons"] += 1;
          break;
        case "rift_herald_kill":
          gameState[event.data.team === "blue" ? "blue_riftHeralds" : "red_riftHeralds"] += 1;
          break;
        case "tower_kill":
          gameState[event.data.team === "blue" ? "blue_towers" : "red_towers"] += 1;
          break;
        case "inhibitor_kill":
          gameState[event.data.team === "blue" ? "blue_inhibitors" : "red_inhibitors"] += 1;
          break;
        case "champion_kill":
          gameState[event.data.team === "blue" ? "blue_champions" : "red_champions"] += 1;
          break;
        case "atakhan_collected":
          gameState[event.data.team === "blue" ? "blue_atakhans" : "red_atakhans"] += 1;
          break;
        case "horde_kill":
          gameState[event.data.team === "blue" ? "blue_hordes" : "red_hordes"] += 1;
          break;
      }
    }

    updatePrediction();
  });
}

// 🔄 Init everything
window.addEventListener("load", async () => {
  await initModel();
  initOverwolfListeners();
});

