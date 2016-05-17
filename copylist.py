#!/usr/bin/python

class Node :
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None
        self.link = None
        pass
    pass

def iterlist(node) :
    while(node) :
        yield node
        node = node.next
    pass

def strlist(list) :
    l = []
    for node in iterlist(list) :
        prev = node.prev.val if node.prev else "nul"
        next = node.next.val if node.next else "nul"
        s = "{0}:\tprev = {1}\tnext = {2}\tlink = {3}".format(node.val, prev, next, node.link.val)
        l.append(s)
    return "\n".join(l)
    pass

def printlist(list) : print(strlist(list))

def makelist(links) :
    nodes = []
    
    # make nodes
    prev = None
    for i, link in enumerate(links) : 
        cur = Node(i)
        cur.link = int(link)
        if prev : prev.next, cur.prev = cur, prev
        prev = cur
        nodes.append(cur)
    
    # set up links
    for n in nodes : n.link = nodes[n.link]

    return nodes[0]
    pass

def copylist(list) :

    # copy nodes, connect original/copied nodes via 'prev' field
    for node in iterlist(list) :
        copy = Node(node.val)
        if node.prev : node.prev.prev.next = copy
        copy.prev, node.prev = node, copy        
        pass
    listcopy = list.prev

    # set up 'link' for copied nodes
    for node in iterlist(list) : node.prev.link = node.link.prev

    # restore 'prev' field
    prev, prevcopy = None, None
    for node in iterlist(list) :
        node.prev.prev = prevcopy
        prevcopy = node.prev
        node.prev = prev
        prev = node

    return listcopy
    pass

def testlist(links) :

    # original list, copied list
    list = makelist(links)
    cl = copylist(list)

    # validate copy
    assert(strlist(list) == strlist(cl))
    for node in iterlist(cl) : 
        assert(not node.prev or node.prev.next == node)
        assert(not node.next or node.next.prev == node)

    # mark values in copied list
    for node in iterlist(cl) : node.val = "{0}*".format(node.val)

    # print
    print("Original list:")
    printlist(list)
    print("Copied list:")
    printlist(cl)
    pass

if __name__ == '__main__': 
    import sys
    testlist(sys.argv[1:])
    pass