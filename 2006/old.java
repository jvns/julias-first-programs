import java.io.*;
import java.util.*;
import java.lang.Exception;

public class expressionEvaluator {
    /* This method evaluates the given arithmetic expression and returns
     * its Integer value. The method throws an Exception if the expression
     * is malformed.*/

    static String evaluate( String expr ) throws Exception {
				expr.replaceAll(" ", "");
			 int open, close;
			 open = close = 1;
			 while(close != 0) {
							 open = close = 0;
							 for (int i = 0; i <=expr.length()-1; i++) {
											 if (String.valueOf(expr.charAt(i)).equals("("))
															 open = i;
											 if (String.valueOf(expr.charAt(i)).equals(")")) { 
															 close = i;
															 if (open + 1 >= close) 
																			 throw new Exception("Empty brackets");
															 expr = expr.substring(0, open) + evalSimple(expr.substring(open+1, close ))+ expr.substring(close + 1, expr.length());
															 break;
											 }
							 }
							 
			 }
			 if (open != 0)
							 throw new Exception("Unmatched bracket");
			 String val = evalSimple(expr);
			 if (val.substring(1,2).equals("-"))
							 return val.substring(1,val.length());
			 else
							 return val;
    } // end of evaluate
		private static String evalSimple( String expr ) throws Exception {
						try {
										new Integer(expr); // if expr is just an integer, return it, otherwise continue
										return expr;
						}
						catch(NumberFormatException e) {}
						System.out.println("Evaluating expression: " + expr);
							String delimiters="+-*%()";
							StringTokenizer nums = new StringTokenizer( expr , delimiters , false );    
							StringTokenizer ops = new StringTokenizer ( expr, "0123456789", false );
							if (nums.hasMoreElements() == false ||  ops.hasMoreElements() == false) 
											throw new Exception("Not enough operators or numbers");
							int value = Integer.parseInt(nums.nextToken()); // holds the value so far 
							if (nums.countTokens() != ops.countTokens()) 
											throw new Exception("Wrong amount of operators and/or numbers: "+ nums.countTokens() + " vs " + ops.countTokens());
							while(nums.hasMoreElements() && ops.hasMoreElements()) {
											String op = ops.nextToken();
											if (op.equals("*")) 
															value *= Integer.parseInt(nums.nextToken());
											else if (op.equals("+"))
															value += Integer.parseInt(nums.nextToken());
											else if (op.equals("%"))
															value = value / Integer.parseInt(nums.nextToken());
											else if (op.equals("-"))
															value -= Integer.parseInt(nums.nextToken());
											else
															throw new Exception(op + ": Not a valid operator");
							}
							if (value >= 0)
											return String.valueOf(value);
							else
											return "0-" + String.valueOf(-value);
		}
		


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
                System.out.println("value = " + value );
            }
            catch (Exception e)
            {
                System.out.println(e.toString());
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
