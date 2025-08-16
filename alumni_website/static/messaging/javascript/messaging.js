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
    convertTimestampsToUserTimezone();
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
      let timestamp;
      
      if (data.utc_timestamp) {
        const utcDate = new Date(data.utc_timestamp + ' UTC');
        timestamp = utcDate.toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit'
        });
      } else {
        const now = new Date();
        timestamp = now.toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit'
        });
      }

      if (data.sender_id == currentUserId){
          html = `
              <div class="message-wrapper sent" data-message-id="${data.message_id || ''}">
                  <div class="message sent">${data.message}</div>
                  <div class="message-timestamp sent">${timestamp}</div>
              </div>
          `;
      }
      else {
          html = `
              <div class="message-wrapper received" data-message-id="${data.message_id || ''}">
                  <div class="message received">${data.message}</div>
                  <div class="message-timestamp received">${timestamp}</div>
              </div>
          `;
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

  function convertTimestampsToUserTimezone() {
    const timestamps = document.querySelectorAll('.message-timestamp[data-utc-time]');
    
    timestamps.forEach(timestamp => {
      const utcTime = timestamp.getAttribute('data-utc-time');
      if (utcTime) {
        const utcDate = new Date(utcTime + ' UTC');
        const localTime = utcDate.toLocaleTimeString('en-US', {
          hour12: false,
          hour: '2-digit',
          minute: '2-digit'
        });
        timestamp.textContent = localTime;
      }
    });
  }
});