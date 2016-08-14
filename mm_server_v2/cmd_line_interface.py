def run(mm, cli1, cli2):
    while(True):
        cmd = input().split(' ')
        if cmd[0] == 'exit':
            break
        
        target, action = cmd
        
        if target == 'mm':
            print(getattr(mm, action)())
        elif target == 'c1':
            print(getattr(cli1, action)())
        elif target == 'c2':
            print(getattr(cli2, action)())
        else:
            print("Invalid Target: {}".format(target))