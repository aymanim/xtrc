xtrc
====

Run all cores at close to 100% for some amount of time. This time is not clearly
defined but it is around 45 seconds on my machine. 

Uses multiple "transfer chains" made of a sender [S], relay(s) [R] and reciever [C]

Sender initates a transfer of trivial data over a pipe, and the data travels
the entire S-R..-C chain. 

Program stops after all the Cs have received the data

Tested on ubuntu precise.
