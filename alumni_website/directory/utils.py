from profiles.models import Profile

def get_directory_filters():
    years = Profile.objects.filter(graduation_year__isnull=False).values("graduation_year").distinct().order_by('-graduation_year')
    universities = Profile.objects.filter(university__isnull=False).values("university").distinct()

    return {
        "years": years,
        "university": universities,
    }

def get_teacher_diretory_filters():
    subjects = Profile.objects.filter(subject__isnull=False).values("subject").distinct()

    return{
        "subjects": subjects,
    }