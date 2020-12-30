from subprocess import call
import yaml

commands = yaml.load(open("../data/commands.yaml"), Loader = yaml.FullLoader)

def serverQuiz():
    for server in ["s1","s2","s3","s4"]:
        order = commands.get("baseCLIforVM")[0] + server + " -- "
        cmd_line = order + "git clone https://github.com/CORE-UPM/quiz_2021.git"
        call(cmd_line, shell=True)
        cmd_line = order + "sed '/app.use(redirectToHTTPS([/localhost:(\d{4})/], [], 301));/d' quiz_2021/app.js"
        call(cmd_line, shell=True)
        cmd_line = order + "cd quiz_2021"
        call(cmd_line, shell=True)
        cmd_line = order + "npm install"
        call(cmd_line, shell=True)
        cmd_line = order + "npm install forever"
        call(cmd_line, shell=True)
        cmd_line = order + "npm install mysql12"
        call(cmd_line, shell=True)
        cmd_line = order + "export QUIZ_OPEN_REGISTER=yes"
        call(cmd_line, shell=True)
        cmd_line = order + "export DATABASE_URL=mysql://quiz:xxxx@20.20.4.31:3306/quiz"
        call(cmd_line, shell=True)
        if server == "s1":
            cmd_line = order + "npm run-script migrate_env"
            call(cmd_line, shell=True)
            cmd_line = order + "npm run-script seed_env"
            call(cmd_line, shell=True)
        cmd_line = order + "./node_modules/forever/bin/forever start ./bin/www"
        call(cmd_line, shell=True)

serverQuiz()