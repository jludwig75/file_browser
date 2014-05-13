import os
import time
from zipfile import ZipFile
localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

import cherrypy
from cherrypy.lib.static import serve_file

cherrypy.config.update({'session_filter.on': True})

from model.directory import *
from view.filebrowser import *
from model.user import *

def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

def CreateZipOfDir(path):
    parts = path.split('/')
    zipFileName = parts[-1] + ".zip"
    baseDir = string.join(parts[:-1], '/')
    cwd = os.path.realpath('./')
    zipsPath = os.path.join(cwd, 'zips')
    zipFileName = os.path.join(zipsPath, zipFileName)
    os.chdir(baseDir)
    try:
        with ZipFile(zipFileName, "w") as zip:
            zipdir(parts[-1], zip)
    finally:
        os.chdir(cwd)
    return zipFileName

class FileBrowserController(object):
    
    def __init__(self):
        self.dir = Directory('/datastore')
        self.view = FileBrowserView(self)

    def index(self):
        if not cherrypy.session.get('cwd'):
            cherrypy.session['cwd'] = ''
        dir = cherrypy.session.get('cwd')
        if dir and len(dir) > 0:
            self.dir.cd(dir)
            
        return self.view.render_index()
    index.exposed = True
    
    def upload(self, myFile):
        newFileName = self.dir.GetAbsFilePath(myFile.filename)
        f = open(newFileName, 'wb')

        size = 0
        while True:
            data = myFile.file.read(8192)
            if not data:
                break
            f.write(data)
            size += len(data)

        f.close()
        raise cherrypy.HTTPRedirect("/")
    upload.exposed = True

    def show_upload_js(self):
        return self.view.render_upload()
    show_upload_js.exposed = True

    def download(self, path):
        if self.dir.isdir(path):
            zipFileName = CreateZipOfDir(self.dir.GetAbsFilePath(path))
            return serve_file(os.path.realpath(zipFileName), "application/x-download", "attachment")
        else:
            return serve_file(self.dir.GetAbsFilePath(path), "application/x-download", "attachment")
    download.exposed = True
    
    def cd_impl(self, path):
        #time.sleep(1.5)
        self.dir.cd(path)
    
    def cd(self, path):
        self.cd_impl(path)
        raise cherrypy.HTTPRedirect("/")
    cd.exposed = True
    
    def cd_js(self, path):
        self.cd_impl(path)
        return self.view.render_dir_view()
    cd_js.exposed = True
    
    def delete_impl(self, dirEntry):
        #time.sleep(5)
        if self.dir.isdir(dirEntry):
            self.dir.rmtree(dirEntry)
        else:
            self.dir.unlink(dirEntry)

    def delete(self, dirEntry):
        self.delete_impl(dirEntry)
        raise cherrypy.HTTPRedirect("/")
    delete.exposed = True

    def delete_js(self, dirEntry):
        print 'Deleteing "%s"' % dirEntry
        self.delete_impl(dirEntry)
        return self.view.render_dir_view()
    delete_js.exposed = True
    
    def rename_view_js(self, dirEntry):
        #time.sleep(1.5)
        text = self.view.render_rename_view(dirEntry)
        return str(text)
    rename_view_js.exposed = True
    
    def rename_js(self, dirEntry, newName):
        #time.sleep(1.5)
        self.dir.rename(dirEntry, newName)
        return self.view.render_dir_view()
    rename_js.exposed = True
    
    def mkdir_js(self, newName):
        #time.sleep(1.5)
        self.dir.mkdir(newName)
        return self.view.render_dir_view()
    mkdir_js.exposed = True
    
    def login(self):
        return self.view.render_login_view()
    login.exposed = True
    
    def signup(self, username, password, email):
        try:
            user = User.create(username, password, email)
            return "OK"
        except UserException, e:
            return e.message
    signup.exposed = True


tutconf = os.path.join(os.path.dirname(__file__), 'file_browser.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(FileBrowserController(), config=tutconf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(FileBrowserController(), config=tutconf)