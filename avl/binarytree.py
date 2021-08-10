from tree import Tree

class LinkedBinaryTree(Tree):
    """Linked representation of a binary tree structure."""

    #-------------------------- nested _Node class --------------------------
    class _Node:
      """Lightweight, nonpublic class for storing a node."""
      __slots__ = '_element', '_parent', '_left', '_right' # streamline memor
      def __init__(self, element, parent=None, left=None, right=None):
        self._element = element
        self._parent = parent
        self._left = left
        self._right = right
       

    #-------------------------- nested Position class -------------------------
    class Position():
      """An abstraction representing the location of a single element."""
      def __init__(self, container, node):
        """Constructor should not be invoked by user."""
        self._container = container
        self._node = node
        

      def element(self):
        """Return the element stored at this Position."""
        return self._node._element

      def __eq__(self, other):
        """Return True if other is a Position representing the same locatio"""
        return type(other) is type(self) and other._node is self._node
    #------------------------------- utility methods ------------------------
    
    def _validate(self, p):
      """Return associated node, if position is valid."""
      if not isinstance(p, self.Position):
        raise TypeError('p must be proper Position type')
      if p._container is not self:
        raise ValueError('p does not belong to this container')
      #if p._node._parent is p._node: # convention for deprecated nodes
        #raise ValueError('p is no longer valid')
      return p._node

    def _make_position(self, node):
      """Return Position instance for given node (or None if no node)."""
      return self.Position(self, node) if node is not None else None

    #-------------------------- binary tree constructor -----------------------
    def __init__(self):
      """Create an initially empty binary tree."""
      self._root = None
      self._size = 0

    #-------------------------- public accessors --------------------------
    def __len__(self):
      """Return the total number of elements in the tree."""
      return self._size
    
    def root(self):
      """Return the root Position of the tree (or None if tree is empty)."""
      return self._make_position(self._root)

    def parent(self, p):
      """Return the Position of p's parent (or None if p is root)."""
      node = self._validate(p)
      return self._make_position(node._parent)

    def left(self, p):
      """Return the Position of p's left child (or None if no left child)."""
      node = self._validate(p)
      return self._make_position(node._left)
    
    def right(self, p):
      """Return the Position of p's right child (or None if no right child)."""
      node = self._validate(p)
      return self._make_position(node._right)

    def children(self, p):
      """Generate an iteration of Positions representing p's children."""
      if self.left(p) is not None:
        yield self.left(p)
      if self.right(p) is not None:
        yield self.right(p)

    def num_children(self, p):
      """Return the number of children of Position p."""
      node = self._validate(p)
      count = 0
      if node._left is not None: # left child exists
        count += 1
      if node._right is not None: # right child exists
        count += 1
      return count


    def netos(self,p):
      filhos = self.children(p)
      for f in filhos:
          yield self.children(f)

    def neto_mais_alto(self,p):
      netos = self.netos(p)
      alto = None
      neto = None
      for f in netos:
        for n in f:
          if alto is None:
            alto = self._height2(n)
            neto = n 
          else:
            if self._height2(n) > alto:
              neto = n 
      return neto


    #-------------------------- nonpublic mutators --------------------------
    def _add_root(self, e):
      """Place element e at the root of an empty tree and return new Position
      Raise ValueError if tree nonempty.
      """
      if self._root is not None:
        raise ValueError('Root exists')
      self._size = 1
      self._root = self._Node(e)
      return self._make_position(self._root)

    def _add_left(self, p, e):
      """Create a new left child for Position p, storing element e.
      Return the Position of new node.
      Raise ValueError if Position p is invalid or p already has a left child
      """
      node = self._validate(p)
      if node._left is not None:
        raise ValueError('Left child exists')
      self._size += 1
      node._left = self._Node(e, node) # node is its parent
      return self._make_position(node._left)

    def _add_right(self, p, e):
      """Create a new right child for Position p, storing element e.
      Return the Position of new node.
      Raise ValueError if Position p is invalid or p already has a right chil
      """
      node = self._validate(p)
      if node._right is not None:
        raise ValueError('Right child exists')
      self._size += 1
      node._right = self._Node(e, node) # node is its parent
      return self._make_position(node._right)