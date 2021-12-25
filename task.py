import sys #module to read variables from batch script

if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "help"):
    print('Usage :-\n$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list\n$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order\n$ ./task del INDEX            # Delete the incomplete item with the given index\n$ ./task done INDEX           # Mark the incomplete item with the given index as complete\n$ ./task help                 # Show usage\n$ ./task report               # Statistics\n')

elif sys.argv[1] == "ls":
    with open("./task.txt", "r") as file:
        index = 1
        for line in file.readlines():
            print(f'{index}. {" ".join(line.split()[1:])} [{"".join(line.split()[:1])}]')
            index += 1

elif sys.argv[1] == "add":
    prior = int(sys.argv[2])
    task = sys.argv[3] + "\n"
    assert prior >= 0

    with open("./task.txt", "r") as file:
        rep_count = {}
        index = 0
        idx = 0
        contents = file.readlines()
        for lines in contents:
            if int("".join(lines.split()[:1])) in rep_count.keys():
                rep_count[int("".join(lines.split()[:1]))] += 1
            else:
                rep_count[int("".join(lines.split()[:1]))] = 1

        for line in contents:
            if prior == int("".join(line.split()[:1])):
                idx = index + rep_count[prior]
            elif int("".join(line.split()[:1])) > prior:
                idx = index
                break
            else:
                idx = index + 1

            index += 1

    contents.insert(idx, sys.argv[2] + " " + task)

    with open("./task.txt", "w") as file:
        contents = "".join(contents)
        file.write(contents)

    print(f'Added task: "{sys.argv[3]}" with priority {prior}')

elif sys.argv[1] == "del":
    index = int(sys.argv[2])

    with open("./task.txt", "r") as file:
        lines = file.readlines()

    if index > len(lines) or index < 0:
        print(f"Error: item with index {sys.argv[2]} does not exist. Nothing deleted.")
    else:
        with open("./task.txt", "w") as file:
            idx = 1
            for line in lines:
                if idx != index:
                    file.write(line)
                idx += 1

        print(f"Deleted item with index {sys.argv[2]}")

elif sys.argv[1] == "done":
    index = int(sys.argv[2])

    with open("./task.txt", "r") as file:
        lines = file.readlines()

    if index > len(lines) or index < 0:
        print(f"Error: no incomplete item with index {sys.argv[2]} exists.")

    else:
        with open("./task.txt", "w") as file:
            idx = 1
            for line in lines:
                if idx != index:
                    file.write(line)
                else:
                    with open("./completed.txt", "a") as f:
                        f.write(" ".join(line.split()[1:]) + "\n")
                idx += 1

        print(f"Marked item as done.")

elif sys.argv[1] == "report":
    with open("./task.txt", "r") as file:
        indexs = 1
        contents = file.readlines()
        print(f"Pending : {len(contents)}")
        for lines in contents:
            print(f'{indexs}. {" ".join(lines.split()[1:])} [{"".join(lines.split()[:1])}]')
            indexs += 1

    with open("./completed.txt", "r") as f:
        index = 1
        content = f.readlines()
        print(f"Completed : {len(content)}")
        for line in content:
            print(f'{index}. {line.strip()}')
            index += 1