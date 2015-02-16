use Chaos;

my $blog = Chaos->new(username=>"someone", password=>"foobar");
for (19..25) {
if (my $entry = $blog->entry($_)) {
print "Title: ", $entry->title, "\n";
print "Tags: ", join(", ", $entry->tags), "\n";
print "HTML: \n", $entry->html, "\n\n";
} else {
print "none\n"; }
#~ print join("\n", $entry->tags), "\n";
#~ print ($entry->html || "no", "\n");
}