document.addEventListener('DOMContentLoaded', function() {

    var modal = document.getElementById("myModal");
    var editButtons = document.querySelectorAll(".open_modal");
    var profilePicButton = document.querySelector(".profile_pic_button");
    var closeBtn = document.getElementsByClassName("close")[0];
    
    var inputContent = document.getElementById("input_content");
    var uploadContent = document.getElementById("upload_content");

    var textInput = document.getElementById("text");
    var textArea = document.getElementById("textarea");

    var error_div = document.getElementById("error-message");
    
    let field = null;
    let fieldHTML = null;
    let icon = null;
    if(document.activeElement) document.activeElement.blur();

    editButtons.forEach(function(btn) {
        btn.onclick = function() {
            modal.style.display = "block";
            field = this.getAttribute("id");
            fieldHTML = document.querySelectorAll(`.${field}_text`)
            icon = this

            inputContent.style.display = "block";
            uploadContent.style.display = "none";

            let placeholder_text = this.getAttribute("data-placeholder");
            let title_text = this.getAttribute("data-title");

            if(field === "about_me") {
                textInput.style.display = "none";
                textArea.style.display = "block";
                textArea.value = "";
                textArea.placeholder = placeholder_text;
                textArea.focus();
            } else {
                textArea.style.display = "none";
                textInput.style.display = "block";
                textInput.value = "";
                textInput.placeholder = placeholder_text;
                textInput.focus();
            }
        }
    });

    profilePicButton.onclick = function() {
        modal.style.display = "block";
        field = "profile_picture";


        inputContent.style.display = "none";
        uploadContent.style.display = "block";


        textInput.blur();
        textArea.blur();
    };


    closeBtn.onclick = function() {
        error_div.style.display = "none"
        modal.style.display = "none";
    };


    window.onclick = function(event) {
        if(event.target == modal) {
            error_div.style.display = "none"
            modal.style.display = "none";
        }
    };


    document.getElementById("submit_button").onclick = function(event) {
        event.preventDefault();

        let value;
        if (textInput.style.display === "block") {
            value = textInput.value;
        } else {
            value = textArea.value;
        }

        fetch("profile", {
            method: "POST",
            headers: { 
                "Content-type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({
                field: field,
                value: value,
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Update success:", data);
            if (data.status === "error"){
                error_div = document.getElementById("error-message")
                error_div.style.display = "block"
                error_div.innerHTML = data.message
            }
            else{
                fieldHTML.forEach( element => {
                    element.innerHTML = value;
                })
                icon.style.display = "none";
                modal.style.display = "none";
            }
        })

        .catch(error => console.error("Error: ", error));
    };

});
