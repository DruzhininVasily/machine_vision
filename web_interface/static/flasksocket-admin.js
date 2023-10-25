
document.addEventListener('DOMContentLoaded', function(){
    var btnStop = document.querySelector(".stop");
    var btnStart = document.querySelector(".start");

    let websocketClient  = new WebSocket("ws://192.168.0.57:5000/control");

    function sendCommand(command) {
        websocketClient.send(command)
    }

    function getQuantity() {
        websocketClient.send("Get count")
    };

    function getMonitor() {
        websocketClient.send("is started")
    }

    let timerId = setInterval(getQuantity, 5000);
    let timerId2 = setInterval(getMonitor, 3000);

    btnStart.onclick = () => {
        sendCommand("Start");
    }

    btnStop.onclick = () => {
        sendCommand("Stop");
    }

    websocketClient.onmessage = (message) => {
        if (message.data == 'is started') {
        document.getElementById('is_monitoring').textContent = 'Monitoring.......';
        document.getElementById('is_monitoring').style.cssText = "font-size: 35px;"
        }
        else if (message.data == 'not started') {document.getElementById('is_monitoring').textContent = ''}
        else {document.getElementById('counter').textContent = message.data}
    }

}, false);