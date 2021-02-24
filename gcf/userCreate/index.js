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
  const payload = Buffer.from(message.data, 'base64').toString();
  const telemetry = JSON.parse(payload);
  const attributes = message.attributes;
  const deviceId = attributes.deviceId;
  
  _timestamp = admin.database.ServerValue.TIMESTAMP;
  data = {"timestamp":_timestamp};
  
  db.collection(`device/${deviceId}/boot`).add(
     bootMsg
  ).then((writeResult) => {
    console.log({'result': 'Message with ID: ' + writeResult.id + ' added.'});
    return;
  }).catch((err) => {
    console.log(err);
    return;
  });

  callback();
};
