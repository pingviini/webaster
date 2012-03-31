from pyramid.view import view_config


@view_config(context='..models.BaseBuildout',
             renderer='../templates/basebuildout.pt')
def view(context, request):
    files = [id for id in context.keys()]
    buildouts = get_allocated_buildouts(request, context.__name__)
    templates = get_templates(context)
    return {'name': context.title, 'version': context.version,
            'url': context.url, 'project': 'Webaster', 'files': files,
            'buildouts': buildouts, 'templates': templates}


def get_allocated_buildouts(request, id):
    buildouts = request.root[u'buildouts']
    tmp = [id for id in buildouts if buildouts[id].__name__ == id]
    return tmp

def get_templates(context):
    return [id for id in context[u'templates'].keys()]
