from pyramid.view import view_config


@view_config(context='..models.Buildouts',
             renderer='../templates/buildouts.pt')
def buildout_view(context, request):
    try:
        objects = context.keys()
    except AttributeError:
        objects = None
    return {'project': 'Webaster', 'buildouts': objects}
