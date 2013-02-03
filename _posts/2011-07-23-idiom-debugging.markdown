---
layout: post
title: "Idiom of the day: Find the error"
tags:  [ 'idioms', 'debugging' ]
---

Today's idiom of the day is a debugging one.

**Find the first error message.  Read it.**

There are many idioms that come out of debugging, and todays should
seem obvious to you, but experience shows that it's a little subtle.

When a system fails there's a good chance that there'll be more
that one error in the logs, and the later failures may be caused by the early
ones.   Making sure you identify and work on the first error will save you a
great deal of effort.

Once you find that first error message, make sure you understand what it's
telling you.  This will sometimes confound you as some error messages are
downright terrible.  What can help is to understand more about what the process
is intended to do -- if you can put yourself in the narrative of what the
program is doing, you may find it easier to spot which obstacle it's
failing on when it complains "I can't do *that*"

As an example, here's an error message that a puppet run might yeild from a simple
file resource -

{% highlight console %}
Could not retrieve file metadata for puppet:///modules/foo/bar: Permission denied 
{% endhighlight %}

Some users when seeing this error will dig around in the auth.conf to see why
the client node isn't permitted to talk to the master, because 'Permission
denied' means you're not allowed to fetch the metadata, right?  Well no, it's a 
message from the master when it failed to open the file to checksum it, so the entire
metatdata api call failed.

{% highlight console %}
$ ls -al foo/files/bar 
-rw-------  1 root  root    8 23 Jul 14:00 foo/files/bar
{% endhighlight %}

Now there is of course a little bit of domain knowledge you need to in order to
pick up the distinction between a master being unable to read a file, and the client
being denied permission to ask, but by reading the message closely and thinking
about the process you should start to be able to intuit that there's a
difference.

As a bonus point, doubly beware backtraces.  Always make sure that you're starting at the
right end, even if it means checking a few times.

