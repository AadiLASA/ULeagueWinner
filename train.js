const fs = require('fs');
const csv = require('csv-parser');
const tf = require('@tensorflow/tfjs-node');

// Function to load CSV data and parse it into a usable format
function loadCSVData(filePath) {
  return new Promise((resolve, reject) => {
    const data = [];
    
    fs.createReadStream(filePath)
      .pipe(csv())
      .on('data', (row) => {
        // Convert row data to feature array and label
        const features = [
          parseInt(row.blue_gold),
          parseInt(row.blue_xp),
          parseInt(row.blue_barons),
          parseInt(row.blue_dragons),
          parseInt(row.blue_towers),
          parseInt(row.blue_inhibitors),
          parseInt(row.blue_riftHeralds),
          parseInt(row.blue_champions),
          parseInt(row.blue_atakhans),
          parseInt(row.blue_hordes),
          parseInt(row.red_gold),
          parseInt(row.red_xp),
          parseInt(row.red_barons),
          parseInt(row.red_dragons),
          parseInt(row.red_towers),
          parseInt(row.red_inhibitors),
          parseInt(row.red_riftHeralds),
          parseInt(row.red_champions),
          parseInt(row.red_atakhans),
          parseInt(row.red_hordes)
        ];
        const label = parseInt(row.label); // 1 for Blue win, 0 for Red win
        data.push({ features, label });
      })
      .on('end', () => {
        resolve(data);
      })
      .on('error', (err) => {
        reject(err);
      });
  });
}

// Function to train the model
async function trainModel() {
  // Load the CSV data
  const data = await loadCSVData('TOTALmatchdata.csv'); // Adjust the path to your CSV file

  // Extract features and labels
  const features = data.map(d => d.features);
  const labels = data.map(d => d.label);

  // Convert to tensors
  const inputTensor = tf.tensor(features);
  const outputTensor = tf.tensor(labels);

  // Define a simple neural network model
  const model = tf.sequential();
  model.add(tf.layers.dense({ units: 32, activation: 'relu', inputShape: [features[0].length] }));
  model.add(tf.layers.dense({ units: 16, activation: 'relu' }));
  model.add(tf.layers.dense({ units: 1, activation: 'sigmoid' }));

  // Compile the model
  model.compile({
    optimizer: 'adam',
    loss: 'binaryCrossentropy',
    metrics: ['accuracy'],
  });

  // Train the model
  await model.fit(inputTensor, outputTensor, {
    epochs: 100,
    batchSize: 10,
    validationSplit: 0.2,
    callbacks: tf.callbacks.earlyStopping({ patience: 5 }),
  });

  // Save the trained model
  await model.save('file://model'); // Save the model to a local directory
  console.log('Model training complete and saved.');
}

// Run the training
trainModel().catch(console.error);
