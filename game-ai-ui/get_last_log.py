import os

def get_last_log(user, lines=20):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    log_file = script_dir + '/user_agents/' + user + '/agent_log'

    try:
        f = open(log_file)
    except:
        return "</br>Can not open log file"

    total_lines_wanted = lines

    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                # from the end of the file
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            # read the last block we haven't yet read
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count('\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = ''.join(reversed(blocks))
    return '\n</br>'.join(all_read_text.splitlines()[-total_lines_wanted:])

#with open("/opt/game-ai-ui/game-ai-ui/user_agents/user1/agent_log") as f:
    #print get_last_log(f)
