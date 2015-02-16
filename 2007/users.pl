#!/usr/bin/perl\

while(<>) {
my ($name, @rest) = split(/:/);
print "$name\n";
}
