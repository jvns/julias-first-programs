use Chaos;

my $blog = new Chaos(username=>"someone", password=>"foobar");

my $entry = $blog->edit(text=>"Blah",
				title=>"You Suck",
				tags=>["test", "test2"],
				id=>3,
);

print $entry->title, "\n";
