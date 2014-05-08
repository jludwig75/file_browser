import FileBrowser

d = FileBrowser.Directory('/dev')

print 'Now in "%s"\n' % d.cwd()

print 'Dir listing:'
print d.GenListing()
print ''

print 'Changing to file_browser dir' 
d.cd('file_browser')
print 'Now in "%s"\n' % d.cwd()

print 'Dir listing:'
print d.GenListing()
print ''

print 'Changing to download dir' 
d.cd('download')
print 'Now in "%s"\n' % d.cwd()

print 'Dir listing:'
print d.GenListing()
print ''

print 'Going up one directory'
d.cd('..')
print 'Now in "%s"\n' % d.cwd()

print 'Dir listing:'
print d.GenListing()
print ''
