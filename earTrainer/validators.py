def validate_only_xml(value):
    import os
    from django.core.exceptions import ValidationError
    suffix = os.path.splitext(value.name)[1]
    valid = ['.xml']

    if not suffix in valid:
        raise ValidationError(u'Iba xml subor je povoleny')