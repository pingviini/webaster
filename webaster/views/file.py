import colander
import deform
from pyramid.view import view_config
from ..models import File


class FileSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    data = colander.SchemaNode(colander.String(),
                               widget=deform.widget.TextAreaWidget(
                                   rows=20,cols=200),
                               description="File content")


@view_config(renderer='../templates/form.pt',
             name='add-file')
def add(context, request):
    schema = FileSchema()
    form = deform.Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure, e:
            return {'form': e.render()}

        context[appstruct[u'name']] = File(appstruct[u'name'],
                                           appstruct[u'data'])

        import transaction
        transaction.commit()
    return {'form': form.render(), 'project': 'Webaster'}


@view_config(context='..models.File',
             renderer='../templates/file.pt')
def view(context, request):
    return {'project': 'Webaster'}

