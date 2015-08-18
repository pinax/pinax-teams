from .models import Team


def create_teams(obj, user, access):
    """
    Will create new teams associated with the referenced obj and set the
    resulting relation to the correct attribute.

    The naming convention for team foreign keys is pluralname_team (for
    example, instructors_team).

    This function will take the access dictionary and apply the specified
    access types as follows:

    access = {
        'trainees_team': ('open', 'add someone'),
    }

    Where the key name is the team name and the tuple contains the access
    types for member access and manager access respectively.

    If the foreign key already has a value associated with it, this function
    will NOT create a new team to replace it.
    """
    for field_name, access_types in access.items():
        id_field = '{}_id'.format(field_name)
        # Check that the team is associated with the object via a FK...
        if hasattr(obj, id_field) and getattr(obj, id_field) is None:
            # ...and there is no existing related team.
            # TODO - the team name needs to be able to create a unique
            # slug that's < 50 characters long.
            # TODO - this is just a workaround:
            next_pk = next(iter(instance.pk for instance in obj.__class__.objects.order_by("-pk")), 0) + 1  # this is a thing a beauty. ;-)
            team_name = u'{} for {} {}'.format(
                field_name, obj._meta.model_name, next_pk)
            new_team = Team(
                name=team_name,
                member_access=access_types[0],
                manager_access=access_types[1],
                creator=user)
            new_team.save()
            setattr(obj, field_name, new_team)
    return obj
