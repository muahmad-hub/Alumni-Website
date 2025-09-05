window.addEventListener('DOMContentLoaded', function() {
    get_teacher("", "")
})

document.getElementById("searchInput").addEventListener("input", function() {
    query = this.value
    subject = document.getElementById("teacher").value
    get_teacher(query, subject)
})

document.getElementById("teacher").addEventListener("change", function() {
    subject = this.value
    query = document.getElementById("searchInput").value
    get_teacher(query, subject)
})

function get_teacher(query, subject){
    if (subject === "Subject"){
        subject = ""
    }
    fetch(`${SearchURL}?q=${encodeURIComponent(query)}&subject=${encodeURIComponent(subject)}`)
    .then(response => response.json())
    .then(data => {
       display_data(data)
    })
    .catch(error =>{
        console.log(error)
    })

}

function display_data(data){
    let container = document.getElementById("alumni-container")
    container.innerHTML = ""

    if (!data.results || data.results.length === 0){
        container.innerHTML = "<div class='col-12 text-center'><h4 data-aos='fade-up' data-aos-delay='300'>No teachers found</h4></div>"
    }
    else{
        data.results.forEach(teacher => {
            let teacher_info = `
                <div class="col-lg-4 col-md-6 mb-4" data-aos="fade-up" data-aos-delay="300">
                    <div class="alumni-card">
                        <div class="mentor-content">
                            <div class="flex-container">
                                <img src="${teacher.profile_url || '/static/images/profile_image.jpg'}" alt="Teacher" class="img-fluid profile-image" style="max-width: 120px; height: auto; float: left; margin-right: 15px;">
                                <div class="mentor-details">
                                    <h4>${teacher.first_name || ""} ${teacher.last_name || ""}</h4>
                                    <p class="mentor-class">Teaching ${teacher.subject || ""}</p>
                                    <div id="view-profile-container">
                                        <a href="" class="view-profile" data-user-id="${teacher.id}">View Profile<i class="bi bi-arrow-right"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `
            container.innerHTML += teacher_info
        })
    }

    document.querySelectorAll(".view-profile").forEach(temp_var => {
        temp_var.addEventListener("click", function(e){
            e.preventDefault();
            const id = this.getAttribute("data-user-id");
            window.location.href = `/profile/view_profile/${id}?view=alumni`;
        });
    });
}
