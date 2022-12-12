// Called after form input is processed
function startConnect() {
    // Generate a random client ID
    // clientID = "clientID-" + parseInt(Math.random() * 100);
    clientID = "mqtt-explorer-b5317878";
    // Fetch the hostname/IP address and port number from the form
    // host = document.getElementById("host").value;
    host = '10.56.131.217';
    // port = document.getElementById("port").value;
    port = '9001';
    // path = '/mqtt';
    // Print output for the user in the messages div
    // document.getElementById("messages").innerHTML += '<span>Connecting to: ' + host + ' on port: ' + port + '</span><br/>';
    // document.getElementById("messages").innerHTML += '<span>Using the following client value: ' + clientID + '</span><br/>';

    // Initialize new Paho client connection
    client = new Paho.MQTT.Client(host, Number(port), clientID);

    // Set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;


    // Connect the client, if successful, call onConnect function
    client.connect({
        onSuccess: onConnect,
        // userName: 'idd',
        // password: 'device@theFarm',
    });
}

// Called when the client connects
function onConnect() {
    // Fetch the MQTT topic from the form
    // topic = document.getElementById("topic").value;
    topic = '#';
    // Print output for the user in the messages div
    // document.getElementById("messages").innerHTML += '<span>Subscribing to: ' + topic + '</span><br/>';
    // document.getElementById("messages").innerHTML += '<span>Subscribing to: ' + '</span><br/>';
    // Subscribe to the requested topic
    client.subscribe(topic);
}

// Called when the client loses its connection
function onConnectionLost(responseObject) {
    console.log("onConnectionLost: Connection Lost");
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost: " + responseObject.errorMessage);
    }
}

// Called when a message arrives
function onMessageArrived(message) {
    console.log("onMessageArrived: " + message.payloadString);
    // document.getElementById("messages").innerHTML += '<span>Topic: ' + message.destinationName + '  | ' + message.payloadString + '</span><br/>';
    document.getElementById('score').innerHTML = message.payloadString
    updateScroll(); // Scroll to bottom of window
}

// Called when the disconnection button is pressed
function startDisconnect() {
    client.disconnect();
    document.getElementById("messages").innerHTML += '<span>Disconnected</span><br/>';
    updateScroll(); // Scroll to bottom of window
}

// Updates #messages div to auto-scroll
function updateScroll() {
    var element = document.getElementById("messages");
    element.scrollTop = element.scrollHeight;
}