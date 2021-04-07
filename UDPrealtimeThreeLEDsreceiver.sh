#!/usr/bin/env bash

ncat -k -l -u -p 21324 --sh-exec "cat|tee boo.txt"   

#ncat -k -l -u -p 8000 --sh-exec "cat > /proc/$$/fd/1"