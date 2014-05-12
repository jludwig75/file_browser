import string
from operator import attrgetter

from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])

class FileBrowserView(object):
    def __init__(self, controller):
        self.controller = controller
        self.dir = controller.dir

    def render_index(self):
        tmpl = lookup.get_template("index.html")
        return tmpl.render(view=self, path=self.render_path())

    def render_path(self):
        html = ''
        parts = self.dir.path.split('/')
        if len(self.dir.path) > 0 and len(parts) > 0:
            html += '<a href="cd?path=/" onclick=\'onClickDirEntry("/");return false\'>[root]</a>'
        else:
            html += '[root]'
        for i in range(len(parts) - 1):
            html += '/'
            linkStr = string.join(parts[0:i+1], '/')
            html += '<a href="cd?path=/%s" onclick=\'onClickDirEntry("/%s");return false\'>' % (linkStr, linkStr) 
            html += parts[i]
            html += '</a>'
        html += '/' + parts[-1]
        return html
    
    def render_dir_listing(self):
        tmpl = lookup.get_template("dir_listing.html")
        dirEntries = self.dir.GetDirEntries()
        dirEntries = sorted(dirEntries, key=attrgetter('isfile', 'entryName'))
        return tmpl.render(view=self, entries=dirEntries)
        
    def render_dir_view(self):
        tmpl = lookup.get_template("dir_view.html")
        return tmpl.render(view=self)
    
    def render_dir_entry(self, dirEntry):
        tmpl = lookup.get_template("dir_entry.html")
        return tmpl.render(dirEntry=dirEntry)
    
    def render_rename_view(self, dirEntry):
        tmpl = lookup.get_template("rename_view.html")
        return tmpl.render(dirEntry=dirEntry)

