import sys
import xml.parsers.expat

class Element(object):
    def __init__(self, name, attrs, parser, forgetful):
        self.items = []
        self.done = False
        self.name = name
        self.attrs = attrs
        self._parser = parser
        self.forgetful = forgetful
    
    def __iter__(self):
        i = 0
        while True:
            if i < len(self.items):
                yield self.items[0]
                if self.forgetful:
                    self.items.pop(0)
                else:
                    i += 1
            elif not self.done:
                if not self._parser.feed_data():
                    return
            else:
                break

class PullParser(Element):
    def __init__(self, infile, forgetful=False):
        Element.__init__(self, '<root>', {}, self, forgetful)
        self.xmlparser = xml.parsers.expat.ParserCreate()
        self.xmlparser.StartElementHandler = self._start_element
        self.xmlparser.EndElementHandler = self._end_element
        self.xmlparser.CharacterDataHandler = self._character_data
        self.infile = infile
        self.elements = [self]

    def feed_data(self):
        data = self.infile.read(4096)
        if data:
            self.xmlparser.Parse(data)
            return True
        else:
            self.xmlparser.Parse('', False)
            return False

    def _start_element(self, name, attrs):
        new_element = Element(name, attrs, self, self.forgetful)
        self.elements[-1].items.append(new_element)
        self.elements.append(new_element)
    
    def _end_element(self, name):
        ended_element = self.elements.pop(-1)
        ended_element.done = True
        ended_element._parser = None

    def _character_data(self, data):
        self.elements[-1].items.append(data)

if __name__ == '__main__':
    def print_element(element, level = 0):
        print(' '*level, element.name, element.attrs)
        for child in element:
            if isinstance(child, Element):
                print_element(child, level+2)
            else:
                print(' '*(level+2), repr(child))

    print_element(PullParser(sys.stdin, forgetful = True))

