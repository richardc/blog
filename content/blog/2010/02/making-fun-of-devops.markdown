---
date: "2010-02-23T00:00:00Z"
tags:
- puppet
- cucumber
- devops
title: When making fun of devops backfires
---

In the last couple of weeks I've been playing with
[puppet-dashboard](http://github.com/reductivelabs/puppet-dashboard), and
after deploying it spotted and patched over a few small niggles.

After I sent a couple of fixes upstream I figured that if I was going to
send any more patches I should do it properly and send supporting testcases
too.  Unfortunately (for me) the test suite is in RSpec was just so alien to
me that I stalled.  I mentioned that I'd found it hard to use to
[Dean](http://www.unixdaemon.net/) in passing, to which his comeback was:

{{< highlight ruby >}}

rspec.should be.better :designed?yes

{{< / highlight >}}

Not to be outdone, I tried to out-trendy him, and so my reply was:

{{< highlight cucumber >}}

Feature: Writing haikus
  In order to be as be cool and hip
  As a programmer
  I have to pretend I'm writing haiku
  And call it devops

  Scenario: Writing a haiku
    Given I am a twat
    And I love the sound of my own voice
    When I order coffee
    Then it will have sprinkles and a long fucking name

  Scenario: Taking the piss
    Given I am angry
    And I thought cucumber was silly
    When it comes out quite well
    Then I feel let down

{{< / highlight >}}

And in doing so I think I've accidentally sold myself on playing with
[cucumber-nagios](http://auxesis.github.com/cucumber-nagios/). Whoops.
