add_message = function () {
    add_input(document.getElementById('user_message').value)
}

add_filename = function () {
    add_input(document.getElementById('file').files[0].name)
    if (document.getElementById('q').value) {
        add_input(document.getElementById('q').value)
    }
}

add_input = function (input_value) {
    let message = document.getElementById('chat-window');
    message.innerHTML += `<div class="message sent"><p>${input_value}</p></div>`;
}