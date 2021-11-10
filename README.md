## SNS ASSIGNMENT2
CLIENT-
 Implemented as a transmitter. Here the transmitter has option to send the message correctly or by changing the message.
Once client enters a message to send, There is a option 'Y' or 'N' to ask the transmitter to send correct message or wrong message.
'Y'- Correct message is sent to receiver.
'N'- Wrong message sent to receiver.

Now the message is encoded and crc is appended to it and sent to receiver.
17 bit key used for CRC-
10001000000100001
Encoding Matrix- A=
[[0,-3,-2],
[1,-4,-2],
[-3,4,1]]

SERVER-
Implemented as Receiver. Here message that comes is first split into cipher text and crc. Then message is decoded and converted to binary and its CRC is calculated. If the calculated CRC bits equal to received the crc, Correct message is received otherwise wrong.
17 bit key used for CRC-
10001000000100001
Decoding Matrix- A inverse=
[[4,-5,-2],
[5,-6,-2],
[-8,9,3]]