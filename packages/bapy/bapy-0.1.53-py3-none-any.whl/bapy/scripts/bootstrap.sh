#!/usr/bin/env bash
export DEBUG="yes"

user="$( whoami )"
kali="$( grep -i kali /etc/*rele* 2>/dev/null )"
path="$( git rev-parse --show-toplevel 2>&1 )"
name="${path##*/}"
debug user kali path name

if [[ "${kali-}" ]]; then
  true
else
  sshconfig
fi

#
#
#path="${PEN}"
#repo=
#if [[ "$( uname -s )" == "Darwin" ]]; then
#  sshconfig
#  rsync -av ~/.ssh "${USER}"@
#else
#
#fi
#sshconfig
#echo "${user}" | sudo -S true
#for user in root "${DEFAULT_KALI_USER}" "{{ ansible_env.SUDO_USER }}"; do
#  home="$( grep "${user}" /etc/passwd | cut -d ':' -f6 )"
#  group="$( grep "${user}" /etc/passwd | cut -d ':' -f4 )"
#  sudo passwd -d "${user}"
#  sudo mkdir -p "${home}/.ssh"
#done
#for file in "{{ ansible_user_dir }}/.ssh/authorized_keys" "
#file="{{ ansible_user_dir }}/.ssh/authorized_keys"
#curl https://github.com/"{{ github_username }}".keys | sudo tee -a "${file}"
#curl https://github.com/"{{ github_nferx_username }}".keys | sudo tee -a "${file}"
#sed 's/^.*" //g' "${file}"
