---
format: post
title: Local install roundup
---

So you've decided on option 4, hide safely in your home directory,
use intepreted code, and hope that the gods don't rain on you.

## Python virtualenv

[virtualenv](http://pypi.python.org/pypi/virtualenv) creates what feels
a little like a chroot, which you can install your libraries into.  Getting
it running is very simple:

{{% highlight console %}}
$ cd ~
$ virtualenv .virtualenv
New python executable in new-env/bin/python
Installing setuptools............done.
{{% endhighlight %}}


and the add that to the start of your $PATH and you're away,

{{% highlight console %}}
export PATH="$HOME/.virtualenv/bin:$PATH"
{{% endhighlight %}}

Installing a module is then as simple as:

{{% highlight console %}}
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
{{% endhighlight %}}

from here on out, just change your $PATH to point into new-env/bin and 
just use that python install with Pygments and so on.

## Ruby gems

gem respects a $GEM_HOME environment variable, and will also default to
populating a $HOME/.gem directory tree if you're not running as root.

http://docs.rubygems.org/read/chapter/3#page83

To make your personal gem library binaries come first, we're back to tweaking
$PATH like so

{{% highlight bash %}}
export GEM_HOME="$HOME/.gem"
export PATH="$GEM_HOME/ruby/1.8/bin:$PATH"
{{% endhighlight %}} 

then just use gem like normal:

{{% highlight console %}}
$ gem install rake
Successfully installed rake-0.8.7
1 gem installed
Installing ri documentation for rake-0.8.7...
Installing RDoc documentation for rake-0.8.7...
{{% endhighlight %}}

and hey presto, rake.

{{% highlight console %}}
$ rake --version
rake, version 0.8.7
{{% endhighlight %}}


## Perl local::lib


Oh c'mon.  Be serious.


