use Chaos;

my $blog = new Chaos(username=>"someone", password=>"foobar");

$blog->add(	text=>"Test Post",
				title=>"This Is A Test",
				tags=>["test", "test2"]
)