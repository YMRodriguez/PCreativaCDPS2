
from subprocess import call
import yaml

commands = yaml.load(open("./data/commands.yaml"), Loader = yaml.FullLoader)

def serverQuiz(cm):
    for server in ["s1","s2","s3","s4"]:
        order = cm.get("baseCLIforVM")[0] + server + " -- "
        cmd_line = order + "git clone https://github.com/CORE-UPM/quiz_2021.git"
        call(cmd_line, shell=True)
        if server == "s1":
            cmd_line = order + "bash -c \"sed -i '29d' quiz_2021/app.js;cd quiz_2021;npm install;npm install forever;npm install mysql2;export QUIZ_OPEN_REGISTER=yes;export DATABASE_URL=mysql://quiz:xxxx@20.20.4.31:3306/quiz;npm run-script migrate_env;npm run-script seed_env; ./node_modules/forever/bin/forever start ./bin/www;mount -t glusterfs 20.20.4.21:/nas public/uploads\""
            call(cmd_line, shell=True)
        else:
            cmd_line = order + "bash -c \"sed -i '29d' quiz_2021/app.js;cd quiz_2021;npm install;npm install forever;npm install mysql2;export QUIZ_OPEN_REGISTER=yes;export DATABASE_URL=mysql://quiz:xxxx@20.20.4.31:3306/quiz;./node_modules/forever/bin/forever start ./bin/www;mount -t glusterfs 20.20.4.21:/nas public/uploads\""
            call(cmd_line, shell=True)
serverQuiz(commands)