---
layout: post
title: vim-pygments syntax highlighting
---

Quite some time ago now I was drawn to jekyll as a blogging engine partly
because all the cool kids were, but partly because the authors had been smart
enough to to have gone to another language for their syntax highlighting by
shelling out to pygmentize, because 1) Syntax Highlighting is Tricky and 2)
the unix philosophy of calling another process without caring for the
implementation language of the other tool is still alive in some corners of
the world.

So life was good in the kingdom, and because I really like putting example
code into my posts. Unfortunately one day I came across a fairly hairy yak.

I'd started writing a post about a gotcha in rpm packaging, and so the code
examples were rpm .spec files. pygments doesn't have a lexer for rpm .spec
files.

"No problem," I thought, "surely .spec files are nice and simple to highlight,
I'll just whip up a new lexer for rpms"

Now it might be I picked a really bad place to start for my first lexer, but
it turns out rpm spec files though easy to read, weren't that easy for me to
come up with a parser for. I churned away on it for a couple of days
cargo-culting left and right and then eventually gave up on both the pygments
lexer and the original post that had inspired this diversion.

This all left my brain until very recently when it occurred to me that I could
programatically translate an existing syntax highlighting definition for one
engine to another, and so save myself some effort and maybe add a bunch of
other new lexers to pygments or anywhere else with a syntax highlighting
engine. It kindof worked for Syntax::Highlight::Engine::Kate afterall.

So I figured I'd start with vim as my source of highlighters, there seem to be
many and yet they still manage to stay quite readable, even if writing them is
a little harder.

For an example here's a slightly abbreviated version of dosini.vim, the syntax
formatter for ini files.

{% highlight vim %}
syn case ignore
syn match  dosiniLabel      "^.\{-}="
syn region dosiniHeader     start="^\[" end="\]"
syn match  dosiniComment    "^[;#].*$"

hi def link dosiniHeader    Special
hi def link dosiniComment   Comment
hi def link dosiniLabel     Type
{% endhighlight %}

So after looking at one of these for a while, trying to figure out how to parse it, it came to me fairly suddenly.

Stop trying to reimplement vim, have vim do the work for you.

Armed with this stunningly obvious insight, which you don't get when you're
that close to the trees at times, I started to peel things apart.


vim ships with a wonderful script, 2html.vim. What it does is take the current
syntax highlighted buffer and create a new buffer containing a html
representation of the current buffer.

Joining this with ex mode you can do this:

{% highlight bash %}
echo "syn case ignore" > sample.vim
vim -E -s sample.vim <<-EOF
   :syntax on
   :let html_use_css=1
   :run syntax/2html.vim
   :wq! sample.vim.html
   :quit
EOF
{% endhighlight %}


You get a new file with this html fragment:

{% highlight html %}
<pre>
<span class="Statement">syn</span> <span class="Type">case</span> <span class="Type">ignore</span>
</pre>
{% endhighlight %}


It turns out this is very close to syntax fragments that pygments emits while
in html mode.

{% highlight bash %}
echo "syn case ignore" | pygmentize -f html -l vim
{% endhighlight %}

{% highlight html %}
<div class="highlight"><pre><span class="nb">syn</span> case ignore
</pre></div>
{% endhighlight %}




So as our grand finale let's compare pygments rendering of a perl fragment
with a vim one. First up, pygments.

{% highlight perl %}
sub hello {
    print "Hello from pygmentize\n";
}
{% endhighlight %}

And again, as vim_perl


{% highlight vim_perl %}
sub hello {
    print "Hello from vim\n";
}
{% endhighlight %}


Or to use another hipper example, here's something (at time of writing vim,
but should pygments get a puppet lexer it'll take over next time I regenerate
the blog) syntax highlighting a puppet manifest.

{% highlight puppet %}
class blog {
    entries { ensure => "infrequent" }
}
{% endhighlight %}


Now there's some way to go, the mapping between pygments token classes and the
vim syntax element equivalents isn't 100%.
