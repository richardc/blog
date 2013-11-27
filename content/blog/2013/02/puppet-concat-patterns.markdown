---
date: "2013-02-02T00:00:00Z"
tags:
- puppet
- datacat
- concat
title: Puppet concat patterns
---

It's common to want to configure a shared resource from many classes in your
module tree, each class defining it's own configuration parameters that then
merge into a more unified whole.

When the resource you're configuring natively supports a conf.d style
this makes the configuration management job quite simple, you just drop
out a new file from each class that's interested and call it done.

The complexity comes when you have a single file that you need to
manage.  At that point it's time to break out one of the concatenation
options available.

Probably the most widely-used concatenation module is R.I.Pienaar's
excellent [puppet-concat](https://github.com/ripienaar/puppet-concat).

If you're not familiar with it here's a worked example of adding lines
to the /etc/motd file from multiple classes.

{{< highlight puppet >}}
# motd/manifests/init.pp
class motd {
    concat { '/etc/motd': }

    concat::fragment { 'motd_header':
        target  => '/etc/motd',
        content => "Hello ${::fqdn}\n",
        order   => '01',
    }
}
{{< / highlight >}}

{{< highlight puppet >}}
# motd/manifests/line.pp
define motd::line {
    concat::fragment { "motd_${title}":
        target  => '/etc/motd',
        content => "${title}\n",
        order   => '10',
    }
}
{{< / highlight >}}

{{< highlight puppet >}}
# chrome/manifests/init.pp
class chrome {
    motd::line { "this machine has chrome on it": }
}
{{< / highlight >}}


`puppet-concat` is great when your files are line-oriented, but when you
need multiple classes to add things to the same line you need to use
something a little more complex.

The pattern I find myself using for this kind of configuration you could
describe as a 'fragment stitching' pattern. You drop data fragments into
a temporary location, then you run a script that parses those those
fragments and assembles them into your intended configuration file.

Here's a worked example of this for a nagios class that manages the
definition of hostgroups.

{{< highlight puppet >}}
# nagios/manifests/init.pp
class nagios {
    file { '/etc/nagios/build':
        ensure  => directory,
        purge   => true,
        recurse => true,
        notify  => Exec['nagios_assemble_hostgroups'],
    }

    file { '/etc/nagios/build/assemble_hostgroups':
        source => 'puppet:///modules/nagios/assemble_hostgroups',
        mode => '0755',
    }

    exec { 'nagios_assemble_hostgroups',
        command => '/etc/nagios/build/assemble_hostgroups'
    }
}
{{< / highlight >}}

{{< highlight puppet >}}
# nagios/manifests/host.pp
define nagios::host($hostgroup = $title) {
    file { "/etc/nagios/build/__HOST_${::hostname}_${hostgroup}.yml",
        content => "{ 'host': '${::hostname}', 'hostgroup': '${hostgroup}' }\n",
        notify  => Exec['nagios_assemble_hostgroups'],
    }
}
{{< / highlight >}}

{{< highlight ruby >}}
# nagios/files/assemble_hostgroups
#/usr/bin/env ruby
$fragment_dir = '/etc/nagios/build'
$output_file  = '/etc/nagios/objects/hostgroups.cfg'

hostgroups = {}
Dir($fragment_dir).each do |filename|
    next unless filename =~ /\.yml$/
    fragment = YAML.load_file("#{$fragment_dir}/#{filename}")
    hostgroups[fragment['hostgroup']] ||= []
    hostgroups[fragment['hostgroup']] << fragment['hostname']
end

assembled = ""
hostgroups.keys.sort.each do |hostgroup|
        assembled = assembled + "
define hostgroup {
        name    #{hostgroup}
        members #{hostgroups[hostgroup].sort.join(',')}
}"
end

File.open($output_file, "w") { |f| f.write(assembled) }
{{< / highlight >}}

{{< highlight puppet >}}
# ntp/manifests/init.pp
class ntp {
    nagios::host { 'ntp server': }
}
{{< / highlight >}}


This works but the major drawback is that you need to write a new
assembly script each time you use it.  Also there are the intermediate files
and a build directory to worry about.  This can make it a little hard to follow
which isn't the best thing in your modules, even if you do hide the complexity
away with definitions.

Having implemented this stitching pattern enough times I started to
think about the practicality of moving to a more data-oriented model, where the
reassembly step can be a straightforward template evaluation step.  What shook
out is a module called [datacat](https://github.com/richardc/puppet-datacat).

Revisiting the nagios hostgroups pattern, with datacat it would look like this:

{{< highlight puppet >}}
# nagios/manifests/init.pp
class nagios {
    datacat { '/etc/nagios/objects/hostgroups.cfg':
        template => 'nagios/hostgroups.cfg.erb',
    }
}
{{< / highlight >}}

{{< highlight puppet >}}
# nagios/manifests/host.pp
define nagios::host($hostgroup = $title) {
datacat_fragment { "nagios::host[${hostgroup}]":
        target => '/etc/nagios/objects/hostgroups.cfg',
        data => {
            $hostgroup => [ $::hostname ],
        },
    }
}
{{< / highlight >}}

{{< highlight erb >}}
# nagios/templates/hostgroups.cfg.erb
<% @data.keys.sort.each do |hostgroup| %>
define hostgroup {
        name    <%= hostgroup %>
        members <%= @data[hostgroup].sort.join(',') %>
}
<% end %>
{{< / highlight >}}

{{< highlight puppet >}}
# ntp/manifests/init.pp
class ntp {
    nagios::host { 'ntp server': }
}
{{< / highlight >}}


The datacat types should provide a general enough model to allow you
to manage files that you build up with data, and what's exposed in your
manifests is cleaner than the machinery involved in managing multiple
fragment files.

There are still a couple of rough edges to sand away, one of which may
be giving it a more obvious name, but it should be available from the
[forge](http://forge.puppetlabs.com/) in a few days.
