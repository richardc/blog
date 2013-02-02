---
layout: post
title: "Puppet concat patterns"
---

It's a common pattern when managing systems with puppet to want to build up a
configuration from multiple points in your classes.   When the service you're
configuring natively supports a conf.d style this is quite straightforward, you
just drop files from whereever makes sense, but for a single-file resource you
need to use one of the concatenation patterns available to you with puppet.

## concat

Probably the most widely-used concatenation pattern is to use
R.I.Pienaar's excellent puppet-concat module.

If you're not familiar with it here's a worked example of adding lines
to the /etc/motd file from multiple classes.

    # motd/manifests/init.pp
    class motd {
        concat { '/etc/motd': }

        concat::fragment { 'motd_header':
            target  => '/etc/motd',
            content => "Hello ${::fqdn}\n",
            order   => '01',
        }
    }

    # motd/manifests/line.pp
    define motd::line {
        concat::fragment { "motd_${title}":
            target  => '/etc/motd',
            content => "${title}\n",
            order   => '10',
        }
    }

    # chrome/manifests/init.pp
    class chrome {
        motd::line { "this machine has chrome on it": }
    }

`concat` is great when your files are line-oriented, but when you need multiple
classes to add things to the same line you need to use something a little more
complex.

## fragment stitching pattern

The pattern I find myself using for this kind of configuation you could
call a 'fragment stitching' pattern. You drop data fragments into a temporary
location, then you run a script that parses those parse those fragments
assembles them into your intended configuration file.

Here's a worked example of this for a nagios class that manages the
definition of hostgroups.

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

    # nagios/manifests/host.pp
    define nagios::host($hostgroup = $title) {
        file { "/etc/nagios/build/__HOST_${::hostname}_${hostgroup}.yml",
            content => "{ 'host': '${::hostname}', 'hostgroup': '${hostgroup}' }\n",
            notify  => Exec['nagios_assemble_hostgroups'],
        }
    }

    # nagios/files/assemble_hostgroups
    #/usr/bin/env ruby
    $fragment_dir = '/etc/nagios/build'
    $output_file  = '/etc/nagios/objects/hostgroups.cfg'

    hostgroups = {}
    Dir($fragment_dir).each do |filename|
        next unless filename =~ /\.yml$/
        fragment = YAML.load_file("#{fragment_dir}/#{filename}")
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

    # ntp/manifests/init.pp
    class ntp {
        nagios::host { "ntp server: }
    }

This works but the major drawback is you need to write a new assembly
script each time you use it, also you end up with a bunch of intermediate
files in a build directory to manage.

Also the logic of it can be quite complex to follow.

## introducing datacat

XXX datacat is not the best name, give me a better one

Having implemented the stitching pattern more than enough times I looked
at moving the reassembly step into a template evaluation step.

Revisiting the nagios hostgroups pattern, with datacat it would look like this:

    # nagios/manifests/init.pp
    class nagios {
        datacat { '/etc/nagios/objects/hostgroups.cfg':
            template => 'nagios/hostgroups.cfg.erb',
        }
    }

    # nagios/manifests/host.pp
    define nagios::host($hostgroup = $title) {
        datacat_fragment { "nagios::host[${hostgroup}]":
            data => {
                $hostgroup => [ $::hostname ],
            },
        }
    }

    # nagios/templates/hostgroups.cfg.erb
    <% @data.keys.sort.each do |hostgroup| %>
    define hostgroup {
         name    <%= hostgroup %>
         members <%= @data[hostgroup].sort.join(',') %>
    }
    <% end %>

    # ntp/manifests/init.pp
    class ntp {
        nagios::host { "ntp server: }
    }

Hopefully the datacat types provide a general enough model to allow you
to manage arbritary files you build up with data, and the interface
should be clearer than dropping multiple fragment files.

I have some rough edges to sand away and more testing to do, but datacat should
be available from the forge in a few days.

