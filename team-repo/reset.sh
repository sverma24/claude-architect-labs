#!/bin/zsh
# Restore the shop code to its starting state (the lab's git-tracked version).
cd ${0:A:h}
git checkout -- shop && git clean -fdq shop
echo "team-repo reset"
