use Interblog;

my $blog = new Interblog(username=>"someone", password=>"foobar");

$blog->add(	text=>"entry",
				title=>" sucks",
				tags=>["mytags", "blah"]
				)
