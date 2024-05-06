#!/bin/bash

echo "Current directory: ${PWD}"
echo "view at root"
ls -al /
echo "Env"
env

function directory_from_repo_url() {
    _var=${1##*/}
    _var=${_var%.*}
    echo ${_var}
}

function enter_directory() {
    cd "${1}"
    echo "Changed directory from: ${OLDPWD} -> ${PWD}"
}

while getopts "a:d:p:s:t:u:v:" flag
do
    case "${flag}" in
        a) main_account_name="${OPTARG}";;
        d) data_repository_common_name="${OPTARG}";;
        p) prereq_repository="${OPTARG}";;
        s) sym_repository="${OPTARG}";;
        t) temp_directory="${OPTARG}";;
        u) user_data_defaults_directory="${OPTARG}";;
        v) user_data_directory="${OPTARG}";;
    esac
done

main_account_page="${GITHUB_SERVER_URL}/${main_account_name}"
parent_repository="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}"
user_data_repository="${GITHUB_SERVER_URL}/${GITHUB_USER}/${data_repository_common_name}"

prereq_temp_directory="${temp_directory}/$(directory_from_repo_url $prereq_repository)"

sym_source_temp_directory="${temp_directory}/$(directory_from_repo_url $sym_repository)"
sym_executable_directory="/usr/local/bin/"

echo "*****************************************************************************************"
echo "User info: $(id)"
echo -e "Machine info: $(uname -a)\n"
echo "Current directory: ${PWD}"
echo -e "In codespace: ${CODESPACES}\n"
echo "Main account name: ${main_account_name}"
echo "Main account page: ${main_account_page}"
echo "Parent repository: ${parent_repository}"
echo -e "Data repository common name: ${data_repository_common_name}\n"
echo "User data defaults source directory: ${user_data_defaults_directory}"
echo "Temp directory: ${temp_directory}"
echo -e "Sym executable directory: ${sym_executable_directory}\n"
echo -e "User data repository: ${user_data_repository}"
echo -e "User data directory: ${user_data_directory}\n"
echo -e "Prerequisites repository: ${prereq_repository}"
echo -e "Prerequisites repo directory: ${prereq_temp_directory}\n"
echo -e "Sym repository: ${sym_repository}"
echo -e "Sym repo directory: ${sym_source_temp_directory}\n"
echo -e "*****************************************************************************************\n"

echo "User data directory (${user_data_directory}) listing:"
echo "**********************************************************************************************"
ls -al "${user_data_directory}"
echo "**********************************************************************************************"

# First check for availability of user data
enter_directory "${user_data_directory}"
echo "Looking for user data repository at: ${user_data_repository}"

GIT_TERMINAL_PROMPT=0 git ls-remote ${user_data_repository} HEAD
if [ $? -ne 0 ]; then 
    echo "Error - repo not available at ${user_data_repository}"
cat << EOF > "${user_data_directory}/README.md"
# ERROR!

## User data repository not available at ${user_data_repository}!

### Please ensure that you have cloned a copy of the sample data repository

### from ${main_account_page}/${data_repository_common_name}

### to your own github repository at https://github.com/${GITHUB_USER}

### NOTE:   
###       **STOP & DELETE THIS DEVCONTAINER NOW**
###       **CLOSE THIS WINDOW**
###       **REOPEN THE MAIN REPOSITORY AT ${parent_repository}**
###       **PRESS THE \"CODE\" BUTTON, SELECT \"CODESPACES\" TAB
###       **AND DELETE THIS CODESPACE.**
###       **ONLY RE-CREATE THIS CODESPACE ONCE YOUR DATA REPO IS SET UP!**

### Instructions for doing all of this can be found at ${main_account_page}/gcubed-2R-user-documentation#clone-data-repo
EOF
    # vscode will open the README automatically on start
    # exit code 0 so that the container starts & displays the error message
    exit
fi

# Looks like we have local user data, so start setting up...

# Removing directory placeholder if there (which would mean it's an empty directory pulled from master repo)
# so that git can clone into an empty directory.
# We have to do it this way as git doesn't track directories, only files.
# If there are user files there already then git won't clone into that directory.
echo "Cloning data from user repo. Git will refuse to overwrite if there are files already in this directory"
rm "${user_data_directory}/.placeholder_semaphore_for_user_data_do_not_remove" 2> /dev/null
git clone "${user_data_repository}" "${user_data_directory}"

# copy default userdata setup & settings in. NOTE: no-clobber
cp -r --no-clobber ${user_data_defaults_directory}/. ${user_data_directory}

echo "Creating temporary directory ("${temp_directory}")..."
sudo sudo install -d -m 775 -o vscode -g root  "${temp_directory}"

echo "Pulling & installing prerequisites"
enter_directory "${temp_directory}"
git clone "${prereq_repository}" "${prereq_temp_directory}"

enter_directory "${prereq_temp_directory}"

echo "Installing all whl files"
for F in *.whl; do
    if [[ ! -f $F ]]; then
        echo "Didn't find any whl files, skipping..."
        break; 
    fi
    echo "Installing $F..."
    pip3 install "$F"
    rm "$F"
done

# Note - doing this after wheel install
echo "Installing requirements text files"
for F in req*.txt; do
    if [[ ! -f $F ]]; then
        echo "Didn't find any requirement text files, skipping..."
        break; 
    fi
    echo "Installing $F..."
    pip3 install -r "$F"
    rm "$F"
done

# yacc/byacc required by sym 
# I'd prefer to bake byacc & the path changes into the docker image but... macOS... :/
export DEBIAN_FRONTEND=noninteractive
sudo apt-get clean
sudo apt-get update
sudo apt-get -y install byacc

enter_directory ".."
git clone "${sym_repository}" "${sym_source_temp_directory}"

enter_directory "${sym_source_temp_directory}/src"

make
chmod a-w sym
sudo mv sym "${sym_executable_directory}"

enter_directory "${user_data_directory}"

echo "Removing temporary directory: ${temp_directory}"
sudo rm -rf "${temp_directory}"
