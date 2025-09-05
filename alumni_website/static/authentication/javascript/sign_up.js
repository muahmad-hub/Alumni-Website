document.addEventListener("DOMContentLoaded", function(){
    var checkbox = document.getElementById("isTeacher")
    var graduationYear = document.getElementById("graduation-year")


    checkbox.addEventListener("change", function(){
        isTeacher = checkbox.checked
        if (isTeacher){
            document.querySelector(".student_form").style.display = "none"
            document.querySelector(".teacher_form").style.display = "block"
            graduationYear.removeAttribute("required")
        }
        else{
            document.querySelector(".student_form").style.display = "block"
            document.querySelector(".teacher_form").style.display = "none"  
            graduationYear.setAttribute("required", "required")
        }
    })
})