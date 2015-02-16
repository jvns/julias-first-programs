#!/usr/bin/perl 
use warnings;
use strict;

unless(open DISTANCES, $ARGV[0]) {
	print "\n\nUsage: ./generatedistances [filename of matrix of expectations]\n";
	exit;
}
my $i = 0;
my $str;
while(<DISTANCES>) {
	# Each row i is the expectations of # of people coming to site i from zone j
	$i++;
	my $j = 0;
	chomp;
	my @distances = split/, /;
	for (@distances) {
		$j++;
		print "$i $j $_\n";
	}
}

sub f {
	exp(-1*shift);
}
