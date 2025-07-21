document.addEventListener("DOMContentLoaded", function() {
    var form = document.querySelector(".chat-input")
    var input = document.getElementById("message_input")
    var container = document.querySelector(".chat-messages")

    form.addEventListener("submit", function(event) {
        event.preventDefault();
    });

    function scrollToBottom() {
        container.scrollTop = container.scrollHeight;
    }

    window.onload = function(){
        scrollToBottom()
    }

    document.body.addEventListener('htmx:afterRequest', function(event) {
        if (event.target.closest('.chat-input')) {
            input.value = ""
            scrollToBottom()
        }
    });
});
