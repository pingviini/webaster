import deform
import base_buildouts
from pyramid.view import view_config


@view_config(context='..models.Webaster', renderer='../templates/main.pt')
def main_view(context, request):
    return {'project': 'Webaster'}
