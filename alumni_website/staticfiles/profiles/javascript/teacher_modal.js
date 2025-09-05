document.addEventListener('DOMContentLoaded', function() {
    const teacherModal = document.getElementById('editTeacherSection')
    if (teacherModal) {
        teacherModal.addEventListener('shown.bs.modal', function () {
            // Ensure focus is set to first input when modal opens
            const firstInput = teacherModal.querySelector('input[type="text"]')
            if (firstInput) {
                firstInput.focus()
            }
        })
    }
})
