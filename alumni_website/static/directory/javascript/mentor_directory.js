window.addEventListener('DOMContentLoaded', function() {
    get_alumni("", "", "")
})

document.getElementById("searchInput").addEventListener("input", function() {
    query = this.value
    batch_year = document.getElementById("batch_year").value
    university = document.getElementById("university").value
    get_alumni(query, batch_year, university)
})

document.getElementById("batch_year").addEventListener("change", function() {
    batch_year = this.value
    query = document.getElementById("searchInput").value
    university = document.getElementById("university").value
    get_alumni(query, batch_year, university)
})

document.getElementById("university").addEventListener("change", function() {
    university = this.value
    query = document.getElementById("searchInput").value
    batch_year = document.getElementById("batch_year").value
    get_alumni(query, batch_year, university)
})


function get_alumni(query, batch_year, university){
    if (batch_year === "Batch Year"){
        batch_year = ""
    }
    if (university === "University"){
        university = ""
    }
    fetch(`${mentorSearchURL}?q=${encodeURIComponent(query)}&batch_year=${encodeURIComponent(batch_year)}&uni=${university}`)
    .then(response => response.json())
    .then(data => {
       display_data(data)
    })
    .catch(error =>{
        console.log(error)
    })

}

function display_data(data){
    alumni_container = document.getElementById("alumni-container")
    alumni_container.innerHTML  = ""

    if (!data.results || data.results.length === 0){
        alumni_container.innerHTML += "<h1>No Results</h1>"
    }
    else{
    data.results.forEach(alumni => {
        alumni_info = `
                <div class="col-lg-4 col-md-6 mb-4" data-aos="fade-up" data-aos-delay="300">
                    <div class="alumni-card">
                    <div class="mentor-content">
                        <div class="flex-container">
                        <img src="/static/images/profile_image.jpg" alt="Mentor" class="img-fluid profile-image" style="max-width: 120px; height: auto; float: left; margin-right: 15px;">
                        <div class="mentor-details">
                            <h4>${alumni.first_name} ${alumni.last_name}</h4>
                            <p class="mentor-class">Class of ${alumni.graduation_year}</p>
                            <span class="mentor-position">${alumni.major_uni} at ${alumni.university}</span>
                `
        if (alumni.has_job){
            alumni_info +=  `
                <span class="mentor-position"> | ${alumni.role} at ${alumni.employer}</span>
            `
        }
        if (alumni.skills && alumni.skills.length > 0 && alumni.skills[0] !== "") {
            alumni_info += '<p class="mentor-skills">Skills: ';
            alumni.skills.forEach(skill => {
                alumni_info += `${skill}, `;
            });
            alumni_info += `</p>`;
        }
        alumni_info += `
                        <div id="view-profile-container"><a href="" class="view-profile" data-user-id = "${alumni.id}">View Profile<i class="bi bi-arrow-right"></i></a></div>
                    </div>
                    </div>
                </div>
                </div>
            </div>
        `
        alumni_container.innerHTML += alumni_info
    })
    }




    document.querySelectorAll(".view-profile").forEach(temp_var => {
        temp_var.addEventListener("click", function(e){
            e.preventDefault();
            const id = this.getAttribute("data-user-id");
            window.location.href = `/profile/view_profile/${id}`;
        });
    });


















}

function open_profile(id){
    window.location.href = `/view_profile/${id}`
}
