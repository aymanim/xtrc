#!/usr/bin/env python


import multiprocessing


def sender(conn, iters, comms):
    p = 0
    for i in range(iters):
        for c in range(comms):
            p += 1
            conn.send(str(i))
    conn.close()

def relay(conn1, conn2, iters, comms):
    for i in range(iters):
        for c in range(comms):
            conn1.recv()
            conn2.send(str(i))
    conn1.close()
    conn2.close()

def reciever(conn, iters, comms):
    for i in range(iters):
        for c in range(comms):
            # print 
            conn.recv()
    conn.close()


if __name__ == '__main__':
    num_relays = 3
    num_iterations = 100000
    num_comms_per_iteration = 5
    num_cores = multiprocessing.cpu_count()
    num_transfers = num_cores
    print num_transfers

    pipes = []
    transfers = []

    # Each sender has num_relays relays
    for i in range(num_transfers * (num_relays + 1)):
        parent_conn, child_conn = multiprocessing.Pipe()
        pipes.append([parent_conn, child_conn])

    print len(pipes)

    # Each core needs a sender
    for i in range(num_transfers):
        transfers.append([multiprocessing.Process(target=sender, args=(pipes[i * (num_relays+1)][0], 
            num_iterations, num_comms_per_iteration))])

    # Set up the relays
    for i in range(num_transfers):
        for r in range(num_relays):
            transfers[i].append(multiprocessing.Process(target=relay, args=(pipes[i * (num_relays+1) + r][1], 
                pipes[i * (num_relays+1) + r + 1][0], num_iterations, num_comms_per_iteration)))

    # Each the transfer with a reception
    for i in range(num_transfers):
        transfers[i].append(multiprocessing.Process(target=reciever, args=(pipes[i * (num_relays+1) - 1][1], num_iterations, 
            num_comms_per_iteration)))


    for t in transfers:
        for process in t:
            process.start()

    
    for t in transfers:
        for process in t:
            process.join()


