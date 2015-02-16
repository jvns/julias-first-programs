#!/usr/bin/perl
use Chaos;
chdir "blog";
use strict;
#use warnings;
use CGI qw/:standard/;
open CONF, "conf";
chomp(my ($glob_pass, $database_name, $username, $password) = <CONF>);
close CONF;
my $loc = "http://".$ENV{'HTTP_HOST'}.$ENV{'SCRIPT_NAME'};
my $blog = new Chaos(username=>$username, password=>$password, scriptloc=>$loc, database => $database_name);

print header;
my @path = split(m:/:,path_info);
shift(@path);

my $first = shift(@path);

if ($first eq "tags") {
	my $tag = shift(@path);
	if($tag ne "") {
		my @entries = $blog->entries($tag);
		put ("", "", "None tagged with $tag") unless @entries;
		my $titles;
		foreach my $entry (@entries) {
			my $title = $entry->title;
			my $id = $entry->id;
			$titles.= "<a href=$loc/id/$id>$title</a><br>\n";
		}
		put ($tag, [], $titles);
	} else {
		my $tags;
		foreach ($blog->tags) {
			my $tag = $_;
			$tags.="<a href='$loc/tags/$tag'>$tag</a><br>\n";
		}
		put( "tags", [], $tags);
	}
} 

elsif ($first eq "id") {
	my $id = shift(@path);
	if ($id =~/^\d+$/) {
		my $entry = $blog->entry($id);
		if($entry->title) {
			my @tags = $entry->tags;
			put($entry->title, \@tags, $entry->html);
		} else {
			put("Invalid ID", [], "No entry exists with id $id. Try again?");
		}
	} else {
		my @entries = $blog->entries;
		my $html;
		foreach (@entries) {
			my $id = $_->id;
			my $title = $_->title;
			$html.=qq^$id: <a href="$loc/id/$id">$title</a><br>^
		}
		put ("All entries", [], $html);
			
	}
}

elsif ($first eq "add") {
	if(param('text')) {
		my $password = param('password');
		my $title = param('title');
		my $text = param('text') ;
		my @tags = split(/\s*,\s*/, param('tags'));
		if ($password eq $glob_pass) {
			my $entry = $blog->add(	text=> $text,
					title=> $title,
					tags=> \@tags,
			);
		} else {
			put ("Incorrect password", [], "Password \"$password\" incorrect.");
		}
#		put($title, \@tags, $entry->html);
	} else {
		my $html = file("add.html");
		put("add entry", [], $html);
	}
}

elsif ($first eq "edit") {
	my $id = (shift(@path) || param('id'));
	if($id=~/^\d+$/) {
		unless (param('text')) {
			my $entry = $blog->entry($id);
			my $title = $entry->title;
			my $text = $entry->text;
			my @tags = $entry->tags;
			my $tags = join(", ", @tags);
			my $html = file("edit.html", $title, $tags, $text, $id);
			put("editing $title", \@tags, $html);
		} else {
			my $text = param('text');
			my $password = param('password');
			my $title = param('title');
			my @tags = split(/\s*,\s*/, param('tags'));
			if ($password eq $glob_pass) {
				my $entry = $blog->edit(text=>$text, 
											title=>$title, 
											tags=> \@tags, 
											id=>$id
				);
				put("entry edited: ". $entry->title, \@tags, $entry->html);
			} else {
				put ("Incorrect password", [], "Password $password incorrect.");
			}
		}
	} else {
		put("edit entry?", [], file("add.html"));
	}
}
else {
	my @tags = $blog->tags;
	put("Hello!", \@tags, "Here's a chain of random thought. Welcome.");
}

sub put {
	my ($title, $tag, $content) = @_;
	my $tags;
	foreach(@{$tag}) {
		my $url = "$loc/tags/$_";
#		$tags.="<tr><td class=\"news\" bgcolor=\"#A7AEB8\"><a href='$loc/tags/$_'>$_</a></td></tr>";
#		$tags.="<li><a href='$url'> $_ </a></li>"
#		$tags.=qq^:: <a href="$url">$_</a><br>^
		$tags.="<div class=\"tag\"><a href='$url'> $_ </a></div>";
	}
								
	my $file = "look.html";
	open(FIL, "< $file");
	my $temp = join("\n", <FIL>);
	close FIL;
	$temp =~s/(\$\w+(?:::)?\w*)/"defined $1 ? $1 : ''"/gee;
	print $temp;
}

sub file {
	my $file = shift;
	my ($title, $tags, $text, $id) = @_;
	open (DAT, "< $file") || print "failed";
	my @blah = <DAT>;
	close DAT;
	my $temp = join("\n", @blah);
	$temp =~s/(\$\w+(?:::)?\w*)/"defined $1 ? $1 : ''"/gee;
	return $temp;
}

