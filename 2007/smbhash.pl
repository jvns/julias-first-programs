#!/usr/bin/perl
my $pass = $ARGV[0];
use Crypt::SmbHash qw(ntlmgen lmhash nthash);
use Encode;
( $lm, $nt ) = ntlmgen decode('iso-8859-1', $pass);
$lm = lmhash(decode_utf8($pass), $pwenc);
$nt = nthash(decode_utf8($pass));
print "sambaLMPassword: $lm\nsambaNTPassword: $nt\n";
