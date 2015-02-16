import java.io.*;
import java.util.*;

public class expressionEvaluator {

    static String evaluate( String expr ) throws Exception { return eval(expr,false); }
    static String evaluatePriority( String expr ) throws Exception {	return eval(expr,true); }

    /* This method evaluates the given arithmetic expression and returns
     * its Integer value. The method throws an exception if the expression
     * is malformed.
		 * if smart == true, evaluates with normal priority
		 * if smart == false, evaluates with left-to-right priority*/
		static String eval( String expr , boolean smart) throws Exception {
			 Stack tokens = new Stack();
		   StringTokenizer tok = new StringTokenizer( expr , "+-*%()", true );  // get the entire expression
			 while (tok.hasMoreTokens()) {
							 String cur = tok.nextToken();
							 if (cur.equals(")")) { /* if we find the end of a parenthesis group, replace the group
																				 with the value of the expression it contains */
											 Stack nums = new Stack();
											 Stack ops = new Stack();
											 while (tokens.peek().equals("(") == false) {
															 String str = tokens.pop().toString();
															 // sort the tokens into two stacks
															 if (str.equals("*") || str.equals("-") || str.equals("+") || str.equals("%"))
																			 ops.push(str);
															 else
																			 nums.push(str);
											 }
											 tokens.pop(); // take off the "(" too
											 tokens.push(evalSimple(nums,ops,smart)); // push the value of the expression onto the stack
							 }
							 else
											 tokens.push(cur);

			 }
			 Stack nums = new Stack();
			 Stack ops = new Stack();
			 while (tokens.empty() == false) {
							 String str = tokens.pop().toString();
							 if (str.equals("*") || str.equals("-") || str.equals("+") || str.equals("%") || str.equals("/"))
											 ops.push(str);
							 else
											 nums.push(str);
			 }
			 return evalSimple(nums,ops,smart);
    } // end of eval

		/* This method takes two stacks of numbers and operators, and returns a String containing the result,
		 * throwing an exception if the expression is malformed
		 * if smart == true, evaluates with normal priority
		 * if smart == false, evaluates with left-to-right priority*/
		private static String evalSimple (Stack nums, Stack ops, boolean smart) throws Exception {
						int value = Integer.parseInt(nums.pop().toString());
						if (nums.size() != ops.size())
										throw new Exception("Too many or too few operators");
					  if (nums.empty()) // if the expression is just a number, return it
										 return String.valueOf(value);
						while(nums.empty() == false && ops.empty() == false) {
											String op = ops.pop().toString();
											int num = Integer.parseInt(nums.pop().toString());
											if (smart == true) { // only do this is we're evaluating with normal priority
															/* If the next n operations exist and are multiplication or a division, do them first */
															if (op.equals("%") == false) { // but integer division doesn't commute, so always do that first
																			while((ops.empty() == false) && (ops.peek().toString().equals("*") || ops.peek().toString().equals("%"))) {
																							int nextnum = Integer.parseInt(nums.pop().toString());
																							String nextop = ops.pop().toString();
																							num = evalBinary(num, nextop, nextnum);
																			}
															}
											}
											value = evalBinary(value, op, num);
						}
						return String.valueOf(value);
		} // end of evalSimple

		/* returns the result of a simple binary operation, given num1 op num2*/
		private static int evalBinary(int num1, String op, int num2) throws Exception {
							if (op.equals("*"))
											return num1 * num2;
							else if (op.equals("+"))
											return num1 + num2;
							else if (op.equals("%"))
											return num1 / num2;
							else if (op.equals("-"))
											return num1 - num2;
							else
											throw new Exception(op + ": Not a valid operator");
		} // end of evalBinary

    /* This method repeatedly asks the user for an expression and evaluates it.
       The loop stops when the user enters an empty expression */
    public void queryAndEvaluate() throws Exception {
        String line;
        BufferedReader stdin = new BufferedReader(new InputStreamReader( System.in ) );
        System.out.println("Enter an expression");
        line = stdin.readLine();
        while ( line.length() > 0 ) {
            try {
                String value = evaluate( line );
                System.out.println("Fake value = " + value );
								System.out.println("Actual value = " + evaluatePriority( line ));
            }
            catch (Exception e)
            {
                System.out.println("Malformed Expression");
            }
            System.out.println( "Enter an expression" );
            line = stdin.readLine();
        } // end of while loop
    } // end of query and evaluate

    public static void main(String args[]) throws Exception {
         expressionEvaluator e=new expressionEvaluator();
         e.queryAndEvaluate();
     } // end of main

}
