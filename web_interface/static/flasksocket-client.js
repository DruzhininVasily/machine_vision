
document.addEventListener('DOMContentLoaded', function(){
    var reqContainer = document.querySelector(".submit-bar");

    let websocketClient  = new WebSocket("ws://192.168.0.57:5000/show_photo");


    function renderSubbar() {
        var newContainer = document.createElement('div');
        newContainer.innerHTML =
            '<h1 id="alert">Залив!!!</h1>' +
            "<input id='submit' type='button' value='Подтвердить'>";
            newContainer.className = "submit-bar";
            newContainer.style.cssText = 'background-color: #ffd1d1; border: 1px solid black; border-radius: 5px; padding: 50px; max-height: 200px; text-align: center;';
        reqContainer.parentNode.replaceChild(newContainer, reqContainer);
        const buttonSubmit = document.querySelector("#submit");
        const textAlert = document.querySelector("#alert");
        buttonSubmit.style.cssText = 'padding: 10px; width: 90%; margin-top: 80px; border-radius: 5px; background-color: #eeffcc; border: 1px solid black;';
        textAlert.style.cssText = 'font-weight: 900; color: red;';

        buttonSubmit.onclick = () => {
        websocketClient.send("Подтверждено");
        reqContainer = document.createElement('div');
        reqContainer.className = "submit-bar";
        reqContainer.innerHTML = "";
        newContainer.parentNode.replaceChild(reqContainer, newContainer);
    }
    }

    function getSubmit() {
        websocketClient.send("get submit")
    }

    function getImg() {
        websocketClient.send("Дай фото")
    };

    let timerId = setInterval(getImg, 2000);
    let timerSubmit = setInterval(getSubmit, 1000);

    websocketClient.onmessage = (message) => {
        if (message.data == 'request submit') {renderSubbar()}
        else {document.getElementById("Image").src=message.data}
    }

}, false);