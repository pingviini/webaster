from pyramid.renderers import get_renderer

def add_base_template(event):
    base = get_renderer('templates/base.pt').implementation()
    top_nav = get_renderer('templates/top_nav.pt').implementation()
    event.update({'base': base, 'top_nav': top_nav})
