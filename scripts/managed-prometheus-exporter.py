#!/usr/bin/env python
#
# Generates the prometheus-exporter manifests and puts it into a manifests directory

import os
import sys
import subprocess
import shutil
import time

def git(*args):
    return subprocess.check_output(['git'] + list(args))

def clone_repos(dest_dir,repo_array):
    wrdir = os.getcwd()
    os.makedirs(dest_dir)
    os.chdir(dest_dir)
    for i in repo_array:
        #os.system('git clone {}'.format(i))
        git("clone", i)

    os.chdir(wrdir)

#def clone_repos(dest_dir,repo_array):
#    #wrdir = os.getcwd()
#    os.makedirs(dest_dir)
#    #os.chdir(dest_dir)
#    for i in repo_array:
#        #os.system('git clone {}'.format(i))
#        git_cmd = '/usr/bin/git clone {}'.format(i)
#        pr = subprocess.Popen([git_cmd], stdout=subprocess.PIPE, cwd=dest_dir)
#        out, error = pr.communicate()
#        print(out)
#        print(error)
#
#    #os.chdir(wrdir)

def make_prom_repos(make_dirs):    
    for dir in make_dirs:
        subprocess.Popen(["make"], stdout=subprocess.PIPE, cwd=dir)

def getSubDirs(parent_dir):
    filenames = os.listdir(parent_dir)
    dirs = []
    for filename in filenames:
        if os.path.isdir(os.path.join(os.path.abspath(parent_dir), filename)):
            dirs.append(os.path.abspath(parent_dir) +"/" +filename)
    return dirs

def copyToManifest(origins,manifest_dir):
    for origin_dir in origins:
        files = os.listdir(origin_dir + "/deploy")
        sub_folder_name = origin_dir.split("/")[-1]
        dest = manifest_dir +"/"+ sub_folder_name
        os.mkdir(dest)
        for f in files:
            if f.lower().endswith(('.yaml','.yml')):
                shutil.move(origin_dir+ "/deploy/" +f, dest)

def usage():
    print("Usage: %s REPO_ARRAY, BUILD_DIR, MANIFEST_DIR")
    print("REPO_ARRAY should be a \",\" seperated list. EX. a,b,c if using with -p flag, else only takes 1 item")
    print("Use -p flag as first argument for prometheus repos requiring make")
    sys.exit(1)

if __name__ == '__main__':
 
    if (len(sys.argv) != 4) and (len(sys.argv) != 5):
        print(sys.argv, len(sys.argv))
        usage()

    if len(sys.argv) == 4:
        repo_array = [sys.argv[1]]
        rtype = sys.argv[1].split("/")[-1]
        print(rtype)
        rtype = rtype.split(".")[0]
        build_dir = sys.argv[2]
        manifest_dir = sys.argv[3]
        clone_dir = build_dir
        build_dir = build_dir + "/" + rtype
        print(build_dir)

        clone_repos(clone_dir,repo_array)
        time.sleep(2)
        print(build_dir)
        full_repo_dirs = getSubDirs(build_dir)
        copyToManifest(full_repo_dirs,manifest_dir)
        sys.exit(0)
    elif len(sys.argv) == 5:
        print(sys.argv[1])

    if sys.argv[1] != "-p":
        usage()
    else:    
        repo_array = sys.argv[2].split(",")
        build_dir = sys.argv[3]
        manifest_dir = sys.argv[4]
        prom_dir = build_dir + "/prometheus"

        clone_repos(prom_dir,repo_array)
        time.sleep(2)
        full_repo_dirs = getSubDirs(prom_dir)
        make_prom_repos(full_repo_dirs)
        copyToManifest(full_repo_dirs,manifest_dir)
        sys.exit(0)

