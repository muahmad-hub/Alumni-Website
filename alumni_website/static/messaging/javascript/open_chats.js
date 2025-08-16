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
                contactList.innerHTML = "<h3 class='text-muted' style='text-align: center;'>Connect with people through their profile to start chatting</h3>";
            } else {
                data.results.forEach(contact => {
                    const mentorBadge = contact.is_mentor ? '<span class="mentor-badge-sidebar">🎓</span>' : '';
                    const unreadBadge = contact.unread_count > 0 ? 
                        `<span class="unread-badge">${contact.unread_count}</span>` : '';

                    contactList.innerHTML += `
                        <a href="/messaging/${contact.group_name}/" class="contact-item-link">
                            <div class="contact-item ${contact.unread_count > 0 ? 'has-unread' : ''}">
                                <img src="${contact.profile_url || '/static/images/profile_image.jpg'}" alt="profile image" class="profile_image" />
                                <div class="contact-details">
                                    <div class="contact-name">
                                        ${mentorBadge}${contact.name}${unreadBadge}
                                    </div>
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