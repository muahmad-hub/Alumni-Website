document.addEventListener('DOMContentLoaded', function() {

    var modal = document.getElementById("myModal");
    var editButtons = document.querySelectorAll(".open_modal");
    var profilePicButton = document.querySelector(".profile_pic_button");
    var closeBtn = document.getElementsByClassName("close")[0];
    
    var inputContent = document.getElementById("input_content");
    var uploadContent = document.getElementById("upload_content");

    var textInput = document.getElementById("text");
    var textArea = document.getElementById("textarea");
    
    let field = null;

    // Blur any focused element on load to remove cursor
    if(document.activeElement) document.activeElement.blur();

    // Handle clicking pencil/edit buttons (show input fields)
    editButtons.forEach(function(btn) {
        btn.onclick = function() {
            modal.style.display = "block";
            field = this.getAttribute("id");

            // Show input fields, hide upload section
            inputContent.style.display = "block";
            uploadContent.style.display = "none";

            // Set placeholder and clear inputs
            let placeholder_text = this.getAttribute("data-placeholder");
            let title_text = this.getAttribute("data-title");

            if(field === "about") {
                // Show textarea for 'about'
                textInput.style.display = "none";
                textArea.style.display = "block";
                textArea.value = "";
                textArea.placeholder = placeholder_text;
                textArea.focus();
            } else {
                // Show text input for others
                textArea.style.display = "none";
                textInput.style.display = "block";
                textInput.value = "";
                textInput.placeholder = placeholder_text;
                textInput.focus();
            }
        }
    });

    // Handle clicking profile picture button (show file upload)
    profilePicButton.onclick = function() {
        modal.style.display = "block";
        field = "profile_picture"; // Or any value you want for backend

        // Show upload, hide input fields
        inputContent.style.display = "none";
        uploadContent.style.display = "block";

        // Blur inputs if any focused
        textInput.blur();
        textArea.blur();
    };

    // Close modal when clicking the X
    closeBtn.onclick = function() {
        modal.style.display = "none";
    };

    // Close modal when clicking outside the modal content
    window.onclick = function(event) {
        if(event.target == modal) {
            modal.style.display = "none";
        }
    };

    // Submit button for text update
    document.getElementById("submit_button").onclick = function(event) {
        event.preventDefault();  // prevent default form submission

        let value = textInput.style.display === "block" ? textInput.value : textArea.value;

        fetch("/profile_update", {
            method: "POST",
            headers: { "Content-type": "application/json" },
            body: JSON.stringify({
                field: field,
                value: value
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Update success:", data);
            modal.style.display = "none";
            // Optionally update the profile fields on the page here
        })
        .catch(error => console.error("Error: ", error));
    };

    // The file upload button just submits form normally, no JS needed here

});
