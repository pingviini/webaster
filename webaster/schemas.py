import colander
import deform
from pyramid.view import view_config


bases = ('jyu-faculty', 'clean')


class Buildout(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    # buildout_base = colander.SchemaNode(colander.String(),
    #                                     widget=deform.widget.RadioChoiceWidget(
    #                                         values=bases))


class Package(colander.MappingSchema):

    title = colander.SchemaNode(colander.String())
    version = colander.SchemaNode(colander.String())


class Packages(colander.SequenceSchema):
    package = Package()


class Schema(colander.MappingSchema):
    buildout = Buildout()


schema = Schema()


@view_config(renderer='templates/form.pt', name='new')
def add_buildout(self):
    schema = Schema()
    form = deform.Form(schema, buttons=('submit',))
    return {'form': form.render()}
