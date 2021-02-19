const admin = require('firebase-admin');
admin.initializeApp();
var db = admin.firestore();

/**
 * Background Cloud Function to be triggered by Pub/Sub.
 * This function gets executed when telemetry data gets
 * send to IoT Core and consequently a Pub/Sub message
 * gets published to the selected topic.
 *
 * @param {Object} event The Cloud Functions event.
 * @param {Function} callback The callback function.
 */
exports.telemetryToFirestore = (message, context, callback) => {
  const pubsubMessage = message.data;

  if (!message.data) {
    throw new Error('No telemetry data was provided!');
  }
  const payload = Buffer.from(message.data, 'base64').toString();
  const telemetry = JSON.parse(payload);
  const attributes = message.attributes;
  const deviceId = attributes.deviceId;
  
  if (!telemetry.timestamp){
    if(!telemetry.deviceTime) {
      throw new Error('No data timestamp was provided!');
    }
  }

  _timestamp = admin.database.ServerValue.TIMESTAMP;
  if (telemetry.timestamp) {_timestamp = telemetry.timestamp;}
  else if (telemetry.deviceTime) {_timestamp = telemetry.deviceTime;}

  measurement = {"timestamp":_timestamp};
  
  if (telemetry.temperature) { measurement["temperature"] = telemetry.temperature;}
  if (telemetry.PH) { measurement["pH"] = telemetry.PH;}
  if (telemetry.EC) { measurement["EC"] = telemetry.EC;}
  else if (telemetry.conductivity) { measurement["EC"] = telemetry.conductivity;}
  if (telemetry.DO) { measurement["DO"] = telemetry.DO;}
  if (telemetry.totalDissolvedSolids) { measurement["totalDissolvedSolids"] = telemetry.totalDissolvedSolids;}
  if (telemetry.salinity) { measurement["salinity"] = telemetry.salinity;}
  if (telemetry.specificGravity) { measurement["specificGravity"] = telemetry.specificGravity;}
  if (telemetry.saturation) { measurement["saturation"] = telemetry.saturation;}
  if (telemetry.ORP) { measurement["ORP"] = telemetry.ORP;}
  else if (telemetry.oxidationReductionPotential) { measurement["ORP"] = telemetry.oxidationReductionPotential;}
  if (telemetry.sensorType) { measurement["sensorType"] = telemetry.sensorType;}
  if (telemetry.voc) { measurement["voc"] = telemetry.voc;}
  if (telemetry.humidity) { measurement["humidity"] = telemetry.humidity;}
  if (telemetry.pressure) { measurement["pressure"] = telemetry.pressure;}
  if (telemetry.altitude) { measurement["altitude"] = telemetry.altitude;}
  if (telemetry.dewPoint) { measurement["dewPoint"] = telemetry.dewPoint;}
  if (telemetry.lux) { measurement["lux"] = telemetry.lux;}
  if (telemetry.infrared) { measurement["infrared"] = telemetry.infrared;}
  if (telemetry.visible) { measurement["visible"] = telemetry.visible;}
  if (telemetry.full_spectrum) { measurement["full_spectrum"] = telemetry.full_spectrum;}
  if (telemetry.CO2) { measurement["CO2"] = telemetry.CO2;}
  if (telemetry.moisture) { measurement["moisture"] = telemetry.moisture;}
  if (telemetry.moisturePercent) { measurement["moisturePercent"] = telemetry.moisturePercent;}
  if (telemetry.rootTemp) { measurement["rootTemp"] = telemetry.rootTemp;}
  if (telemetry.rootLight) { measurement["rootLight"] = telemetry.rootLight;}
  if (telemetry.minMoist) { measurement["minMoist"] = telemetry.minMoist;}
  if (telemetry.maxMoist) { measurement["maxMoist"] = telemetry.maxMoist;}
  
  db.collection(`device/${deviceId}/measurements`).add(
     measurement
  ).then((writeResult) => {
    console.log({'result': 'Message with ID: ' + writeResult.id + ' added.'});
    return;
  }).catch((err) => {
    console.log(err);
    return;
  });

  callback();
};

