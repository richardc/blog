---
layout: post
title: Local install roundup
tags:  [ 'python', 'perl', 'ruby' ]
---

There are going to be times when you need to stray outside your packaging
system to get a version of a module. It might be that the version your vendor
ships is too old, or that it's not packaged. One way around is to set up a
local library path tucked away in your home directory, and install modules
there.

While there's a bigger topic on the ways that this can mess you up, here's a
cleaned up page out of my notebook on how to set this up for various
languages.


## Python

[virtualenv](http://pypi.python.org/pypi/virtualenv) creates what feels a
little like a chroot which you can install your libraries into. Getting it
going is very simple:

{% highlight console %}
$ virtualenv .virtualenv
New python executable in .virtualenv/bin/python
Installing setuptools............done.
{% endhighlight %}

and the add that to the start of your `$PATH` by adding something like this to
your `.bashrc`

{% highlight bash %}
export PATH="$HOME/.virtualenv/bin:$PATH"
{% endhighlight %}

And you're good to go.  Installing modules is then as simple as:

{% highlight console %}
$ easy_install Pygments
Searching for Pygments
Reading http://pypi.python.org/simple/Pygments/
Reading http://pygments.org/
Reading http://pygments.pocoo.org/
Best match: Pygments 1.2.2
Downloading http://pypi.python.org/packages/2.5/P/Pygments/Pygments-1.2.2-py2.5.egg#md5=bbb12b2aba148e69923c7143d2af73bd
Processing Pygments-1.2.2-py2.5.egg
creating /home/richardc/.virtualenv/lib/python2.5/site-packages/Pygments-1.2.2-py2.5.egg
Extracting Pygments-1.2.2-py2.5.egg to /home/richardc/.virtualenv/lib/python2.5/site-packages
Adding Pygments 1.2.2 to easy-install.pth file
Installing pygmentize script to /home/richardc/.virtualenv/bin

Installed /home/richardc/.virtualenv/lib/python2.5/site-packages/Pygments-1.2.2-py2.5.egg
Processing dependencies for Pygments
Finished processing dependencies for Pygments
{% endhighlight %}


## Ruby

[gem](http://docs.rubygems.org/) respects a `$GEM_HOME` environment variable,
or will default to populating a `$HOME/.gem` directory tree if you're not
running as root.

To make your gem-installed binaries come first, we're back to adding things to
our `.bashrc`

{% highlight bash %}
export GEM_HOME="$HOME/.gem"
export PATH="$GEM_HOME/ruby/1.8/bin:$PATH"
{% endhighlight %}

then you can just use `gem` like normal:

{% highlight console %}
$ gem install rake
Successfully installed rake-0.8.7
1 gem installed
Installing ri documentation for rake-0.8.7...
Installing RDoc documentation for rake-0.8.7...
{% endhighlight %}

and hey presto, rake.

{% highlight console %}
$ rake --version
rake, version 0.8.7
{% endhighlight %}


## Perl

Perl's [local::lib](http://search.cpan.org/perldoc/local::lib) sets up all the
necessary environment to install CPAN modules into local paths, so again to
our `.bashrc`

{% highlight bash %}
eval $( perl -Mlocal::lib=$HOME/.perl-local )
{% endhighlight %}

And then you can just install things using the CPAN shell as normal.

{% highlight console %}
$ cpan -i Tie::File
[...]
Installing /home/richardc/.perl-local/lib/perl5/Tie/File.pm
Installing /home/richardc/.perl-local/man/man3/Tie::File.3
Writing /home/richardc/.perl-local/lib/perl5/i686-linux/auto/Tie/File/.packlist
Appending installation info to /home/richardc/.perl-local/lib/perl5/i686-linux/perllocal.pod
  MJD/Tie-File-0.96.tar.gz
  /usr/bin/make install  -- OK
{% endhighlight %}


