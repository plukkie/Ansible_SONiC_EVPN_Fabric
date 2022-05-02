#!/bin/bash

# COMMENTS on additional cli arguments when executing ./ansible_deploy.sh
# --limit=spine	-> run only on group spine

for arg in "$@"
do
    args=$args" $arg"
done

ansible-playbook -i hosts $args playbook.yaml -vvv
