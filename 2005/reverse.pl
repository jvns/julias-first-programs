#!/usr/bin/perl
print "Content-type: text/html\n\n";
my $string = $ENV{'QUERY_STRING'};
$string =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("c", hex($1))/ge;
my $reverse = reverse $string;
print $reverse;