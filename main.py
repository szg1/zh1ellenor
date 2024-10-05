import os
import random
import shutil
import subprocess
import zipfile

path = input("Path of the zip archive (absolute): ")

_last_print_len = 0
def reprint(msg, finish=False):
    global _last_print_len

    print(" " * _last_print_len, end="\r")

    if finish:
        end = "\n"
        _last_print_len = 0
    else:
        end = "\r"
        _last_print_len = len(msg)

    print(msg, end=end)


if os.path.exists(path):
    reprint("File exists.")
else:
    exit("File does not exist.")
# check if .zip or .rar or .7z
if path.endswith('.zip'):
    reprint("File is a zip archive.")
else:
    exit("File is not a zip archive.")

script_path = os.path.dirname(os.path.realpath(__file__))
# create folder

folder = os.path.join(script_path,"extracted")
shutil.rmtree(folder)
os.makedirs(folder, exist_ok=True)
# unzip file to folder
if path.endswith('.zip'):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(folder)
# elif path.endswith('.rar'):
#     with rarfile.RarFile(path, 'r') as rar_ref:
#         rar_ref.extractall(folder)
# elif path.endswith('.7z'):
#     with py7zr.SevenZipFile(path, mode='r') as seven_zip:
#         seven_zip.extractall(folder)
# check if extracted folder is empty
if not os.listdir(folder):
    exit("Archive is empty.")
else:
    reprint("Archive extracted.")

# folder should contain 1 C# solution folder with 3 csprojs or 3 C# solution folders
# check if folder contains 1 C# solution folder
folders = os.listdir(folder)
# filter for directories
folders = [f for f in folders if os.path.isdir(os.path.join(folder, f))]
onefolder = False
if len(folders) == 1:
    reprint("Folder contains 1 C# solution folder.")
    onefolder = True
elif len(folders) == 3:
    reprint("Folder contains 3 C# solution folders.")
else:
    exit("Folder does not contain 1 or 3 C# solution folders. (Folders found: " + str(len(folders)) + ")")

if not onefolder:
    #find the csproj in each folder
    csproj = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.csproj'):
                csproj.append(file)
    if len(csproj) == 3:
        reprint("Folder contains 3 csprojs.")
    else:
        #check if there are 3 .sln-s
        sln = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith('.sln'):
                    sln.append(file)
        if len(sln) == 3:
            reprint("Folder contains 3 slns.")
        else:
            exit("Folder does not contain 3 csprojs or 3 slns. (csprojs found: " + str(len(csproj)) + ", slns found: " + str(len(sln)) + ")")
else:
    #find the 3 csprojs in the folder
    csproj = []
    for root, dirs, files in os.walk(os.path.join(folder,folders[0])):
        for file in files:
            if file.endswith('.csproj'):
                csproj.append(file)
    if len(csproj) == 3:
        reprint("Folder contains 3 csprojs.")
    else:
        #check if there are 3 .sln-s
        sln = []
        for root, dirs, files in os.walk(os.path.join(folder,folders[0])):
            for file in files:
                if file.endswith('.sln'):
                    sln.append(file)
        if len(sln) == 3:
            reprint("Folder contains 3 slns.")
        else:
            exit("Folder does not contain 3 csprojs or 3 slns. (csprojs found: " + str(len(csproj)) + ", slns found: " + str(len(sln)) + ")")

# compile the csprojs
for i,c in enumerate(csproj):
    cwd = os.path.join(folder, folders[i])
    #supress output, check for errors
    reprint(f"Building {c}...")
    reprint(f"dotnet build {c} in {cwd}")
    res = subprocess.run(["dotnet", "build", c], cwd=cwd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        exit(f"Build failed for {c}.")
    reprint(f"Build successful.")
# find Program.cs in each project
program = []
for i,c in enumerate(csproj):
    cwd = os.path.join(folder, folders[i])
    dirs = os.listdir(cwd)
    for file in dirs:
        if file.endswith(".cs"):# file.endswith('feladat.cs') or file.endswith("Program.cs"):
            program.append(file)
if len(program) == 3:
    reprint("Program.cs found in each project.")
else:
    print(program)
    exit("Program.cs not found in each project.")

# run the programs

def runProgram(cwd, input, name):
    timeout = 10 #seconds
    try:
        res = subprocess.run(["dotnet", "run"], cwd=cwd, input=input.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        return res
    except subprocess.TimeoutExpired:
        return f"{name} timed out."

def testBenzinkut(rundir):
    cwd = os.path.join(folder, rundir)
    print()
    print(cwd)
    print()
    reprint("Testing Benzinkut...")
    # run the program
    # program expects Console.ReadLine() input
    # run the program with input
    # check the output
    # check the exit code
    inputs = [
        "-10",
        "0",
        "94",
        "101",
        "95",
        "0",
        "51",
        "31.13",
        "31,13",
        "talán",
        "",
        "igen",
    ]
    input = '\n'.join(inputs)
    res = runProgram(cwd, input, "benzinkut")
    if isinstance(res, str):
        return res
    if res.returncode != 0:
        return "Benzinkut failed."
    reprint("Beniznkut run successful.")
    reprint("Checking outputs...")
    op = res.stdout.decode('utf-8')
    if (str(round(583*31.13)) not in op):
        print(input)
        print(res.stdout.decode())
        return "Benzinkut output incorrect."
    if (str(31) not in op):
        print(input)
        print(res.stdout.decode())
        return "Benzinkut output incorrect."

    inputs = [
        "95",
        "15",
        "nem"
    ]
    input = '\n'.join(inputs)
    res = runProgram(cwd, input, "benzinkut")
    if isinstance(res, str):
        return res
    if res.returncode != 0:
        print(input)
        print(res.stdout.decode())
        return "Benzinkut failed."
    reprint("Beniznkut run successful.")
    reprint("Checking outputs...")
    op = res.stdout.decode('utf-8')
    if str(round(583 * 15)) not in op:
        print(input)
        print(res.stdout.decode())
        return "Benzinkut output incorrect."
    if str(15) in op:
        print(input)
        print(res.stdout.decode())
        return "Benzinkut output incorrect."

    inputs = [
        "100",
        "15",
        "igen"
    ]
    input = '\n'.join(inputs)
    res = runProgram(cwd, input, "benzinkut")
    if isinstance(res, str):
        return res
    if res.returncode != 0:
        return "Benzinkut failed."
    reprint("Beniznkut run successful.")
    reprint("Checking outputs...")
    op = res.stdout.decode('utf-8')
    if str(round(637*15)) not in op:
        print(input)
        print(res.stdout.decode())
        return "Benzinkut output incorrect."
    if str(15*5) not in op:
        print(input)
        print(res.stdout.decode())
        return "Benzinkut output incorrect."
    return "Benzinkut successful."

def testHorgasz(rundir):
    cwd = os.path.join(folder, rundir)
    print()
    print(cwd)
    print()
    reprint("Testing Horgász...")
    # run the program
    inputs = [
        '14',
        '101',
        '-1',
        '50'
    ]
    input = '\n'.join(inputs)
    res = runProgram(cwd, input, "horgasz")
    if isinstance(res, str):
        return res
    if res.returncode != 0:
        return "Horgász failed."
    return "Horgász successful."

def testNyolcosztas(rundir):
    cwd = os.path.join(folder, rundir)
    print()
    print(cwd)
    print()
    reprint("Testing Nyolcosztás...")
    # run the program
    # random int array

    # remove all elements after the 8th element that is divisible by 5
    c = 0
    randints2 = []
    while True:
        val = random.randint(-100, 100000)
        randints2.append(val)
        if val % 5 == 0:
            c += 1
        if c == 8:
            if len(randints2) > 500:
                break
            else:
                randints2.remove(randints2[-1])
                c-=1
                reprint(f"removing last element, current length: {len(randints2)}")
    inputs = [
        '\n'.join(map(str, randints2))
    ]
    inputs[0] += '\n'
    # print()
    # print(inputs)
    # print()
    # reprint(inputs)
    input = '\n'.join(inputs)
    res = runProgram(cwd, input, "nyolcosztas")
    if isinstance(res, str):
        return res
    if res.returncode != 0:
        return "Nyolcosztás failed."
    # check if amount of numbers divisible by 10 is in stdout
    op = res.stdout.decode()
    m10c = 0 # mod 10 count
    for ri in randints2:
        if ri % 10 == 0:
            m10c+=1
    if str(m10c) not in op:
        print(input)
        print(op)
        return "Nyolcosztás output incorrect."
    maxmod10 = 0
    for i in randints2:
        if i % 10 == 0 and i > maxmod10:
            maxmod10 = i
    if str(maxmod10) not in op:
        print(input)
        print(op)
        return "Nyolcosztás output incorrect"

    return "Nyolcosztás successful."
print()
for i, fol in enumerate(folders):
    print(f"{i}) {fol}")
benzinkut = input("Choose Benzinkut project: (id) ")
bkdir = folders[int(benzinkut)]
horgasz = input("Choose Horgász project: (id) ")
hordir = folders[int(horgasz)]
nyolcosztas = input("Choose Nyolcosztás project: (id) ")
nyoldir = folders[int(nyolcosztas)]
reprint(testBenzinkut(bkdir),True)
reprint(testHorgasz(hordir),True)
reprint(testNyolcosztas(nyoldir),True)
