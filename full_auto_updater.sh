
#
# Script to fully automate updating and pull request.
#
# That is, 
#  - Checks out LookML code
#  - Runs updater
#  - if and only if any changes made:
#     - commits
#     - pushes to remote
#     - creates a pull request.
#
# Author: Carl Anderson (carl.anderson@weightwatchers.com)
#
# to run, you will need to set:
# 1) GITHUB_TOKEN
# 2) REMOTE
# 3) source of definitions (in config)

brew install hub

#this is your github access token for hub
GITHUB_TOKEN='xxx'
# alternatively, set GITHUB_USER, GITHUB_PASSWORD 

TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

#######################################
# generate the config
#######################################
REMOTE="https://github.com/someorg/somerepo.git"

GITREPO="auto_gitrepo_${TIMESTAMP}"

cat > auto.config <<- EOM
{    
    "git": {
        "url": "${REMOTE}",
        "folder": "${GITREPO}"
    },

    "use_hub": true,

    "use_basename": true,

    "definitions": {
        "type": "CsvDefinitionsProvider",
        "filename": "definitions.csv"
    }
}
EOM


#######################################
# pull down the LookML to process
#######################################

python run_git_clone.py --config auto.config

cd ${GITREPO}


#######################################
# create a new branch
#######################################

BRANCHNAME="lookml_updater_${TIMESTAMP}"

echo "Creating a new branch ${BRANCHNAME}"

git pull

git checkout -b ${BRANCHNAME}

#git push origin ${BRANCHNAME}



#######################################
# run the updater
#######################################

cd ..

for file in ${GITREPO}/dim_location.view.lkml
do
    echo $file
    python run_updater.py --config auto.config --infile $file --outfile $file
done



#######################################
# push changes to remote and create PR
#######################################

cd ${GITREPO}

if [ -z $(git status --porcelain) ];
then
    echo "No changes were made"
else
    echo "Files were changed!"

    git add *.view.lkml

    git commit -m "modifications for lookml updater run at ${TIMESTAMP}"

    git push --set-upstream origin ${BRANCHNAME}

    hub pull-request -m "modifications for lookml updater run at ${TIMESTAMP}"

    hub push

fi
