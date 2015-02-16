#!/usr/bin/perl
use GD;
use strict;
use warnings;
use CGI qw/:standard/;
my %songdat;
song();
my $string = &randstring;

my $browser = $ENV{'HTTP_USER_AGENT'};
if ($songdat{'is_playing'} eq "true") {
	my $song = $songdat{'playlist_title'};
	my $length = length (length($string) > length("music: $song") ? $string: "music: $song") * 6;
	my $im = new GD::Image($length + 2, 40);
	my $white = $im->colorAllocate(255,255,255);
	my $black = $im->colorAllocate(0,0,0);
	# make the background transparent and interlaced
	$im->transparent($white);
	$im->interlaced('true');
	$im->string(gdSmallFont, 2, 2, $string, $black);
	$im->string(gdSmallFont, 2, 22, "music: $song" , $black);
	print "Content-type: image/png\n\n";
	binmode STDOUT;
	print $im->png;
} else {
	my $length = length($string) * 6;
	my $im = new GD::Image($length + 2, 20);
	my $white = $im->colorAllocate(255,255,255);
	my $black = $im->colorAllocate(0,0,0);
	# make the background transparent and interlaced
	$im->transparent($white);
	$im->interlaced('true');$im->string(gdSmallFont, 2, 2, $string, $black);
	print "Content-type: image/png\n\n";
	binmode STDOUT;
	print $im->png;
}

	 
sub randstring {
	my $file = "sigs";
	open(DAT, "< $file");
	chomp(my @array  = <DAT>);
	my $rand = rand(@array);
	$array[$rand];
}

sub song {
	my $file = "nowplaying";
	open (DAT, "< $file");
	while(<DAT>) {
		chomp;
		next unless /=/;
		my ($key, $val) = split/=/;
		$songdat{$key} = $val;
	}
}