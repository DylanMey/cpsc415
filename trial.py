import time
full_board  = []
start_time = time.time()

for i in range(100):
    temp_row = []
    for x in range(100):
        temp_row.append(".")
        for x in range(100):
            pass
    full_board.append(temp_row)
print("--- %s seconds ---" % (time.time() - start_time))
