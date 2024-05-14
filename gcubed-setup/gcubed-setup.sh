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

function show_current_commit() {
    echo "${1}$(git --no-optional-locks symbolic-ref --short HEAD 2>/dev/null || git --no-optional-locks rev-parse --short HEAD 2>/dev/null)"
}

while getopts "g:p:s:t:u:v:" flag
do
    case "${flag}" in
        g) sym_repository_tag="${OPTARG}";;
        p) gcubed_prerequisites_repository="${OPTARG}";;
        s) sym_repository="${OPTARG}";;
        t) temp_directory="${OPTARG}";;
        u) user_data_defaults_directory="${OPTARG}";;
        v) user_data_directory="${OPTARG}";;
    esac
done

gcubed_prerequisites_temp_directory="${temp_directory}/$(directory_from_repo_url $gcubed_prerequisites_repository)"
sym_source_temp_directory="${temp_directory}/$(directory_from_repo_url $sym_repository)"
sym_executable_directory="/usr/local/bin/"

echo "*****************************************************************************************"
echo "User info: $(id)"
echo -e "Machine info: $(uname -a)\n"
echo "Current directory: ${PWD}"
echo -e "In codespace: ${CODESPACES}\n"
echo "User data defaults source directory: ${user_data_defaults_directory}"
echo "Temp directory: ${temp_directory}"
echo -e "Sym executable directory: ${sym_executable_directory}\n"
echo -e "User data directory: ${user_data_directory}\n"
echo "Prerequisites repository: ${gcubed_prerequisites_repository}"
echo -e "Prerequisites repo directory: ${gcubed_prerequisites_temp_directory}\n"
echo "Sym repository: ${sym_repository}"
echo "Sym repository TAG: ${sym_repository_tag}"
echo -e "Sym source temporary directory: ${sym_source_temp_directory}\n"
echo -e "*****************************************************************************************\n"

echo "User data directory (${user_data_directory}) listing:"
echo "**********************************************************************************************"
ls -al "${user_data_directory}"
echo "**********************************************************************************************"


# copy default userdata setup & settings in. NOTE: no-clobber
cp -r --no-clobber ${user_data_defaults_directory}/. ${user_data_directory}

# Install gcubed prereqs
echo "Pulling & installing prerequisites"

echo "Updating apt & installing byacc"
# yacc/byacc required by sym 
# doing upfront in case the update affects any python prerequisites?
# I'd prefer to bake byacc & the path changes into the docker image but... macOS... :/
export DEBIAN_FRONTEND=noninteractive
sudo apt-get clean
sudo apt-get update
sudo apt-get -y install byacc

echo "Creating temporary directory ("${temp_directory}")..."
sudo sudo install -d -m 775 -o vscode -g root  "${temp_directory}"
enter_directory "${temp_directory}"

echo "Installing G-Cubed code"
git clone --depth 1 --single-branch "${gcubed_prerequisites_repository}" "${gcubed_prerequisites_temp_directory}"

enter_directory "${gcubed_prerequisites_temp_directory}"
show_current_commit "Pulled gcubed code commit: "

echo "Installing any whl files"
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
echo "Installing any requirements text files"
for F in req*.txt; do
    if [[ ! -f $F ]]; then
        echo "Didn't find any requirement text files, skipping..."
        break; 
    fi
    echo "Installing $F..."
    pip3 install -r "$F"
    rm "$F"
done

echo "Installing sym processor"
enter_directory ".."
# git clone "${sym_repository}" "${sym_source_temp_directory}"
git clone --depth 1 --single-branch --branch "${sym_repository_tag}" "${sym_repository}" "${sym_source_temp_directory}"

enter_directory "${sym_source_temp_directory}/src"
show_current_commit "Pulled sym code commit: "

make
chmod a-w sym
sudo mv sym "${sym_executable_directory}"

enter_directory "${user_data_directory}"

echo "Removing temporary directory: ${temp_directory}"
sudo rm -rf "${temp_directory}"
