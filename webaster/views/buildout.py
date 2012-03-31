import colander
import zipfile
import deform
import urllib2
import tempfile
from StringIO import StringIO
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from ..models import Buildout, File


@colander.deferred
def deferred_choices_widget(node, kw):
    choices = kw.get('choices')
    return deform.widget.SelectWidget(values=choices)


class BuildoutSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    description = colander.SchemaNode(colander.String())
    buildout_base = colander.SchemaNode(
        colander.String(),
        widget=deferred_choices_widget)


@view_config(context='..models.Buildouts',
             renderer='../templates/form.pt',
             name='add')
def add(context, request):
    bases = get_base_buildouts(request)
    schema = BuildoutSchema().bind(choices=bases)
    form = deform.Form(schema, buttons=('submit',))

    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure, e:
            return {'form': e.render()}

        context[appstruct[u'name']] = buildout = Buildout(
                appstruct[u'name'],
                appstruct[u'buildout_base'],
                appstruct[u'description'])

        templates = request.root[u'base_buildouts'][appstruct[u'buildout_base']][u'templates']

        template_ids = [id for id in templates.keys()]

        for template in template_ids:
            print templates[template].data
        buildout['buildout.cfg'] = File(u'buildout.cfg', data="""[buildout]
buildoutname=%s
extends=%s

[instance]
http-port=%s
user=%s%s
""" % (appstruct['name'], 'http://', '8000', 'admin', 'admin'))

        buildout['sources.cfg'] = File(u'sources.cfg', data="""[buildout]
extensions = mr.developer buildout.dumppickedversions
auto-checkout = *
sources = sources

[sources]
""")

        buildout['bootstrap.py'] = File(u'bootstrap.py', data=get_bootstrap())

        import transaction
        transaction.commit()
        return HTTPFound(location = request.resource_url(buildout))
    return {'form': form.render(), 'project':'Webaster'}


@view_config(context='..models.Buildout',
             renderer='../templates/buildout.pt')
def view(context, request):
    files = [id for id in context.keys()]
    return {'project':'Webaster', 'files': files}


def get_base_buildouts(request):
    bases = request.root['base_buildouts'].keys()
    if not bases:
        return [('Error: add base buildouts first','Error'),]
    return [(i,i) for i in bases]


def get_bootstrap():
    handle = urllib2.urlopen('http://svn.zope.org/repos/main/zc.buildout/trunk/bootstrap/bootstrap.py')
    return handle.read()


@view_config(renderer='templates/buildout.cfg.txt')
def buildout_cfg_view(request):
    return {'buildoutname':'world', 'http-port': '8000', 'extends': ['1','2']}


@view_config(context='..models.Buildout', name='zip')
def zip(context, request):
    temp = tempfile.mkdtemp()
    filename = '%s/%s' % (temp,'buildout.zip')
    with zipfile.ZipFile(filename, 'w') as buildout:
        for bfile in context.keys():
            buildout.writestr(bfile.encode('utf-8'), context[bfile].data.encode('utf-8'))

    response = Response()
    zipped_file = open(filename, 'r')
    response.body_file = zipped_file
    response.content_type = 'application/zip'
    response.content_disposition = "attachment; filename=buildout.zip"
    return response

@view_config(context='..models.Buildout', name='zip2')
def zip2(context, request):
    out = StringIO()
    with zipfile.ZipFile(out, 'w') as buildout:
        for bfile in context.keys():
            buildout.writestr(bfile.encode('utf-8'), context[bfile].data.encode('utf-8'))

    out.seek(0)
    response = Response(out.getvalue())
    response.content_type = 'application/zip'
    response.content_disposition = "attachment; filename=buildout.zip"
    return response
