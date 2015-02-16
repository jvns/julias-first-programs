#!/usr/bin/perl
use warnings;
use strict;

my $file1 = $ARGV[0];
my $file2 = $ARGV[1];

unless ((-e $file1) and (-e $file2)) {
	print "Usage: generate_expectations.pl distance_matrix_file.txt density_file.txt\n";
	exit;
}

open DISTANCES, $file1;
open DENSITIES, $file2;

my @densities;
while(<DENSITIES>) {
	chomp;
	push @densities, $_;
}
my $i = 0;
while(<DISTANCES>) {
	next if /^$/;
	chomp;
	my @distances = split /\s+/;
	for (@distances) {
		my $expectation = f($_) * $densities[$i] *10000;
		print "$expectation ";
	}
	print "\n";
	$i++;
}

sub f {
	return exp(-1*shift); # f(x) is probability that someone at distance x will come to the clinic
	# this function should actually be provided by the management team 
	# (mostly so that we can blame them for it). I asked Yang for something yesterday.
}
