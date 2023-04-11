const message_input = document.getElementById("message_input");
const message_div = document.getElementById("messages");
const chat_form = document.getElementById("chat-form");
const socket = io();

socket.on("connect", () => {
    console.log("Connection made!");
})
socket.on("chat_msg", (data) => {
    const message = document.createElement("h1");
    console.log("Got a response!");
    message.innerHTML = data.username + ": " + data.msg;
    message_div.appendChild(message);
})

chat_form.onsubmit = (e) => {
    e.preventDefault();
    socket.emit("send_msg", message_input.value);
    message_input.value = "";
}
