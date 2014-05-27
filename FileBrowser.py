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

def GetZipDir():
    cwd = os.path.realpath('./')
    zipsPath = os.path.join(cwd, 'zips')
    zipsPath = os.path.join(zipsPath, GetUserData().username)
    if not os.path.exists(zipsPath):
        os.mkdir(zipsPath)
    zipsPath = os.path.join(zipsPath, cherrypy.session.id)
    if not os.path.exists(zipsPath):
        os.mkdir(zipsPath)
    return zipsPath

def CreateZipOfDir(path):
    parts = path.split('/')
    zipFileName = parts[-1] + ".zip"
    baseDir = string.join(parts[:-1], '/')
    zipsPath = GetZipDir()
    zipFileName = os.path.join(zipsPath, zipFileName)
    cwd = os.path.realpath('./')
    os.chdir(baseDir)
    try:
        with ZipFile(zipFileName, "w") as zip:
            zipdir(parts[-1], zip)
    finally:
        os.chdir(cwd)
    return zipFileName

class SessionData:
    def __init__(self):
        cherrypy.log('Creating new session data')
        self.user = None
        self.dir = None
        self.files_to_copy = set()
        self.files_to_cut = set()
    
    def AddFilesToCopy(self, files):
        for file in files:
            self.files_to_copy.add(file)
    
    def AddFilesToCut(self, files):
        for file in files:
            self.files_to_cut.add(file)
    
    def ClearFilesToCopy(self):
        self.files_to_copy.clear()
    
    def ClearFilesToCut(self):
        self.files_to_cut.clear()
    
    def SetUserId(self, user_id):
        self.ClearUserId()
        cherrypy.session.get['user_id'] = user_id
        
    def GetUser(self):
        if self.user:
            return self.user;
        if not cherrypy.session.get('user_id'):
            return None
        self.user = User(cherrypy.session.get('user_id'))
        return self.user
    
    def ClearUser(self):
        dir = GetZipDir()
        if os.path.isdir(dir):
            # Remove the session dir.
            os.rmdir(dir)
        cherrypy.session.pop('user_id')
        self.user = None
        self.dir = None
    
    def GetDir(self):
        user = self.GetUser()
        if not user:
            self.dir = None
            return None
        if self.dir:
            return self.dir
        cherrypy.log('Creating new directory object')
        self.dir = Directory(user.home_directory)
        return self.dir

session_data = {}

def GetSessionData():
    session_id = cherrypy.session.id
    cherrypy.log('Retrieving session data for session %s' % session_id)
    if not session_data.has_key(session_id):
        session_data[session_id] = SessionData()
    return session_data[session_id]

def ClearSessionData():
    session_id = cherrypy.session.id
    cherrypy.log('Clearing session data for session %s' % session_id)
    if session_data.has_key(session_id):
        del session_data[session_id]
        
def GetUserData():
    return GetSessionData().GetUser()
        
        
class FileBrowserController(object):
    
    def __init__(self):
        self.view = FileBrowserView(self)
        self.user_data = {}
    
    def GetSessionData(self):
        return GetSessionData()
    
    def GetDir(self):
        return GetSessionData().GetDir()
    
    def GetUser(self):
        return GetSessionData().GetUser()

    def index(self):
        if not self.GetUser():
            raise cherrypy.HTTPRedirect("/login")
        
        return self.view.render_index()
    index.exposed = True
    
    def upload(self, myFile):
        newFileName = self.GetDir().GetAbsFilePath(myFile.filename)
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

    def download_complete(self):
        os.unlink(cherrypy.request.zipFileName)

    def download(self, path):
        if self.GetDir().isdir(path):
            zipFileName = CreateZipOfDir(self.GetDir().GetAbsFilePath(path))
            zipFileName = os.path.realpath(zipFileName)
            cherrypy.request.zipFileName = zipFileName
            cherrypy.request.hooks.attach('on_end_request', self.download_complete)
            return cherrypy.lib.static.serve_download(zipFileName)
        else:
            return cherrypy.lib.static.serve_download(self.GetDir().GetAbsFilePath(path))
    download.exposed = True
    
    def cd_impl(self, path):
        #time.sleep(1.5)
        self.GetDir().cd(path)
    
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
        dir = self.GetDir()
        if dir.isdir(dirEntry):
            dir.rmtree(dirEntry)
        else:
            dir.unlink(dirEntry)

    def delete(self, dirEntry):
        self.delete_impl(dirEntry)
        raise cherrypy.HTTPRedirect("/")
    delete.exposed = True

    def delete_js(self, dirEntry):
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
        self.GetDir().rename(dirEntry, newName)
        return self.view.render_dir_view()
    rename_js.exposed = True
    
    def mkdir_js(self, newName):
        #time.sleep(1.5)
        self.GetDir().mkdir(newName)
        return self.view.render_dir_view()
    mkdir_js.exposed = True
    
    def login(self):
        if GetUserData():
            raise cherrypy.HTTPRedirect("/")
        return self.view.render_login_view()
    login.exposed = True
    
    def signup(self, username, password, email):
        try:
            user = User.create(username, password, email)
            os.mkdir(user.home_directory)
            return "OK"
        except UserException, e:
            return e.message
    signup.exposed = True

    def authenticate(self, username, password):
        try:
            user = User(username)
            if user.authenticate(password):
                cherrypy.session['user_id'] = user.user_id
                return "OK"
        except UserException, e:
            pass
        return "Unknown user name or password"
    authenticate.exposed = True
    
    def logout(self):
        GetSessionData().ClearUser()
        ClearSessionData()
        raise cherrypy.HTTPRedirect("/")
    logout.exposed = True
    
    def select_for_copy_or_cut(self, operation, entries):
        entriesList = entries.split(',')[:-1]
        dir = self.GetDir()
        entriesList = [dir.GetAbsFilePath(x) for x in entriesList]
        session = GetSessionData()
        if operation == "copy":
            session.AddFilesToCopy(entriesList)
            print session.files_to_copy
        elif operation == "cut":
            session.AddFilesToCut(entriesList)
            print session.files_to_cut
        return self.view.render_copy_and_cut();
    select_for_copy_or_cut.exposed = True
    
    def clear_select_for_copy_or_cut(self, operation):
        print 'clear_select_for_copy_or_cut() called.'
        session = GetSessionData()
        if operation == "copy":
            session.ClearFilesToCopy()
        elif operation == "cut":
            session.ClearFilesToCut()
        return self.view.render_copy_and_cut();
    clear_select_for_copy_or_cut.exposed = True

tutconf = os.path.join(os.path.dirname(__file__), 'file_browser.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(FileBrowserController(), config=tutconf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(FileBrowserController(), config=tutconf)