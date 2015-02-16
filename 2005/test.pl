use Entry;
use warnings;
my $entry = new Entry;

$entry->title("Hello");
$entry->id("339293");
$entry->tags(1,2,3,4);
print $entry->title;
print $entry->id;
print join("\n", $entry->tags);

my %other = (
	song => "greenday",
	mood => "insane",
);

$entry->other(\%other);

my %hash = ($entry->other);
print keys %hash, "\n";