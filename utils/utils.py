from datetime import datetime


def generate_student_matric_no(instance) -> str:
    """
        Generates a unique matriculation number for a new student based on the current year and month.

        Args:
            :param instance: The instance of the Student model.

        Returns:
            str: The generated matriculation number.
    """
    now = datetime.now()
    year = now.year
    month = now.month
    prefix = f"{year}{month:02d}"
    last_student = instance.objects.filter(matric_no__startswith=prefix).order_by('matric_no').last()

    if not last_student or not last_student.student_id:
        new_id = f"{prefix}000001"
    else:
        last_id = int(last_student.matric_no[len(prefix):])
        new_id = f"{prefix}{last_id + 1:06d}"

    return new_id
