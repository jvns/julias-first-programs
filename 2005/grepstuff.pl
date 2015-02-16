#!/usr/bin/perl
use warnings;
my @imgs;
while(<>)
{
/src="(.+?)"/;
s:/pictures::g;
if ($1)
{
push(@imgs,$1) unless -e $1 ;
}
}
print join("\n",@imgs);
