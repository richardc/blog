#!/usr/local/bin/perl
use lib qw( /home/richardc/hck/perl-Bryar-DataSource-FlatFile-Dated-Markdown/lib );
use Bryar;
use Bryar::Renderer::TT;
Bryar::Renderer::TT->register_format( html2 => "template2.html", "text/html" );
Bryar->go()
