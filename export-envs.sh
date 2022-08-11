#!/bin/bash -ex

echo "** Export environments from config.yml. **"

function parse_yaml {
   local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')

   sed -ne "s|^\($s\):|\1|" \
        -e "s|^\($s\)\($w\)$s:$s[\"']\(.*\)[\"']$s\$|\1$fs\2$fs\3|p" \
        -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p"  "$1" |

   awk -F"$fs" '{
      indent = length($1)/2;
      name[indent] = $2;
      for (i in name) {if (i > indent) {delete name[i]}}
      if (length($3) > 0) {
         vn=""
         for (i=0; i<indent; i++) {vn=(vn)(name[i])("")}
         _env=(vn)($2)("=")($3)
         printf("%s\n", _env)
      }
   }'
}

IFS=$'\n'
_envs=$(parse_yaml "$1")
for _env in ${_envs}; do
  # https://github.com/koalaman/shellcheck/wiki/SC2163
  export "${_env?}"
  echo "${_env}"
done
