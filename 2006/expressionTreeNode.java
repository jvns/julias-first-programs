import java.lang.Math.*;
import java.lang.Double;

class expressionTreeNode {
    private Object value;
    private expressionTreeNode leftChild, rightChild, parent;
    
    expressionTreeNode() {
        value = null; 
        leftChild = rightChild = parent = null;
    }
    
    // Constructor
    /* Arguments: String s: Value to be stored in the node
                  expressionTreeNode l, r, p: the left child, right child, and parent of the node to created      
       Returns: the newly created expressionTreeNode               
    */
    expressionTreeNode(String s, expressionTreeNode l, expressionTreeNode r, expressionTreeNode p) {
        value = s; 
        leftChild = l; 
        rightChild = r;
        parent = p;
    }
    
    /* Basic access methods */
    Object getValue() { return value; }

    expressionTreeNode getLeftChild() { return leftChild; }

    expressionTreeNode getRightChild() { return rightChild; }

    expressionTreeNode getParent() { return parent; }


    /* Basic setting methods */ 
    void setValue(Object o) { value = o; }
    
    // sets the left child of this node to n
    void setLeftChild(expressionTreeNode n) { 
        leftChild = n; 
        n.parent = this; 
    }
    
    // sets the right child of this node to n
    void setRightChild(expressionTreeNode n) { 
        rightChild = n; 
        n.parent=this; 
    }
    

    // Returns the root of the tree describing the expression s
    // Watch out: it makes no validity checks whatsoever!
    expressionTreeNode(String s) {
        // check if s contains parentheses. If it doesn't, then it's a leaf
        if (s.indexOf("(")==-1) setValue(s);
        else {  // it's not a leaf

            /* break the string into three parts: the operator, the left operand,
               and the right operand. ***/
            setValue( s.substring( 0 , s.indexOf( "(" ) ) );
            // delimit the left operand
            int left = s.indexOf("(")+1;
            int i = left;
            int parCount = 0;
            // find the comma separating the two operands
            while (parCount>=0 && !(s.charAt(i)==',' && parCount==0)) {
                if ( s.charAt(i) == '(' ) parCount++;
                if ( s.charAt(i) == ')' ) parCount--;
                i++;
            }
            int mid=i;
            if (parCount<0) mid--;

        // recursively build the left subtree
            setLeftChild(new expressionTreeNode(s.substring(left,mid)));
    
            if (parCount==0) {
                // it is a binary operator
                // find the end of the second operand
                while ( ! (s.charAt(i) == ')' && parCount == 0 ) )  {
                    if ( s.charAt(i) == '(' ) parCount++;
                    if ( s.charAt(i) == ')' ) parCount--;
                    i++;
                }
                int right=i;
                setRightChild( new expressionTreeNode( s.substring( mid + 1, right)));
        }
    }
    }


    // Returns a copy of the subtree rooted at this node.
    expressionTreeNode deepCopy() {
        expressionTreeNode n = new expressionTreeNode();
        n.setValue( getValue() );
        if ( getLeftChild()!=null ) n.setLeftChild( getLeftChild().deepCopy() );
        if ( getRightChild()!=null ) n.setRightChild( getRightChild().deepCopy() );
        return n;
    }
    
    // Returns a String describing the subtree rooted at a certain node
    public String toString() {
        String ret = (String) value;
        if ( getLeftChild() == null ) return ret;
        else ret = ret + "(" + getLeftChild().toString();
        if ( getRightChild() == null ) return ret + ")";
        else ret = ret + "," + getRightChild().toString();
        ret = ret + ")";
        return ret;
    } 


    // Returns the value of the the expression rooted at a given node
    // when x has a certain value
    double evaluate(double x) {
		expressionTreeNode left = getLeftChild();
		expressionTreeNode right = getRightChild();
		if (left == null && right == null) {
			  if (value.toString().equals("x"))
				    return x;
			  else
				    return new Double(value.toString());
		}
		String op = value.toString();
		if (op.equals("add"))
			  return left.evaluate(x) + right.evaluate(x);
		else if (op.equals("mult"))
			  return left.evaluate(x) * right.evaluate(x);
		else if (op.equals("minus"))
			  return left.evaluate(x) - right.evaluate(x);
		else if (op.equals("cos"))
			  return java.lang.Math.cos(left.evaluate(x));
		else if (op.equals("sin"))
			  return java.lang.Math.sin(left.evaluate(x));
		else if (op.equals("exp"))
			  return java.lang.Math.exp(left.evaluate(x));
		else 
			  System.out.println("Invalid operator in eval(): " + op);
		return 0;
    }                         

    /* returns the root of a new expression tree representing the derivative of the
    expression represented by the tree rooted at the node on which it is called ***/
    expressionTreeNode differentiate() {
		expressionTreeNode left = getLeftChild();
		expressionTreeNode right = getRightChild();
		if (left == null && right == null) {
			  if (value.toString().equals("x"))
				    return new expressionTreeNode("1");
			  else
				    return new expressionTreeNode("0");
		}
		String op = value.toString();
		if (op.equals("add"))
			  return new expressionTreeNode("add", left.differentiate(), right.differentiate(), null);
		else if (op.equals("mult")) {
			  expressionTreeNode prod = new expressionTreeNode("add", null, null, null);
			  prod.setLeftChild(new expressionTreeNode("mult", right.differentiate(), left, null));
			  prod.setRightChild(new expressionTreeNode("mult", left.differentiate(), right, null));
			  return prod;
		}
		else if (op.equals("minus"))
			  return new expressionTreeNode("minus", left.differentiate(), right.differentiate(), null);
		else if (op.equals("cos")) {
			  expressionTreeNode copy = deepCopy();
			  copy.setValue("sin");
			  expressionTreeNode prod = new expressionTreeNode("mult", left.differentiate(), null, null);
			  prod.setRightChild(new expressionTreeNode("minus", new expressionTreeNode("0"), copy,null)); 
			  return prod;
		}
		else if (op.equals("sin")) {
			  expressionTreeNode copy = deepCopy();
			  copy.setValue("cos");
			  expressionTreeNode prod = new expressionTreeNode("mult", left.differentiate(), null, null);
			  prod.setRightChild(copy);
			  return prod;
		}
		else if (op.equals("exp")) {
			  expressionTreeNode copy = deepCopy();
			  expressionTreeNode prod = new expressionTreeNode("mult", left.differentiate(), null, null);
			  prod.setRightChild(copy);
			  return prod;
		}
		else 
			  System.out.println("Invalid operator in diff(): " + op);
		return new expressionTreeNode("0");
    } // end of differentiate()

    expressionTreeNode simplify() {
		String val = value.toString();
		// base case: 
		if (getRightChild() == null && getLeftChild() == null)
			return this;
		if (getRightChild() != null) {
		// clears up all the 0*, 1*, and 0+
			  expressionTreeNode right = getRightChild().simplify();
			  String rval = right.getValue().toString();
			  expressionTreeNode  left = getLeftChild().simplify();
			  String lval = left.getValue().toString();
		// evaluates binary numerical expressions
			  if (isNum((right.getValue().toString()))  && isNum(left.getValue().toString())) {
				    Double result = evaluate(1);
				    return new expressionTreeNode(result.toString());
			  }
			  String op = value.toString();
				    
			  
			  if (op.equals("add")) {
				    if (rval.equals("0") || rval.equals("0.0"))
						return left; 
				    if (lval.equals("0")|| lval.equals("0.0"))
						return right;
			  }
			  if (op.equals("mult")) {
//System.out.println("hey, i'm mult! for .." + right + " and " + left);
				    if (rval.equals("0") || rval.equals("0.0"))
						return new expressionTreeNode("0");
				    if (lval.equals("0")|| lval.equals("0.0"))
						return new expressionTreeNode("0");
				    if (rval.equals("1") || rval.equals("1.0"))
						return left;
				    if (lval.equals("1")|| lval.equals("1.0"))
						return right;
				    
			  }
			return new expressionTreeNode(getValue().toString(), left, right, null);
		}

		else {
		// evaluates other expressions
			expressionTreeNode  left = getLeftChild().simplify();
			if (isNum(left.getValue().toString())) {
				    Double result = evaluate(1);
				    return new expressionTreeNode(result.toString());
			}
			return new expressionTreeNode(getValue().toString(), left, null, null);
		}
    }
    

    private boolean isNum(String s) {
		try {
			  double k = new Double(s);
			  return true;
		}
		catch (NumberFormatException e) {
			  return false;
		}
			  
    }			  
    
    public static void main(String args[]) {
        expressionTreeNode e = new expressionTreeNode("mult(exp(mult(x,2)),x)");
        System.out.println(e);
        System.out.println(e.evaluate(1));
        System.out.println(" Diff: "+ e.differentiate());
        System.out.println("Simplified: " + e.differentiate().simplify());
    }

}
