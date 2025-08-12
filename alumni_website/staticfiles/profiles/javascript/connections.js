document.addEventListener("DOMContentLoaded", function(){
    var connectButton = document.querySelector(".connect")
    var requestMentorButton = document.querySelector(".request_mentor")
    var connect_message = document.getElementById("connect_message")
    var mentor_message = document.getElementById("mentor_message")

    if (connectButton){
    connectButton.addEventListener("click", function(event){
        event.preventDefault()
        fetch(connect, {
            method: "POST",
            headers: {  
                "Content-type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                "profile_id": profile_id
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                if (data.message === "Disconnected"){
                    connectButton.textContent = "Connect"
                }
                else if (data.accepted === "True"){
                    connectButton.textContent = "Connected"
                }
                else{
                    connectButton.textContent = "Pending"
                    connect_message.style.display = "block"
                }
            }
        })
        .catch(error => {
            console.error("Error:", error)
        })
    })
    }

    if (requestMentorButton){
    requestMentorButton.addEventListener("click", function(event){
        event.preventDefault()
        fetch(mentor_match, {
            method: "POST",
            headers: {
                "Content-type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                "id": id
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success"){
                if (data.message === "Deleted"){
                    requestMentorButton.textContent = "Request Mentor"
                }
                else if (data.accepted === "True"){
                    requestMentorButton.textContent =  "Mentor Connected"
                }
                else{
                    requestMentorButton.textContent = "Mentor Request Sent"
                    mentor_message.style.display = "block"
                }
            }
        })
        .catch(error => {
            console.error("Error:", error)
        })
    })
    }
})