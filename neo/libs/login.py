import getpass
import os
from dotenv import load_dotenv
from keystoneauth1.identity import v3
from keystoneauth1 import session, plugin
from keystoneclient.v3 import client

home = os.path.expanduser("~")
auth_url = 'https://keystone.wjv-1.neo.id:443/v3'
user_domain_name='neo.id'

def get_username():
    return input("usename: ")

def get_password():
    return getpass.getpass("password: ")

def check_env():
    return os.path.isfile("{}/.neo.env".format(home))

def create_env_file(username,password,project_id):
    try:
        env_file = open("{}/.neo.env".format(home),"w+")
        env_file.write("OS_USERNAME=%s\n" % username)
        env_file.write("OS_PASSWORD=%s\n" % password)
        env_file.write("OS_AUTH_URL=%s\n" % auth_url)
        env_file.write("OS_PROJECT_ID=%s\n" % project_id) 
        env_file.write("OS_USER_DOMAIN_NAME=%s\n" % user_domain_name)
        env_file.close()
        return True
    except:
        return False

def add_token(token):
    try:
        env_file = open("{}/.neo.env".format(home),"a+")
        env_file.write("OS_TOKEN=%s\n" % token)
        env_file.close()
    except:
        return False

def load_env_file():
    return load_dotenv("{}/.neo.env".format(home), override=True)

def get_project_id(username,password):
        auth = v3.Password(auth_url=auth_url,
                                    username=username,
                                    password=password,
                                    user_domain_name=user_domain_name)
        sess = session.Session(auth=auth)
        keystone = client.Client(session=sess)
        project_list = [t.id for t in keystone.projects.list(user=sess.get_user_id())]
		
        return create_env_file(username,password,project_list[0])

def do_login():
    try:
        if check_env():
            load_env_file()
        else:
            username = get_username()
            password = get_password()
            get_project_id(username,password)
            load_env_file()

        auth = v3.Password(auth_url=os.environ.get("OS_AUTH_URL"),
                                username=os.environ.get("OS_USERNAME"),
                                password=os.environ.get("OS_PASSWORD"),
                                user_domain_name=os.environ.get("OS_USER_DOMAIN_NAME"),
                                project_id=os.environ.get("OS_PROJECT_ID"),
                                reauthenticate=True,
                                include_catalog=True)
        
        sess = session.Session(auth=auth)

        with open("{}/.neo.env".format(home)) as envfile:
            if not 'OS_TOKEN' in envfile.read():
                token = sess.get_token()
                add_token(token)
                load_env_file()
                print("Login Success")
    except Exception as e:
        print(e)
        print("Login Failed")

def  do_logout():
    if check_env():
        with open("{}/.neo.env".format(home)) as envfile:
            os.remove("{}/.neo.env".format(home))    
            print("Logout Success")
