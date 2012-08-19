#!/bin/sh

curl -o /tmp/gfwlist.tmp http://autoproxy-gfwlist.googlecode.com/svn/trunk/gfwlist.txt

if [ "0"="$?" ]; then
    base64 -D -i /tmp/gfwlist.tmp -o /tmp/gfwlist.decode
    if [ "0"="$?" ]; then
        cat /tmp/gfwlist.decode | grep -Eo '[0-9a-z][0-9a-z]+(\.[a-z]{2,3})(\.[a-z]{2})?(/.*)?$' | grep -Eo '[0-9a-z][0-9a-z]+(\.[a-z]{2,3})+' | sort -u > gfw_domain.lst
        cat gfw_domain.lst | while read domain
        do
            echo $domain
        done
    fi
fi
