import colander
import deform
from pyramid.view import view_config
from ..models import BaseBuildout
from repoze.folder import Folder


class BaseBuildoutSchema(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    version = colander.SchemaNode(colander.String())
    url = colander.SchemaNode(colander.String())


@view_config(context='..models.BaseBuildouts', renderer='../templates/basebuildouts.pt')
def basebuildouts(context, request):
    try:
        objects = context.keys()
    except AttributeError:
        objects = None
    add_url = request.resource_url(context, '@@add')
    return {'project': 'Webaster', 'buildouts': objects, 'add_url': add_url}


@view_config(context='..models.BaseBuildouts',
             renderer='../templates/form.pt',
             name='add')
def add(context, request):
    schema = BaseBuildoutSchema()
    form = deform.Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure, e:
            return {'form': e.render()}

        basebuildout = BaseBuildout(
                appstruct[u'title'],
                appstruct[u'version'],
                appstruct[u'url'])
        templates = Folder()
        basebuildout[u'templates'] = templates
        context[appstruct[u'title'].replace(' ','-').lower()] = basebuildout

        import transaction
        transaction.commit()
    return {'form': form.render(),'project': 'Webaster'}

