# Python Pull Parser
Tiny pull-style xml parsing API in Python

This is a streaming XML parser based on the expat parser. Instead of providing callbacks, you can iterate over elements to visit their child nodes. If the child nodes are elements, you may iterate over them (or ignore them if you are not interested in their contents).

While this might be considered a DOM parser (for a very liberal definition of DOM), the DOM is built as the document is parsed and items are returned. If "forgetful" mode is set, previous parts of the DOM will also be deleted as they are returned, meaning it can be used for large documents while using very little RAM (proportional to the depth of the tree).

I'd like to expand this to allow different styles of accessing the data, but for now iteration is the only supported way, mostly because I'm just making this for a different project and I'm already spending way too much time on it by writing documentation and an example but what's even the point of even publishing it if you don't have those things.

## Element type

 pullparser.Element is the type used to represent XML elements.

 An element can be iterated to access the child nodes. Child nodes are either Element objects or strings representing character data.
 
 Elements will be created by the parser. Users are not expected to create them directly.

### Element attributes

 Element.name: Element name as string.
 
 Element.attrs: Element attributes as dictionary of strings to strings.
 
 Element.items: A list of child items in the element. If "forgetful" is True, this will not include items already returned. If "done" is False, this element has not yet been fully parsed, and some child elements may be missing.
 
 Element.done: True if this element has been fully parsed.
 
 Element.forgetful: If True, iterating over this element will remove items from the items list as they are returned. This defaults to the same value as the PullParser used to create this object. Setting this to True reduces RAM usage, but if it is True then child nodes can be iterated only once and cannot be accessed through the items attribute.

## PullParser type

 The PullParser class represents an XML document being parsed. It is also an Element object that represents the root of the Element tree.
 
 PullParser(infile, forgetful=False): Creates a PullParser for a file-like object 'infile'. Set "forgetful" to True if you are working with a large document and will iterate child nodes of each element one time at most.

## Example

This example reads an Atom feed and prints the item titles and links.

```python
import pullparser
import sys

def handle_entry(entry):
    title = ''
    links = []
    
    for child in entry:
        if isinstance(child, pullparser.Element):
            if child.name == 'title':
                title = ''.join(str(x) for x in child)
            elif child.name == 'link':
                links.append(child.attrs)
    
    print(title)
    
    for link in links:
        print('    ' + repr(link))

def handle_feed(feed):
    for child in feed:
        if isinstance(child, pullparser.Element) and child.name == 'entry':
            handle_entry(child)

root = pullparser.PullParser(sys.stdin, forgetful=True)

for item in root:
    if isinstance(item, pullparser.Element) and item.name == 'feed':
        handle_feed(item)
```

Sample output using [Wikipedia's atom example](https://en.wikipedia.org/wiki/Atom_%28standard%29#Example_of_an_Atom_1.0_feed):

```
Atom-Powered Robots Run Amok
    {u'href': u'http://example.org/2003/12/13/atom03'}
    {u'href': u'http://example.org/2003/12/13/atom03.html', u'type': u'text/html', u'rel': u'alternate'}
    {u'href': u'http://example.org/2003/12/13/atom03/edit', u'rel': u'edit'}
```
