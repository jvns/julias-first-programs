
		 for(int i = 1; i< 30; i++) {
			 int k = (int)java.lang.Math.pow(2,i);
			 String l = "" + k;
        bigInteger a = new bigInteger(l);  
        bigInteger b = new bigInteger(l);
			 long t1 = System.currentTimeMillis();        
        bigInteger product=b.iterativeMultiplication( a );
        long t2 = System.currentTimeMillis();
			 System.out.println(l + " : " + (t2 - t1));
		}
		
		
		
				 long t1 = System.currentTimeMillis();
		 int tries = 1;
		 for(int i = 1; i<= tries; i++) {
			a = bigInteger.getRandom( 8 );  
			b = bigInteger.getRandom( 8 );
			 a.iterativeMultiplication(b);
			 
			}
		 long t2 = System.currentTimeMillis();
			System.out.println(((float)(t2 - t1))/tries);


        /* This is just an example of how to use various things you'll need 
           for question 4. You don't need to keep any of the code below if 
           you don't feel it's necessary. */

	/* since getRandom is a static member of bigInteger,  
	   it can be called using only the name of the class 
	   ( i.e. without an actual object ) */
public class testBigInteger {
    public static void main( String args[] ) {
        bigInteger a = bigInteger.getRandom( 1000 );  
        bigInteger b = bigInteger.getRandom( 1000 );

        long t1 = System.currentTimeMillis();        
        bigInteger product=b.recursiveMultiplication( a );
        long t2 = System.currentTimeMillis();
//        System.out.println( a + " * " + b + " = " + product );
        System.out.println( "Recursive: Total time: " + ( t2-t1 ) );
		 
		  t1 = System.currentTimeMillis();        
        product=b.standardMultiplication( a );
        t2 = System.currentTimeMillis();
//        System.out.println("Standard: \n" +  a + " * " + b + " = " + product );
        System.out.println( "Standard: Total time: " + ( t2-t1 ) );
		  
		  t1 = System.currentTimeMillis();        
        product=b.recursiveFastMultiplication( a );
        t2 = System.currentTimeMillis();
//        System.out.println("Recursive Fast: \n" +  a + " * " + b + " = " + product );
        System.out.println( "Fast: Total time: " + ( t2-t1 ) );
		  
		 a = new bigInteger(args[0]);
		 b = new bigInteger(args[1]);
		 t1 = System.currentTimeMillis();        
        product=b.iterativeMultiplication( a );
        t2 = System.currentTimeMillis();
        System.out.println( a + " * " + b + " = " + product );
        System.out.println( "Total time: " + ( t2-t1 ) );
		  
		  
		 
    }
}                