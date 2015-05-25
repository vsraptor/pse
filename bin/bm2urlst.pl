#!/usr/bin/env perl
use strict;
use Data::Dumper;
use Mojo::DOM;
$Data::Dumper::Sortkeys = 1;

my $bkmark = $ARGV[0];
my $grep_str = $ARGV[1];
unless ($bkmark) { print "Please specify bookmark file\n"; exit};
unless (-e $bkmark) { print "The Bookmark you specified does not exist\n"; exit};

undef $/;
open my $fh, "<$bkmark" or die print $!;
my $str = <$fh>;
close $fh;

open my $fh, ">url.lst" or die print "cant create url.lst : $!";
my $dom = new Mojo::DOM($str);
for my $el ( $dom->find('a')->each ) {;#->map(attr => 'HREF')->join("\n");
	print $el->{href} . ' : ' . $el->text . "\n";
	print $fh $el->{href} . "\n" if $el->{href} =~ /^http/;
}
close $fh;
