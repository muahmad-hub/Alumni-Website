window.addEventListener('DOMContentLoaded', function() {
    get_chats("")
})

document.getElementById("search-messages").addEventListener("input", function() {
    query = this.value

    if (query !== ""){
        get_chats(query)
    }
    else{
        get_chats("")
    }
})


function get_chats(query) {
    fetch(`/messaging/open_chats/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            contactList = document.querySelector(".contact-list");
            contactList.innerHTML = "";

            if (!data.results || data.results.length === 0) {
                contactList.innerHTML = "<h3 class='text-muted'>No Results</h3>";
            } else {
                data.results.forEach(contact => {
                    contactList.innerHTML += `
                        <a href="/messaging/${contact.group_name}/" class="contact-item-link">
                            <div class="contact-item">
                                <img src="${contact.profile_url || '/static/images/profile_image.jpg'}" alt="profile image" class="profile_image" />
                                <div class="contact-details">
                                    <div class="contact-name">${contact.name}</div>
                                </div>
                            </div>
                        </a>
                    `;
                });
            }
        })
        .catch(error => {
            console.error("Fetch error:", error);
        });
}