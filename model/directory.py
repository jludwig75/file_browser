import os
import glob
import string

class DirectoryException(Exception):
    def __init__(self, msg):
        self.msg = msg

class Directory:
    def __init__(self, baseDir):
        self.baseDir = baseDir
        if len(self.baseDir) > 1 and self.baseDir[-1] == '/':
            self.baseDir = self.baseDir[-1]
        self.path = ''
    
    def cd(self, path):
        print 'CD to "%s"' % path
        if path[0] == '/':
            newPath = path[1:]
        elif path == '.':
            return
        elif path == '..':
            if len(self.path) > 1:
                parts = self.path.split('/')
                newPath = string.join(parts[:-1], '/')
            else:
                raise DirectoryException('Already at the root directory')
        else:
            if self.path == '':
                newPath = path
            else:
                newPath = string.join([self.path, path], '/')

        print 'Path: "%s"' % newPath
        newAbsPath = string.join([self.baseDir, newPath], '/')
        print 'Absolute Path: "%s"' % newAbsPath
        if not os.path.isdir(newAbsPath):
            raise DirectoryException('Invalid directory path "%s"' % newPath)
        self.path = newPath
        
    def GetAbsPath(self):
        if self.path == '':
            return self.baseDir
        return string.join([self.baseDir, self.path], '/')
    
    def cwd(self):
        return string.join(['', self.path], '/')
    
    def isdir(self, entry):
        if entry == '..' or entry == '.':
            return True
        return os.path.isdir(string.join([self.GetAbsPath(), entry], '/'))
    
    def unlink(self, path):
        fileName = self.GetAbsFilePath(path)
        os.unlink(fileName)

    def rename(self, path, newName):
        oldFileName = self.GetAbsFilePath(path)
        newFileName = self.GetAbsFilePath(newName)
        os.rename(oldFileName, newFileName)

    def GetAbsFilePath(self, entry):
        return string.join([self.GetAbsPath(), entry], '/')
    
    def GetDirEntries(self):
        base = self.GetAbsPath()
        dir = os.path.join(base, '*')
        dirEntries = glob.glob(dir)
        if len(self.path) > 0:
            dirEntries = [base + '\\..'] + dirEntries
        for i in range(len(dirEntries)):
            dirEntries[i] = dirEntries[i][len(base)+1:]
        return dirEntries
