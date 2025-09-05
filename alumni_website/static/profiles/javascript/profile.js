document.addEventListener('DOMContentLoaded', function() {
    var employed = document.getElementById("employed");
    var notEmployed = document.getElementById("not_employed");

    var jobSection = document.getElementById("job_section");
    var yesPreference = document.getElementById("yes-preference");
    var noPreference = document.getElementById("no-preference");

    if (employed){
        if (employed.checked) {
            jobSection.style.display = "block";
        } else {
            jobSection.style.display = "none";
        }

    employed.addEventListener("change", function () {
        if (employed.checked) {
            jobSection.style.display = "block";
            change_employed_status("True");
        } else {
            jobSection.style.display = "none";
            change_employed_status("False");
        }
    })

    notEmployed.addEventListener("change", function () {
        if (notEmployed.checked) {
            jobSection.style.display = "none";
            change_employed_status("False");
        }
    })
    }
        
    document.addEventListener("click", function(event){
        if (event.target.classList.contains("connect") || event.target.classList.contains("decline")){
            var contactDetailsDiv = event.target.closest(".connect-details")
            var isAcceptButton = event.target.classList.contains("connect")
            var container = event.target.closest(".contact-item")
            if (isAcceptButton){
                sendConnectionDetails(contactDetailsDiv.getAttribute("data-url-accept"), container)
            }
            else{
                sendConnectionDetails(contactDetailsDiv.getAttribute("data-url-decline"), container)
            }
        }    
    })

    yesPreference.addEventListener("click", function() {
        fetch(yesDigestEmailURL, {
            method: "POST",
            headers: {
                "X-CSRFToken": `${csrfToken}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                console.log(data.message)
                closePreferenceModal()
            } else {
                console.error(data.message)
            }
        })
        .catch(error => {
            console.error("Fetch failed:", error)
        })
    })

    noPreference.addEventListener("click", function() {
        fetch(noDigestEmailURL, {
            method: "POST",
            headers: {
                "X-CSRFToken": `${csrfToken}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                console.log(data.message)
                closePreferenceModal()
            } else {
                console.error(data.message)
            }
        })
        .catch(error => {
            console.error("Fetch failed:", error)
        })
    })

})

function closePreferenceModal(){
    let preferenceModalElement = document.getElementById("emailPreferences")
    let preferenceModal = bootstrap.Modal.getInstance(preferenceModalElement)
    preferenceModal.hide()
}

function sendConnectionDetails(url, container){
    fetch(url, {
        method: "POST",
        headers: {
        "Content-type": "application/json",
        "X-CSRFToken": csrfToken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            container.remove()
        } else {
            alert('Error: ' + data.message);
        }
    })
}

function change_employed_status(value){
    fetch(edit_employment_status, {
    method: "POST",
    headers: {
        "Content-type": "application/json",
        "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
        "has_job": value
    })
    })

    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    })

}