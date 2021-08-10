import collections

class Tree:
  """Abstract base class representing a tree structure."""
  #------------------------------- nested Position class --------------------
  class Position:
      """An abstraction representing the location of a single element within 
      Note that two position instaces may represent the same inherent locatio
      Therefore, users should always rely on syntax 'p == q' rather than 'p i
      equivalence of positions.
      """
      def element(self):
        """Return the element stored at this Position."""
        raise NotImplementedError('must be implemented by subclass')
      
      def __eq__(self, other):
        """Return True if other Position represents the same location."""
        raise NotImplementedError('must be implemented by subclass')
      
      def __ne__(self, other):
        """Return True if other does not represent the same location."""
        return not (self == other) # opposite of __eq__

  # ---------- abstract methods that concrete subclass must support ---------
  def __len__(self):
    """Return the total number of elements in the tree."""
    raise NotImplementedError('must be implemented by subclass')

  def children(self, p):
    """Generate an iteration of Positions representing p's children."""
    raise NotImplementedError('must be implemented by subclass')
  # ---------- concrete methods implemented in this class ----------
  def is_leaf(self, p):
    """Return True if Position p does not have any children."""
    return self.num_children(p) == 0

  def is_empty(self):
    """Return True if the tree is empty."""
    return self.__len__() == 0

  def _height2(self, p): # time is linear in size of subtree
    """Return the height of the subtree rooted at Position p."""
    if self.is_leaf(p):
      return 0
    else:
      return 1 + max(self._height2(c) for c in self.children(p))

  def inorder(self):
    """Generate an inorder iteration of positions in the tree."""
    if not self.is_empty():
      for p in self._subtree_inorder(self.root()):
        yield p

  def _subtree_inorder(self, p):
    """Generate an inorder iteration of positions in subtree rooted at p."""
    if self.left(p) is not None: # if left child exists, traverse 
      for other in self._subtree_inorder(self.left(p)):
        yield other
    yield p # visit p between its subtrees
    if self.right(p) is not None: # if right child exists, traverse
      for other in self._subtree_inorder(self.right(p)):
        yield other
  
  def preorder(self):
    """Generate a preorder iteration of positions in the tree."""
    if not self.is_empty():
      for p in self._subtree_preorder(self.root()): # start recursion
        yield p
  
  def _subtree_preorder(self, p):
    yield p # visit p before its 
    for c in self.children(p): # for each child c
      for other in self._subtree_preorder(c): # do preorder of c
        yield other # yielding each t
  
  def postorder(self):
    if not self.is_empty():
      for p in self._subtree_postorder(self.root()): # start recursion
        yield p
  
  def _subtree_postorder(self, p):
    for c in self.children(p): # for each child c
      for other in self._subtree_postorder(c): # do postorder of c
        yield other # yielding each t
    yield p 