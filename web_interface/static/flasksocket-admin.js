
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

    function getError() {
        websocketClient.send("check error")
    }

    let timerId = setInterval(getQuantity, 3000);
    let timerId2 = setInterval(getMonitor, 2000);
    let timer3 = setInterval(getError, 2500);

    btnStart.onclick = () => {
        document.querySelector(".modal").style.cssText = "display: none";
        sendCommand("Start");
    }

    btnStop.onclick = () => {
        sendCommand("Stop");
    }

    websocketClient.onmessage = (message) => {
        if (message.data == 'is started') {
        document.getElementById('is_monitoring').textContent = 'Monitoring.......';
        document.getElementById('is_monitoring').style.cssText = "font-size: 35px;";
        btnStart.style.cssText = "background: #0bf702;";
        btnStop.style.cssText = "background: #e8f2fa;";
        }
        else if (message.data == 'not started') {
        document.getElementById('is_monitoring').textContent = ''
        btnStart.style.cssText = "background: #e8f2fa;";
        btnStop.style.cssText = "background: #f70202;";
        }
        else if (message.data == 'camera error') {
            document.querySelector(".modal").style.cssText = "display: flex";
        }
        else {document.getElementById('counter').textContent = message.data}
    }

}, false);