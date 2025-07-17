window.addEventListener('DOMContentLoaded', function() {
    get_alumni("")
})

document.getElementById("alumni-container").addEventListener("click", function(event){
    card = event.target.closest(".alumni-card")
    if (card){
        id = card.getAttribute("data-user-id")
        console.log(id)
        window.location.href = `/view_profile/${id}`
    }
    })


document.getElementById("searchInput").addEventListener("input", function() {
    query = this.value

    if (query !== ""){
        get_alumni(query)
    }
    else{
        get_alumni("")
    }
})

function get_alumni(query){
    fetch(`/mentor_search_directory?q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
        alumni_container = document.getElementById("alumni-container")
        alumni_container.innerHTML  = ""

        if (!data.results || data.results.length === 0){
            alumni_container.innerHTML += "<h1>No Results</h1>"
        }
        else{

        data.results.forEach(alumni => {
            alumni_info = `
                <div class="col-12 col-sm-6 col-lg-4">
                    <div class="card h-100 alumni-card" data-user-id = "${alumni.id}">
                        <img src="${alumni.profile_url || '/static/images/profile_image.jpg'}" class="card-img-top" alt="Alumni_card">
                        <div class="card-body">
                        <h5 class="card-title">${alumni.name}</h5>
                    `

            if (alumni.skills && alumni.skills.length > 0) {
                alumni_info += '<span class="card-text">Skills: </span>'
            alumni.skills.forEach(skill => {
                alumni_info += `<span class="skill card-text">${skill}, </span>`;
            })}

            alumni_info +=  `
                            <p class="card-text">Class of ${alumni.graduation_year}</p>
                            <p class="card-text">Studying ${alumni.career} at ${alumni.university}</p>
                        </div>
                    </div>
                </div>
            `

            alumni_container.innerHTML += alumni_info
        })

        }
    })
    .catch(error =>{
        console.log(error)
    })

}

function open_profile(id){
    window.location.href = `/view_profile/${id}`
}