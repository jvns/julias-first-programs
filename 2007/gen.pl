#!/usr/bin/perl
use Crypt::SmbHash qw(ntlmgen lmhash nthash);
use Encode;

while(<>) {
	my ($username, $nothing, $uid, $gid, $gecos, $homedir, $shell) = split(/:/);
	$gecos=~/(.+?) \</;
	my $name = $1;
	my $sambauid = 2*$uid+1000;
	my $pass = $username;
	my $lm = lmhash(decode_utf8($pass), $pwenc);
	my $nt = nthash(decode_utf8($pass));

	print qq^
dn: uid=$username,ou=people,dc=sums,dc=math,dc=mcgill,dc=ca
objectClass: top
objectClass: account
objectClass: posixAccount
objectClass: sambaSamAccount
sambaSID: S-1-5-21-672012390-4289083522-773950578-$sambauid
sambaLMPassword: $lm
sambaNTPassword: $nt
displayName: $name
^;
}