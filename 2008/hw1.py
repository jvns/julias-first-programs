from math import sqrt
import operator
def rosenbrock(x,y):
	return 100*(y - x*x)**2  + (1-x)**2
def gradient(x, y):
	return [400*x * (x*x - y) + 2*(x-1) , 200 * (y-x*x)]
def hessian(x,y):
	return [[1200*x*x - 400*y, -400*x], [-400*x, 200]]
def dot(l1, l2):
	return reduce( operator.add, map( operator.mul, l1, l2))
def mul(a, list):
	return map(lambda x: x*a, list)
def add(l1, l2):
	return map(operator.add, l1, l2)
def Mmulv(M, v):	
	return map(lambda x: dot(v,x), M)

def inverse(l):
	[[a,b], [c,d]] = l
	det = a*d-b*c
	return [[d/(det), -b/(det)], [-c/(det), a/(det)]]

def backtrack(f, fk, pk, xk, grad, p, c, alpha):
#	dir = c*alpha * dot(grad, pk)
	[a,b] = add(xk, mul(alpha, pk))
	if (fk + c*alpha * dot(grad, pk) < f(a,b)):
#		print "f(", xk, " + ", alpha, "*", pk, ")", "<", "f", (a,b), "returning", p, "times alpha"
#		print fk + c*alpha * dot(grad, pk), " < " ,f(a,b)
		return backtrack(f, fk, pk, xk, grad, p, c, alpha*p)
	else:
#		print "f(", xk, " + ", alpha, "*", pk, ")", ">", "f", (a,b), "ok step size"
#		print fk + c*alpha * dot(grad, pk), " > " ,f(a,b)
		print "direction is ", pk
		print "Step length: ", alpha
		return alpha

def descent(f,x,y):
	grad = gradient(x,y)
	print "I am at: ", [x,y]
	print "Gradient is: ", grad
	print "Gradient has size: ", dot(grad, grad)
	if dot(grad, grad) < 0.00001:
		return [x,y] 
	else:
		pk = mul(-1/sqrt(dot(grad, grad)), grad)
		alpha = backtrack(f, f(x,y), pk, [x,y], grad, 0.8, 0.9,1)
		[a,b]=add( [x,y], mul(alpha, pk))
#		print "Moving by: ", alpha, " * ", pk, " = ",  mul(alpha, pk), "from: ", [x,y], [a,b], add([x,y], mul(alpha, pk))
		return descent(f,a,b)

def newton(f,x,y):
	grad = gradient(x,y);
	hess = hessian(x,y); 
	print "I am at: ", [x,y]
	print "Gradient is: ", grad
	print "Gradient has size: ", dot(grad, grad)
	if dot(grad, grad) < 0.00001:
		return [x,y] 
	else:
		pk = mul( -1, Mmulv(inverse(hessian(x,y)), grad))
		alpha = backtrack(f, f(x,y), pk, [x,y], grad, 0.8, 0.9,1)
		[a,b]=add( [x,y], mul(alpha, pk))
		return newton(f, a, b)

print "Steepest descent starting from point (1.2, 1.2): "
descent(rosenbrock, 1.2, 1.2);
print "Steepest descent starting from point (-1.2, 1): "
descent(rosenbrock, -1.2, 1);
print "Newton's method starting from point (1.2, 1.2): "
newton(rosenbrock, 1.2, 1.2);
print "Newton's method starting from point (-1.2, 1): "
newton(rosenbrock, -1.2, 1);
