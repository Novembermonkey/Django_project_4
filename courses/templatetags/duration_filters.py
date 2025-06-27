from django import template

register = template.Library()


@register.filter
def duration_hm(duration):
    if not duration:
        return ""

    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    parts = []
    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")

    return ' '.join(parts) if parts else '0 minutes'

