import os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
class FileTree():
    """docstring for FileTree"""
    def __init__(self):
        #super(FileTree, self).__init__()
        self.html = ""
    def traverse(self,fpath):
        self.html += '<ul>'
        #print(fpath)
        for item in os.listdir(fpath):
            fullpath = os.path.join(fpath, item)
            ext = os.path.splitext(item)
            if os.path.isfile(fullpath) and ext[1]=='.py':
                self.html += '<li data-path="'+fullpath+'" data-jstree=\'{"icon":"glyphicon glyphicon-leaf"}\' data-executable=1>'+item+'</li>'
            elif os.path.isdir(fullpath):
                self.html +=  '<li>%s' % item
            else:
                self.html +=  '<li data-jstree=\'{"icon":"glyphicon glyphicon-leaf"}\' data-executable=0 data-path='+fullpath+'>%s</li>' % item
            if os.path.isdir(fullpath):
                self.traverse(fullpath)
        self.html += '</ul>'
        return self.html
