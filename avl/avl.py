from binarytree import LinkedBinaryTree
from mapbase import MapBase

class TreeMap(LinkedBinaryTree, MapBase): 

  #---------------------------- override Position class ------------
  class Position(LinkedBinaryTree.Position):
    def key(self):
      """Return key of map's key-value pair."""
      return self.element()._key

    def value(self):
      """Return value of map's key-value pair."""
      return self.element()._value 
    

  #------------------------------- nonpublic utilities -----------------
  
  def _subtree_search(self, p, e):
      if e == p.value(): # found match
        return p 
      elif e < p.value(): # search left subtree
        if self.left(p) is not None:
          return self._subtree_search(self.left(p), e) 
      else: # search right subtree
        if self.right(p) is not None:
          return self._subtree_search(self.right(p), e)
      return p
  #--------------------- public methods for (standard) map interface ----
  def __getitem__(self, v):
    """Return value associated with key k (raise KeyError if not found)."""
    if self.is_empty():
      raise KeyError('Key Error: ' + repr(v))
    else:
      p = self._subtree_search(self.root(), v)
      if v != p.value():
        raise KeyError('Key Error: ' + repr(v))
      return p

  def __setitem__(self, k, v):
    """Assign value v to key k, overwriting existing value if present."""
    if self.is_empty():
      leaf = self._add_root(self._Item(k,v)) # from LinkedBinaryTree
    else:
        p = self._subtree_search(self.root(),v)
        item = self._Item(k,v)
        if v < p.value():
          leaf = self._add_left(p, item) # inherited from LinkedBinaryTree
        else:
          leaf = self._add_right(p, item) # inherited from LinkedBinaryTree
    self._rebalance(leaf) # hook for balanced tree subclasses

  def __delitem__(self, k):
    """Remove item associated with key k (raise KeyError if not found)."""
    if not self.is_empty():
      p = self._subtree_search(self.root(), k)
      if k == p.key():
        self.delete(p) # rely on positional version
        return # successful deletion complete
      #self._rebalance_access(p) # hook for balanced treesubclasses
    raise KeyError('Key Error: ' + repr(k))

  def __iter__(self):
      """Generate an iteration of all keys in the map in order."""
      p = self.first()
      while p is not None:
        yield p.key()
        p = self.after(p)

  def balanced(self,p):
    h1 = 0
    h2 = 0
    for i in self.children(p):
      if h1 == 0:
        h1 = self._height2(i)+1
      else:
        h2= self._height2(i)+1
        if (-1 <= (h2- h1 ) <= 1):
          return True
        else:
          return False
  
  def _rebalance(self, p):
    
    while p != None:
        h_antiga = self._height2(p)
        if self.balanced(p) is False:
          self._restructure(self.neto_mais_alto(p))
        if h_antiga == (self._height2(p)+1):
            p = None
        else:
            p = self.parent(p)
    #--------------------- nonpublic methods to support tree balancing ---------

  def _relink(self, parent, child, make_left_child):
    """Relink parent node with child node (we allow child to be None)."""
    if make_left_child: # make it a left child
      parent._left = child
    else: # make it a right child
      parent._right = child
    if child is not None: # make child point to parent
      child._parent = parent

  def _rotate(self, p):
    x = p._node
    y = x._parent # we assume this exists
    z = y._parent # grandparent (possibly None)
    if z is None: 
      self._root = x # x becomes root
      x._parent = None 
    else:
      self._relink(z, x, y == z._left) # x becomes a direct child of z
    # now rotate x and y, including transfer of middle subtree
    if x == y._left:
      self._relink(y, x._right, True) # x._right becomes leftchild of y
      self._relink(x, y, False) # y becomes right child of x
    else:
      self._relink(y, x._left, False) # x._left becomes rightchild of y
      self._relink(x, y, True) # y becomes left child of x

  def _restructure(self, x):
    """Perform trinode restructure of Position x with parent/grandparent."""
    y = self.parent(x)
    z = self.parent(y)
    if (x == self.right(y)) == (y == self.right(z)): # matching alignments
      self._rotate(y) # single rotation (of y)
      return y # y is new subtree root
    else: # opposite alignments
      self._rotate(x) # double rotation (of x) 
      self._rotate(x)
      return x # x is new subtree root
      
      
m = int(input(''))
a = TreeMap()
for i in range(0,m):
  e = int(input(''))
  a.__setitem__(i,e)


for e in a.preorder():
  print(e.value(), end=" ")
print('')
for e in a.inorder():
  print(e.value(), end=" ")
print('')
for e in a.postorder():
  print(e.value(), end=" ")