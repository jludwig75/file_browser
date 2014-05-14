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

class UserData:
    def __init__(self, user_id):
        self.user_id = user_id
        self.dir = Directory('/datastore')
        self.cwd = ''
        self.user = None
    
    def GetUser(self):
        if not self.user:
            self.user = User(self.user_id)
        return self.user
        
class FileBrowserController(object):
    
    def __init__(self):
        self.view = FileBrowserView(self)
        self.user_data = {}

    def GetUserData(self):
        user_id = cherrypy.session.get('user_id')
        if not user_id:
            print "No current user ID"
            return None
        print "Current used ID: %s" % user_id
        if not self.user_data.has_key(user_id):
            self.user_data[user_id] = UserData(user_id)
        return self.user_data[user_id]
    
    def ClearUserData(self):
        user_id = cherrypy.session.get('user_id')
        if user_id:
            del self.user_data[user_id]
        
    def index(self):
        user_data = self.GetUserData()
        if not user_data:
            raise cherrypy.HTTPRedirect("/login")
        
        return self.view.render_index()
    index.exposed = True
    
    def upload(self, myFile):
        newFileName = self.GetUserData().dir.GetAbsFilePath(myFile.filename)
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
        if self.GetUserData().dir.isdir(path):
            zipFileName = CreateZipOfDir(self.GetUserData().dir.GetAbsFilePath(path))
            return serve_file(os.path.realpath(zipFileName), "application/x-download", "attachment")
        else:
            return serve_file(self.GetUserData().dir.GetAbsFilePath(path), "application/x-download", "attachment")
    download.exposed = True
    
    def cd_impl(self, path):
        #time.sleep(1.5)
        self.GetUserData().dir.cd(path)
    
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
        if self.GetUserData().dir.isdir(dirEntry):
            self.GetUserData().dir.rmtree(dirEntry)
        else:
            self.GetUserData().dir.unlink(dirEntry)

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
        self.GetUserData().dir.rename(dirEntry, newName)
        return self.view.render_dir_view()
    rename_js.exposed = True
    
    def mkdir_js(self, newName):
        #time.sleep(1.5)
        self.GetUserData().dir.mkdir(newName)
        return self.view.render_dir_view()
    mkdir_js.exposed = True
    
    def login(self):
        user_data = self.GetUserData()
        if user_data:
            raise cherrypy.HTTPRedirect("/")
        return self.view.render_login_view()
    login.exposed = True
    
    def signup(self, username, password, email):
        try:
            user = User.create(username, password, email)
            return "OK"
        except UserException, e:
            return e.message
    signup.exposed = True

    def authenticate(self, username, password):
        try:
            user = User(username)
            if user.authenticate(password):
                self.current_user_id = user.user_id
                cherrypy.session['user_id'] = user.user_id
                return "OK"
        except UserException, e:
            pass
        return "Unknown user name or password"
    authenticate.exposed = True
    
    def logout(self):
        cherrypy.session['user_id'] = None
        self.ClearUserData()
        raise cherrypy.HTTPRedirect("/")
    logout.exposed = True

tutconf = os.path.join(os.path.dirname(__file__), 'file_browser.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(FileBrowserController(), config=tutconf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(FileBrowserController(), config=tutconf)