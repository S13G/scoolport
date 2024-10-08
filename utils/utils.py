from datetime import datetime


def generate_student_matric_no(model_class) -> str:
    """
    Generates a unique matriculation number for a new student based on the current year and month.

    Args:
        :param model_class: The instance of the Student model.

    Returns:
        str: The generated matriculation number.
    """
    now = datetime.now()
    year = now.year
    month = now.month
    prefix = f"{year}{month:02d}"
    last_student = (
        model_class.objects.filter(matric_no__startswith=prefix)
        .order_by("matric_no")
        .last()
    )

    if not last_student or not last_student.id:
        new_id = f"{prefix}000001"
    else:
        last_id = int(last_student.matric_no[len(prefix) :])
        new_id = f"{prefix}{last_id + 1:06d}"

    return new_id
