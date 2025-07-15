  document.addEventListener('DOMContentLoaded', function() {
  
    var modal = document.getElementById("myModal");
    var btn = document.querySelectorAll(".open_modal");
    var span = document.getElementsByClassName("close")[0];
    let field

    for (i = 0; i < btn.length; i++){
        btn[i].onclick = function() {
            modal.style.display = "block";
            const title_text = this.getAttribute("data-title")
            const placeholder_text = this.getAttribute("data-placeholder")


            field = this.getAttribute("id")
            let placeholder = document.querySelector(".pop_up_input")

            placeholder.setAttribute("placeholder", placeholder_text)
        }
    }

 span.onclick = function() {
        modal.style.display = "none";
    }

   window.onclick = function(event) {
        if (event.target == modal) {
        modal.style.display = "none";
        }
    }

    let submit = document.querySelector("#submit_button")

    submit.onclick = function(){
        let value = document.getElementById("text").value
        
        fetch("/profile_update", {
            method: "POST",
            headers: { "Content-type": "application/json"},
            body: JSON.stringify({
                field: field,
                value: value
            })
        })

        .then(response => response.json())

        

        .catch(error => console.error("Error: ", error))
    }
  });