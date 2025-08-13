document.addEventListener('DOMContentLoaded', function () {

  const form = document.querySelector('.chat-input');
  const messageInput = document.getElementById('message_input');
  const chatBox = document.getElementById('chat-box');
  const onlineCount = document.getElementById('online_count')

  const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
  const chatSocket = new WebSocket(
    `${wsScheme}://${window.location.host}/ws/message/${groupName}/`
  )

  window.onload = function () {
    scroll_to_bottom();
  }

  chatSocket.onopen = function () {
    console.log('WebSocket connection established');
    scroll_to_bottom();
  }
  
  chatSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    let html;

    
    if(data.message){
      if (data.sender_id == currentUserId) {
          html = `<div class="message sent">${data.message}</div>`;
      } else {
          html = `<div class="message received">${data.message}</div>`;
      }
      chatBox.insertAdjacentHTML('beforeend', html);
      scroll_to_bottom();
      }

      if (data.online_count !== undefined) {
        onlineCount.innerHTML = data.online_count
      }
    }

  chatSocket.onclose = function () {
    console.log('WebSocket connection closed');
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const message = messageInput.value.trim()
    if (!message) return
    
    if (chatSocket.readyState === WebSocket.OPEN) {
      chatSocket.send(JSON.stringify({ message }))
      messageInput.value = ''
    } else {
      alert('WebSocket connection is closed.')
    }
  });

  function scroll_to_bottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }
});
