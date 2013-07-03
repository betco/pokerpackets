Poker Packets
=============

this package contains all files needed to

 * build and create all relevant poker classes
 * convert these packets to json structures
 * convert these packets to the binary poker protocol
 * only rely on **attributes** sections!


for more information please read the docstrings or take 
a look at the documentation at [http://pokermania.github.io/pokerpackets](http://pokermania.github.io/pokerpackets).

-------------

### Packet (id: 0)

    Packet base class

### PacketString (id: 1)

    Packet containing a single string

attributes:

    string: string: <length of string as unsigned short (2 bytes)><string>

### PacketInt (id: 2)

    Packet containing an unsigned integer value

attributes:

    value: unsigned int (4 bytes)

c example:
```c
struct packet_int {
    unsigned int value;
}
```

### PacketError (id: 3)

    Packet describing an error

attributes:

    message: string: <length of string as unsigned short (2 bytes)><string>
    code: unsigned int (4 bytes)
    other_type: unsigned char (1 byte)

### PacketAck (id: 4)

    

### PacketPing (id: 5)

    

### PacketSerial (id: 6)

    Semantics: the serial number of the authenticated user
               associated to the client after a PacketLogin
               was sent. This packet is sent to the client
               after the PacketAuthOk acknowledging the success
               of the authentication.
    
    Direction: server => client
    
    serial: the unique number associated to the user.

attributes:

    serial: unsigned int (4 bytes)

c example:
```c
struct packet_serial {
    unsigned int serial;
}
```

### PacketQuit (id: 7)

    Client tells the server it will leave

### PacketAuthOk (id: 8)

    Semantics: authentication request succeeded.
    
    Direction: server => client

### PacketAuthRefused (id: 9)

    Semantics: authentication request was refused by the server.
    
    Direction: server => client
    
    message: human readable reason for the authentication failure
    code: machine readable code matching the human readable message
          the list of which can be found in the PacketPokerSetAccount
          packet definition
    other_type: the type of the packet that triggered the authentication
                error, i.e. :class:`PACKET_LOGIN <pokerpackets.packets.PacketLogin>`

attributes:

    message: string: <length of string as unsigned short (2 bytes)><string>
    code: unsigned int (4 bytes)
    other_type: unsigned char (1 byte)

### PacketLogin (id: 10)

    Semantics: authentify user "name" with "password".
    
    Direction: server <= client
    
    If the user/password combination is valid, the
    PacketAuthOk packet will be sent back to the client,
    immediately followed by the PacketSerial packet that
    holds the serial number of the user.
    
    If the user/password combination is invalid, the
    PacketAuthRefused packet will be sent back to the client.
    If the user is already logged in, a PacketError is sent
    with code set to PacketLogin.LOGGED.
    
    name: valid user name as a string
    password: matching password string

attributes:

    name: string: <length of string as unsigned short (2 bytes)><string>
    password: string: <length of string as unsigned short (2 bytes)><string>

### PacketAuthRequest (id: 11)

    Packet to ask authentification from the client

### PacketList (id: 12)

    Packet containing a list of packets

attributes:

    packets: packet list: <number of packets as unsigned short (2 bytes)>[<binary packed packet>,..]

### PacketLogout (id: 13)

    Login out

### PacketBootstrap (id: 14)

    

### PacketProtocolError (id: 15)

    Client protocol version does not match server protocol version.

attributes:

    message: string: <length of string as unsigned short (2 bytes)><string>
    code: unsigned int (4 bytes)
    other_type: unsigned char (1 byte)

### PacketMessage (id: 16)

    server => client
    Informative messages

attributes:

    string: string: <length of string as unsigned short (2 bytes)><string>

### PacketAuth (id: 25)

    Semantics: authentify user with "auth" token.
    
    Direction: server <= client
    
    If the auth string is valid, the
    PacketAuthOk packet will be sent back to the client,
    immediately followed by the PacketSerial packet that
    holds the serial number of the user.
    
    If the auth string is invalid, the
    PacketAuthRefused packet will be sent back to the client.
    If the user is already logged in, a PacketError is sent
    with code set to PacketAuth.LOGGED.
    
    auth: valid user auth hash as a string

attributes:

    auth: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerSeats (id: 50)

    Semantics: attribution of the seats of a game to the players.
    
    Context: packet sent at least once per turn. It is guaranteed
    that no player engaged in a turn (i.e. who shows in a
     :class:`PACKET_POKER_IN_GAME <pokerpackets.networkpackets.PacketPokerInGame>` packet) will leave their seat before
    the turn is over (i.e. before packet  :class:`PACKET_POKER_STATE <pokerpackets.networkpackets.PacketPokerState>` packet
    with string == "end" is received).
    It is guaranteed that all PACKET_PLAYER_ARRIVE packets for
    all players listed in the "seats" have already been sent
    by the server.
    
    Notes: The list is 10 seats long even when a game only allows 5
    players to seat.
    
    seats: list of serials of players. The list contains exactly 10 integers.
           The position of the serial of a given player is the seat number.
           A serial of 0 means the seat is empty.
           Example: [ 0, 0, 201, 0, 0, 0, 0, 0, 305, 0 ]
    game_id: integer uniquely identifying a game.

attributes:

    seats: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned int (4 bytes)>,..]
    game_id: unsigned int (4 bytes)

### PacketPokerId (id: 51)

    abstract packet with game id and serial

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_id {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerMessage (id: 52)

    server => client
    Informative messages

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    string: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerError (id: 53)

    Packet describing an error

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    message: string: <length of string as unsigned short (2 bytes)><string>
    code: unsigned int (4 bytes)
    other_type: unsigned char (1 byte)

### PacketPokerPosition (id: 54)

    Semantics: the player "serial" is now in position for game
    "game_id" and should act. If "serial" is 0, no player is
    in position.
    
    Direction: server  => client
    
    Context: emitted by the server when paying blinds or antes,
    in which case the "serial" field does not contain a
    serial number but a position. This packet is discarded
    when other packets are inferred. Inferred by the client
    during all other betting rounds.
    A :class:`PACKET_POKER_POSITION <pokerpackets.networkpackets.PacketPokerPosition>` with serial 0 is inferred by the
    client at the end of each turn.
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    game_id: unsigned int (4 bytes)
    position: unsigned char (1 byte, -1 encoded as 255)
    serial: unsigned int (4 bytes)

### PacketPokerInt (id: 55)

    base class for a int coded amount

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    amount: unsigned int (4 bytes)

c example:
```c
struct packet_poker_int {
    unsigned int serial;
    unsigned int game_id;
    unsigned int amount;
}
```

### PacketPokerBet (id: 56)

    base class for raise. It is not used. To bet use PokerRaise instead.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    amount: unsigned int (4 bytes)

c example:
```c
struct packet_poker_bet {
    unsigned int serial;
    unsigned int game_id;
    unsigned int amount;
}
```

### PacketPokerFold (id: 57)

    Semantics: the "serial" player folded.
    
    Direction: server <=> client
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_fold {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerState (id: 58)

    Semantics: the state of the game "game_id" changed to
    "string". The common game states are:
    
     null : new game.
     end : a game just ended.
     blindAnte : players are paying blinds and/or antes.
    
    The other game states are not pre-determined and depend on the content
    of the variant file. For instance, the states matching the
    poker.holdem.xml variant file are : pre-flop, flop, turn and river.
    
    Direction: server  => client
    
    Context: the sequence of states is guaranteed, i.e. "turn" will never be
    sent before "flop". However, there is no guarantee that the next state
    will ever be sent. For instance, if a holdem game is canceled
    (i.e. :class:`PACKET_POKER_CANCELED <pokerpackets.networkpackets.PacketPokerCanceled>` is sent) because no player is willing to pay
    the blinds, the client must know that it will never receive the
    packet announcing the "pre-flop" state. The "end" state is not
    sent when a game is canceled (i.e. :class:`PACKET_POKER_CANCELED <pokerpackets.networkpackets.PacketPokerCanceled>` is sent).
    
    serial: the unique number associated to the user.
    game_id: integer uniquely identifying a game.
    string: state of the game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    string: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerWin (id: 59)

    Semantics: the "serials" of the players who won
    the turn for game "game_id" to display the showdown.
    
    Context: this packet is sent even when there is no showdown, i.e. when all
    other players folded. However, it is not sent if the game is canceled
    (i.e. :class:`PACKET_POKER_CANCELED <pokerpackets.networkpackets.PacketPokerCanceled>` is sent). It is sent after
    the :class:`PACKET_POKER_STATE <pokerpackets.networkpackets.PacketPokerState>` packet announcing the "end" state and after all
    necessary information is sent to explain the
    showdown (i.e. the value of the losing cards). The client may deduce
    the serials of players who won from previous packets and use the
    packet information for checking purposes only.
    
    The client infers the following packets from :class:`PACKET_POKER_WIN <pokerpackets.networkpackets.PacketPokerWin>`:
    
     :class:`PACKET_POKER_PLAYER_NO_CARDS <pokerpackets.clientpackets.PacketPokerPlayerNoCards>`
     :class:`PACKET_POKER_BEST_CARDS <pokerpackets.clientpackets.PacketPokerBestCards>`
     :class:`PACKET_POKER_CHIPS_POT_MERGE <pokerpackets.clientpackets.PacketPokerChipsPotMerge>`
     PACKET_POKER_CHIPS_POT2PLAYER
     :class:`PACKET_POKER_POT_CHIPS <pokerpackets.clientpackets.PacketPokerPotChips>`
     :class:`PACKET_POKER_PLAYER_CHIPS <pokerpackets.networkpackets.PacketPokerPlayerChips>`
    
    They roughly match the following logic. Some players mucked their
    losing cards (:class:`PACKET_POKER_PLAYER_NO_CARDS <pokerpackets.clientpackets.PacketPokerPlayerNoCards>`). The winners show their
    best five card combination (high and/or low)
     :class:`PACKET_POKER_BEST_CARDS <pokerpackets.clientpackets.PacketPokerBestCards>`. If there are split pots and a player wins
    more than one pot, merge the chips together before giving them to the
    winner (:class:`PACKET_POKER_CHIPS_POT_MERGE <pokerpackets.clientpackets.PacketPokerChipsPotMerge>`). Give each player the part of
    the pot they won (PACKET_POKER_CHIPS_POT2PLAYER): there may be more
    than one packet for each player if more than one pot is involved. When
    the distribution is finished all pots are empty
    (:class:`PACKET_POKER_POT_CHIPS <pokerpackets.clientpackets.PacketPokerPotChips>`) and each player has a new amount of chips in
    their stack (:class:`PACKET_POKER_PLAYER_CHIPS <pokerpackets.networkpackets.PacketPokerPlayerChips>`). These last two packets make
    it possible for the client to ignore the chips movements and only deal
    with the final chips amounts.
    
    The :class:`PACKET_POKER_BEST_CARDS <pokerpackets.clientpackets.PacketPokerBestCards>` is only infered for actual winners. Not
    for players who participated in the showdown but lost. The cards of
    these losers are known from a :class:`PACKET_POKER_CARDS <pokerpackets.networkpackets.PacketPokerCards>` sent before the
     :class:`PACKET_POKER_WIN <pokerpackets.networkpackets.PacketPokerWin>`.
    
    Direction: server  => client
    
    serials: list of serials of players who won.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    serials: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned int (4 bytes)>,..]

### PacketPokerCards (id: 60)

    base class for player / board / best cards

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    cards: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned char (1 byte)>,..]

### PacketPokerPlayerCards (id: 61)

    Semantics: the ordered list of "cards" for player "serial"
    in game "game_id".
    
    Direction: server  => client
    
    cards: list of integers describing cards.
           255 == placeholder, i.e. down card with unknown value
           bit 7 and bit 8 set == down card
           bit 7 and bit 8 not set == up card
           bits 1 to 6 == card value as follows:
    
           2h/00  2d/13  2c/26  2s/39
           3h/01  3d/14  3c/27  3s/40
           4h/02  4d/15  4c/28  4s/41
           5h/03  5d/16  5c/29  5s/42
           6h/04  6d/17  6c/30  6s/43
           7h/05  7d/18  7c/31  7s/44
           8h/06  8d/19  8c/32  8s/45
           9h/07  9d/20  9c/33  9s/46
           Th/08  Td/21  Tc/34  Ts/47
           Jh/09  Jd/22  Jc/35  Js/48
           Qh/10  Qd/23  Qc/36  Qs/49
           Kh/11  Kd/24  Kc/37  Ks/50
           Ah/12  Ad/25  Ac/38  As/51
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    cards: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned char (1 byte)>,..]

### PacketPokerBoardCards (id: 62)

    Semantics: the ordered list of community "cards"
    for game "game_id".
    
    Direction: server  => client
    
    cards: list of integers describing cards.
           255 == placeholder, i.e. down card with unknown value
           bit 7 and bit 8 set == down card
           bit 7 and bit 8 not set == up card
           bits 1 to 6 == card value as follows:
    
           2h/00  2d/13  2c/26  2s/39
           3h/01  3d/14  3c/27  3s/40
           4h/02  4d/15  4c/28  4s/41
           5h/03  5d/16  5c/29  5s/42
           6h/04  6d/17  6c/30  6s/43
           7h/05  7d/18  7c/31  7s/44
           8h/06  8d/19  8c/32  8s/45
           9h/07  9d/20  9c/33  9s/46
           Th/08  Td/21  Tc/34  Ts/47
           Jh/09  Jd/22  Jc/35  Js/48
           Qh/10  Qd/23  Qc/36  Qs/49
           Kh/11  Kd/24  Kc/37  Ks/50
           Ah/12  Ad/25  Ac/38  As/51
    
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    cards: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned char (1 byte)>,..]

### PacketPokerChips (id: 63)

    base class

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    bet: unsigned long long (8 bytes)

c example:
```c
struct packet_poker_chips {
    unsigned int serial;
    unsigned int game_id;
    unsigned long long bet;
}
```

### PacketPokerPlayerChips (id: 64)

    Semantics: the "money" of the player "serial" engaged in
    game "game_id" and the "bet" currently wagered by the player, if any.
    
    Direction: server  => client
    
    Context: this packet is infered each time the bet or the chip
    stack of a player is modified.
    
    bet: the number of chips wagered by the player for the current betting round.
    money: the number of chips available to the player for this game.
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    bet: unsigned long long (8 bytes)
    money: unsigned long long (8 bytes)

c example:
```c
struct packet_poker_player_chips {
    unsigned int serial;
    unsigned int game_id;
    unsigned long long bet;
    unsigned long long money;
}
```

### PacketPokerCheck (id: 65)

    Semantics: the "serial" player checked in game
    "game_id".
    
    Direction: server <=> client
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_check {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerStart (id: 66)

    Semantics: start the hand "hand_serial" for game "game_id". If
    "level" is greater than zero, play at tournament level "level".
    If "level" is greater than zero, meaning that the hand is part
    of a tournament, the fields "hands_count" is set to the number
    of hands since the beginning of the tournament and "time" is set to
    the number of seconds since the beginning of the
    tournament.
    
    Direction: server  => client
    
    Context: this packet is sent exactly once per turn, after the
     :class:`PACKET_POKER_DEALER <pokerpackets.networkpackets.PacketPokerDealer>` and :class:`PACKET_POKER_IN_GAME <pokerpackets.networkpackets.PacketPokerInGame>` packets relevant to
    the hand to come.
    A :class:`PACKET_POKER_CHIPS_POT_RESET <pokerpackets.clientpackets.PacketPokerChipsPotReset>` packet is inferred after this packet.
    A :class:`PACKET_POKER_PLAYER_CHIPS <pokerpackets.networkpackets.PacketPokerPlayerChips>` packet is inferred for each player sit after
    this packet.
    
    hands_count: total number of hands dealt for this game.
    time: number of seconds since the first hand dealt for this game.
    hand_serial: server wide unique identifier of this hand.
    level: integer indicating the tournament level at which the current
           hand is played.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    hands_count: unsigned int (4 bytes)
    time: unsigned int (4 bytes)
    hand_serial: unsigned int (4 bytes)
    level: unsigned char (1 byte)

c example:
```c
struct packet_poker_start {
    unsigned int serial;
    unsigned int game_id;
    unsigned int hands_count;
    unsigned int time;
    unsigned int hand_serial;
    unsigned char level;
}
```

### PacketPokerInGame (id: 67)

    Semantics: the list of "players" serials who are participating
    in the hand to come or the current hand for the game "game_id".
    
    Context: this packet is sent before the hand starts (i.e. before
    the :class:`PACKET_POKER_START <pokerpackets.networkpackets.PacketPokerStart>` packet is sent). It may also be sent before
    the end of the "blindAnte" round (i.e. before a :class:`PACKET_POKER_STATE <pokerpackets.networkpackets.PacketPokerState>`
    packet changing the state "blindAnte" to something else is sent).
    The later case happen when a player refuses to pay the blind or
    the ante. When the hand is running and is past the "blindAnte" round,
    no :class:`PACKET_POKER_IN_GAME <pokerpackets.networkpackets.PacketPokerInGame>` packet is sent.
    
    Direction: server => client
    
    players: list of serials of players participating in the hand.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    players: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned int (4 bytes)>,..]

### PacketPokerCall (id: 68)

    Semantics: the "serial" player called in game "game_id".
    
    Direction: server <=> client
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_call {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerRaise (id: 69)

    Semantics: the "serial" player raised "amount" chips in
    game "game_id".
    
    Direction: server <=> client
    
    Context: the client infers a :class:`PACKET_POKER_BET_LIMIT <pokerpackets.clientpackets.PacketPokerBetLimit>` packet each
    time the position changes.
    
    amount: the number of chips for the raise. A value of all 0 means the lowest possible raise.
         A value larger than the maximum raise will be clamped by
         the server.
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    amount: unsigned int (4 bytes)

c example:
```c
struct packet_poker_raise {
    unsigned int serial;
    unsigned int game_id;
    unsigned int amount;
}
```

### PacketPokerDealer (id: 70)

    Semantics: the dealer button for game "game_id" is at seat "dealer".
    and the previous dealer was at seat "previous_dealer"
    
    Direction: server  => client
    
    Context: this packet is guaranteed to be sent when the game is not
    running. The dealer is never altered while the game is running.
    It is never sent for non button games such as stud 7.
    
    dealer: the seat number on wich the dealer button is located [0-9].
    previous_dealer: the seat number on wich the previous dealer button is located [0-9].
    game_id: integer uniquely identifying a game.

attributes:

    game_id: unsigned int (4 bytes)
    dealer: unsigned char (1 byte, -1 encoded as 255)
    previous_dealer: unsigned char (1 byte, -1 encoded as 255)

### PacketPokerTableJoin (id: 71)

    Semantics: player "serial" wants to become an observer
    of the game "game_id".
    
    There are three possible outcomes for the client in response to a
    PacketPokerTableJoin():
    
      (0) In the case that the join is completely successful, or if the player
          had already joined the table, the following packets are sent:
    
              :class:`PACKET_POKER_TABLE <pokerpackets.networkpackets.PacketPokerTable>`
              :class:`PACKET_POKER_BATCH_MODE <pokerpackets.networkpackets.PacketPokerBatchMode>`
              for each player in the game:
                   :class:`PACKET_POKER_PLAYER_ARRIVE <pokerpackets.networkpackets.PacketPokerPlayerArrive>`
              if the player is playing:
                    :class:`PACKET_POKER_PLAYER_CHIPS <pokerpackets.networkpackets.PacketPokerPlayerChips>`
              if the player is sit:
                    :class:`PACKET_POKER_SIT <pokerpackets.networkpackets.PacketPokerSit>`
              :class:`PACKET_POKER_SEATS <pokerpackets.networkpackets.PacketPokerSeats>`
              if the game is running:
                    the exact packet sequence that lead to the current state
                    of the game. Varies according to the game.
              :class:`PACKET_POKER_STREAM_MODE <pokerpackets.networkpackets.PacketPokerStreamMode>`
    
          Note clearly that if the player had already previously joined the
          table, the packets above will be sent as if the player just joined.
          However, in that case, the packet will have no side effect.
    
    
       (1) If the the player was unable to join the table specifically that
           the server has reached the maximum number of joined players, two
           packets will be sent to the client, the second of which is
           deprecated:
    
            (a) the following packet (recommended way of testing for failure):
                PacketPokerError(code      = PacketPokerTableJoin.FULL,
                                message   = "This server has too many seated players and observers.",
                               other_type = :class:`PACKET_POKER_TABLE_JOIN <pokerpackets.networkpackets.PacketPokerTableJoin>`,
                               serial     = <player's serial id>,
                               game_id    = <id of the table>)
    
            (b) a packet, :class:`PACKET_POKER_TABLE <pokerpackets.networkpackets.PacketPokerTable>`, with serial 0 will be sent.  It
                will contain no meaningful information.  (THIS BEHAVIOR IS
                DEPRECATED, and is left only for older clients.
                New clients should not rely on this behavior.)
    
      (2) If the player cannot join the table for any reason (other than the
          table is FULL (as per (1) above), two packets will be sent to the
          client, one of which is deprecated:
    
           (a) the following packet (recommended way of testing for failure):
               PacketPokerError(code      = PacketPokerTableJoin.GENERAL_FAILURE,
                                message   = <some string of non-zero length, for use
                                            in displaying to the user>,
                               other_type = :class:`PACKET_POKER_TABLE_JOIN <pokerpackets.networkpackets.PacketPokerTableJoin>`,
                               serial     = <player's serial id>,
                               game_id    = 0)
    
           (b) a packet, :class:`PACKET_POKER_TABLE <pokerpackets.networkpackets.PacketPokerTable>`, with serial 0 will be sent.  It
               will contain no meaningful information.  (THIS BEHAVIOR IS
               DEPRECATED, and is left only for older clients.
               New clients should not rely on this behavior.)
    
    Direction: server <= client
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_table_join {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerTableSelect (id: 72)

    Semantics: request the list of tables matching the "string" constraint.
    The answer is a possibly empty :class:`PACKET_POKER_TABLE_LIST <pokerpackets.networkpackets.PacketPokerTableList>` packet.
    
    Direction: server <=  client
    
    string: currency<tabulation>variant
            Examples: 1 holdem selects all holdem tables using this currency
            The specials value "my" restricts the search to the tables
            in which the player id attached to the connection is playing.

attributes:

    string: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerTable (id: 73)

    Semantics: the full description of a poker game. When sent
    to the server, act as a request to create the corresponding
    game. When sent by the server, describes an existing poker
    game.
    
    The answer sent to the client will be the same as the answer
    sent when receiving a PacketPokerTableJoin packet.
    
    Direction: server <=> client
    
    Display information:
    # 10 seats (P01 to P10)
    # a dealer button (D)
    # each player has two chip stacks displayed on the table
    ## the chips that are not engaged in the game (M)
    ## the chips that were bet during this betting round (B)
    # each player two places for cards
    ## up to 5 cards hidden in his hand (H)
    ## up to 7 cards on the table in front of him (some up some down) (V)
    # 5 community cards are displayed face up in the middle (C)
    # up to 9 pots are in the middle, each for a player who is allin (P1 to P9)
    # at showdown the winning hands are
    ## two hands for high / low variants (colors on H, V or C)
    ## as many winning hands per allin player
    {{{
            HHHHH   HHHHH    HHHHH   HHHHH
             P09     P10      P01     P02
           VVVVVVV VVVVVVV  VVVVVVV VVVVVVV
             B M     B M      B M     B M
      HHHHH                               HHHHH
       P08 M B        CCCCC            B M P03
     VVVVVVV P1 P2 P3 P4 P5 P6 P7 P8 P9  VVVVVVV
    
             B M     B M      B M     B M D
           VVVVVVV VVVVVVV   VVVVVVV VVVVVVV
             P07     P06       P05     P04
            HHHHH   HHHHH     HHHHH   HHHHH
    }}}
    
    name: symbolic name of the game.
    variant: base name of the variant that must match a poker.<variant>.xml
             file containing a full description of the variant.
    betting_structure: base name of the betting structure that must
                       match a poker.<betting_structure>.xml file containing
                       a full description of the betting structure.
                       The betting_structure has a naming convention:
                       <small blind>-<big_blind>_<min buy_in>-<max buy_in>_<something>
    id: integer used as the unique id of the game and referred to
        with the "game_id" field in all other packets.
    seats: maximum number of seats in this game.
    average_pot: the average amount put in the pot in the past few minutes.
    percent_flop: the average percentage of players after the flop in the past
                  few minutes.
    players: the number of players who joined the table and are seated
    observers: the number of players who joined (as in :class:`PACKET_POKER_TABLE_JOIN <pokerpackets.networkpackets.PacketPokerTableJoin>`)
               the table but are not seated.
    waiting: the number of players in the waiting list.
    player_timeout: the number of seconds after which a player in position is forced to
             play (by folding).
    muck_timeout: the number of seconds after which a player is forced to muck.
    currency_serial: int currency id
    skin: name of the level model to use
    reason: string representing the reason that this packet is being sent to
            the client.  Possible values are ("", "TableList", "TablePicker",
            "TourneyMove", "TourneyStart", "TableJoin", "TableCreate", "HandReplay")

attributes:

    id: unsigned int (4 bytes)
    seats: unsigned char (1 byte)
    average_pot: unsigned int (4 bytes)
    hands_per_hour: unsigned short (2 bytes)
    percent_flop: unsigned char (1 byte)
    players: unsigned char (1 byte)
    observers: unsigned short (2 bytes)
    waiting: unsigned char (1 byte)
    player_timeout: unsigned short (2 bytes)
    muck_timeout: unsigned short (2 bytes)
    currency_serial: unsigned int (4 bytes)
    name: string: <length of string as unsigned short (2 bytes)><string>
    variant: string: <length of string as unsigned short (2 bytes)><string>
    betting_structure: string: <length of string as unsigned short (2 bytes)><string>
    skin: string: <length of string as unsigned short (2 bytes)><string>
    reason: string: <length of string as unsigned short (2 bytes)><string>
    tourney_serial: unsigned int (4 bytes)
    player_seated: not transmitted over network (ignored)

### PacketPokerTableList (id: 74)

    Semantics: a list of :class:`PACKET_POKER_TABLE <pokerpackets.networkpackets.PacketPokerTable>` packets sent as a
    response to a PACKET_POKER_SELECT request.
    
    Direction: server  => client
    
    packets: a list of :class:`PACKET_POKER_TABLE <pokerpackets.networkpackets.PacketPokerTable>` packets.

attributes:

    packets: packet list: <number of packets as unsigned short (2 bytes)>[<binary packed packet>,..]
    players: unsigned int (4 bytes)
    tables: unsigned int (4 bytes)

### PacketPokerSit (id: 75)

    Semantics: the player "serial" is willing to participate in
    the game "game_id".
    
    Direction: server <=> client
    
    Context: this packet must occur after getting a seat for the
    game (i.e. a :class:`PACKET_POKER_SEAT <pokerpackets.networkpackets.PacketPokerSeat>` is honored by the server). A
    number of :class:`PACKET_POKER_SIT <pokerpackets.networkpackets.PacketPokerSit>` packets are inferred from the
     :class:`PACKET_POKER_IN_GAME <pokerpackets.networkpackets.PacketPokerInGame>` packet. The server will broadcast to
    all players and observers the :class:`PACKET_POKER_SIT <pokerpackets.networkpackets.PacketPokerSit>` in case of
    success. The server will not send anything back if an error
    occurs.
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_sit {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerTableDestroy (id: 76)

    destroy

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_table_destroy {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerTimeoutWarning (id: 77)

    Semantics: the player "serial" is taking too long to play and will
    be folded automatically shortly in the game "game_id".
    
    Direction: server  => client
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    timeout: unsigned int (4 bytes)
    when: not transmitted over network (ignored)

c example:
```c
struct packet_poker_timeout_warning {
    unsigned int serial;
    unsigned int game_id;
    unsigned int timeout;
}
```

### PacketPokerTimeoutNotice (id: 78)

    Semantics: the player "serial" is took too long to play and has
    been folded in the game "game_id".
    
    Direction: server  => client
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_timeout_notice {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerSeat (id: 79)

    Semantics: the player "serial" is seated on the seat "seat"
    in the game "game_id". When a client asks for seat 255,
    it instructs the server to chose the first seat available.
    If the server refuses a request, it answers to the
    requestor with a :class:`PACKET_POKER_SEAT <pokerpackets.networkpackets.PacketPokerSeat>` packet with a seat field
    set to 255.
    
    Direction: server <=> client
    
    Context: the player must join the game (:class:`PACKET_POKER_TABLE_JOIN <pokerpackets.networkpackets.PacketPokerTableJoin>`)
    before issuing a request for a seat. If the request is a success,
    the server will send a :class:`PACKET_POKER_PLAYER_ARRIVE <pokerpackets.networkpackets.PacketPokerPlayerArrive>` and a
     PACKET_POKER_TABLE_SEATS packet.
    
    seat: a seat number in the interval [0,9] or 255 for an invalid seat.
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    seat: unsigned char (1 byte, -1 encoded as 255)

### PacketPokerTableMove (id: 80)

    Semantics: move player "serial" from game "game_id" to
    game "to_game_id". Special operation meant to reseat a player
    from a tournament game to another. The player is automatically
    seated at sit-in in the new game.
    
    Direction: server  => client
    
    Context: this packet is equivalent to a PACKET_POKER_LEAVE immediately
    followed by a PACKET_POKER_JOIN, a :class:`PACKET_POKER_SEAT <pokerpackets.networkpackets.PacketPokerSeat>` and a :class:`PACKET_POKER_SIT <pokerpackets.networkpackets.PacketPokerSit>`
    without the race conditions that would occur if using multiple packets.
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.
    to_game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    seat: unsigned char (1 byte, -1 encoded as 255)
    to_game_id: unsigned int (4 bytes)

### PacketPokerPlayerLeave (id: 81)

    Semantics: the player "serial" leaves the seat "seat" at game "game_id".
    
    Direction: server <=> client
    
    Context: ineffective in tournament games. If the player is playing a
    hand the server will wait until the end of the turn to relay the
    packet to other players involved in the same hand. A player is allowed
    to leave in the middle of the game but the server hides this to the
    other players.
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.
    seat: the seat left in the range [0,9]

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    seat: unsigned char (1 byte, -1 encoded as 255)

### PacketPokerSitOut (id: 82)

    Semantics: the player "serial" seated at the game "game_id"
    is now sit out, i.e. not willing to participate in the game.
    
    Direction: server <=> client
    
    Context: if the game is not running (i.e. not between :class:`PACKET_POKER_START <pokerpackets.networkpackets.PacketPokerStart>`
    packet and a :class:`PACKET_POKER_STATE <pokerpackets.networkpackets.PacketPokerState>` with state == "end" or a :class:`PACKET_POKER_CANCELED <pokerpackets.networkpackets.PacketPokerCanceled>` )
    or still in the blind / ante phase (i.e. the last :class:`PACKET_POKER_STATE <pokerpackets.networkpackets.PacketPokerState>` was
    state == "blindAnte"), the server honors the request immediately and broadcasts the packet
    to all the players watching or participating in the game. If the game
    is running and is not in the blind / ante phase, the request is
    interpreted as a will to fold (equivalent to :class:`PACKET_POKER_FOLD <pokerpackets.networkpackets.PacketPokerFold>`) when
    the player comes in position and to sit out when the game ends
    (i.e. the :class:`PACKET_POKER_SIT_OUT <pokerpackets.networkpackets.PacketPokerSitOut>` is postponed to the end of the game).
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_sit_out {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerTableQuit (id: 83)

    Semantics: the player "serial" is will to be disconnected from
    game "game_id".
    
    Direction: server <=  client / client <=> client
    
    Context: inferred when sent to the server because no answer
    is expected from the server.
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_table_quit {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerBuyIn (id: 84)

    Semantics: the player "serial" is willing to participate in
    the game "game_id" with an amount equal to "amount". The server
    will ensure that the "amount" fits the game constraints (i.e.
    player bankroll or betting structure limits).
    
    Direction: server <=  client.
    
    Context: this packet must occur after a successfull :class:`PACKET_POKER_SEAT <pokerpackets.networkpackets.PacketPokerSeat>`
    and before a :class:`PACKET_POKER_SIT <pokerpackets.networkpackets.PacketPokerSit>` for the same player. The minimum/maximum
    buy in are determined by the betting structure of the game, as
    specified in the :class:`PACKET_POKER_TABLE <pokerpackets.networkpackets.PacketPokerTable>` packet.
    
    amount: integer specifying the amount to bring to the game.
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    amount: unsigned int (4 bytes)

c example:
```c
struct packet_poker_buy_in {
    unsigned int serial;
    unsigned int game_id;
    unsigned int amount;
}
```

### PacketPokerRebuy (id: 85)

    Semantics: the player "serial" is willing to participate in
    the game "game_id" with an amount equal to "amount". The server
    will ensure that the "amount" fits the game constraints (i.e.
    player bankroll or betting structure limits).
    
    Direction: server <=  client.
    
    Context: this packet must occur after a successfull :class:`PACKET_POKER_BUY_IN <pokerpackets.networkpackets.PacketPokerBuyIn>`
    The minimum/maximum rebuy are determined by the betting structure of
    the game, as specified in the :class:`PACKET_POKER_TABLE <pokerpackets.networkpackets.PacketPokerTable>` packet. The player
    may rebuy at any moment if he has less than the maximum amount of money
    allowed by the betting structure.
    
    amount: integer specifying the amount to bring to the game.
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    amount: unsigned int (4 bytes)

c example:
```c
struct packet_poker_rebuy {
    unsigned int serial;
    unsigned int game_id;
    unsigned int amount;
}
```

### PacketPokerChat (id: 86)

    Semantics: a text "message" sent to all players seated
    at the poker table "game_id".
    
    Direction: server  <=> client
    
    message: a text message string (2^16 long max)
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    message: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerPlayerInfo (id: 87)

    Semantics: the player "serial" descriptive informations. When
    sent to the server, sets the information and broadcast them
    to other players. When sent from the server, notify the client
    of a change in the player descriptive informations.
    
    Direction: server <=> client
    
    name: login name of the player.
    url: outfit url to load from
    outfit: name of the player outfit.
    serial: integer uniquely identifying a player.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    name: string: <length of string as unsigned short (2 bytes)><string>
    outfit: string: <length of string as unsigned short (2 bytes)><string>
    url: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerPlayerArrive (id: 88)

    Semantics: the player "serial" is seated at the game "game_id".
    Descriptive information for the player such as "name" and "outfit"
    is provided.
    
    Direction: server  => client
    
    Context: this packet is the server answer to successfull
     :class:`PACKET_POKER_SEAT <pokerpackets.networkpackets.PacketPokerSeat>` request. The actual seat allocated to the player
    will be specified in the next :class:`PACKET_POKER_SEATS <pokerpackets.networkpackets.PacketPokerSeats>` packet.
    
    name: login name of the player.
    outfit: name of the player outfit, usually referring to the organization he belongs
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    name: string: <length of string as unsigned short (2 bytes)><string>
    outfit: string: <length of string as unsigned short (2 bytes)><string>
    url: string: <length of string as unsigned short (2 bytes)><string>
    blind: bool string: <length of string as unsigned short (2 bytes)><string>, there are two special strings ('_TRUE'/'_FALSE')
    remove_next_turn: unsigned char (1 byte, true = 1 false = 0)
    sit_out: unsigned char (1 byte, true = 1 false = 0)
    sit_out_next_turn: unsigned char (1 byte, true = 1 false = 0)
    auto: unsigned char (1 byte, true = 1 false = 0)
    auto_blind_ante: unsigned char (1 byte, true = 1 false = 0)
    wait_for: unsigned char (1 byte, true = 1 false = 0)
    buy_in_payed: unsigned char (1 byte, true = 1 false = 0)
    seat: unsigned char (1 byte, None/NULL encoded as 255)

### PacketPokerHandSelect (id: 89)

    Semantics: query the hand history for player "serial"
    and filter them according to the "string" boolean expression.
    Return slice of the matching hands that are in the range
    ["start", "start" + "count"[
    
    Direction: server <=  client
    
    Context: the answer of the server to this query is a
     :class:`PACKET_POKER_HAND_LIST <pokerpackets.networkpackets.PacketPokerHandList>` packet.
    
    string: a valid SQL WHERE expression on the hands table. The
    available fields are "name" for the symbolic name of the hand,
    "description" for the python expression describing the hand, "serial"
    for the unique identifier of the hand also known as the hand_serial
    in the :class:`PACKET_POKER_START <pokerpackets.networkpackets.PacketPokerStart>` packet.
    start: index of the first matching hand
    count: number of matching hands to return starting from start
    serial: integer uniquely identifying a player.

attributes:

    string: string: <length of string as unsigned short (2 bytes)><string>
    start: unsigned int (4 bytes)
    count: unsigned char (1 byte)

### PacketPokerHandList (id: 90)

    Semantics: a list of hand serials known to the server.
    
    Direction: server  => client
    
    Context: reply to the :class:`PACKET_POKER_HAND_SELECT <pokerpackets.networkpackets.PacketPokerHandSelect>` packet.
    
    hands: list of integers uniquely identifying a hand to the server.

attributes:

    string: string: <length of string as unsigned short (2 bytes)><string>
    start: unsigned int (4 bytes)
    count: unsigned char (1 byte)
    hands: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned int (4 bytes)>,..]
    total: unsigned int (4 bytes)

### PacketPokerHandSelectAll (id: 91)

    Semantics: query the hand history for all players
    and filter them according to the "string" boolean expression.
    The user must be logged in and have administrative permissions
    for this query to succeed.
    
    Direction: server <=  client
    
    Context: the answer of the server to this query is a
     :class:`PACKET_POKER_HAND_LIST <pokerpackets.networkpackets.PacketPokerHandList>` packet.
    
    string: a valid SQL WHERE expression on the hands table. The
    available fields are "name" for the symbolic name of the hand,
    "description" for the python expression describing the hand, "serial"
    for the unique identifier of the hand also known as the hand_serial
    in the :class:`PACKET_POKER_START <pokerpackets.networkpackets.PacketPokerStart>` packet.

attributes:

    string: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerUserInfo (id: 92)

    Semantics: read only user descriptive information, complement
    of :class:`PACKET_POKER_PLAYER_INFO <pokerpackets.networkpackets.PacketPokerPlayerInfo>`.
    
    Direction: server  => client
    
    Context: answer to the :class:`PACKET_POKER_GET_USER_INFO <pokerpackets.networkpackets.PacketPokerGetUserInfo>` packet.
    
    rating: server wide ELO rating.
    serial: integer uniquely identifying a player.

attributes:

    serial: unsigned int (4 bytes)
    rating: unsigned int (4 bytes)
    affiliate: unsigned int (4 bytes)
    name: string: <length of string as unsigned short (2 bytes)><string>
    password: string: <length of string as unsigned short (2 bytes)><string>
    email: string: <length of string as unsigned short (2 bytes)><string>
    money: money: <number of currencys as unsigned short (2 bytes)>[<currency serial as unsinged integer (4 bytes)><money as unsigned long long (8 bytes)><in game money as unsinged long long (8 bytes)><points as unsgined long long (8 bytes)>,..]

### PacketPokerGetUserInfo (id: 93)

    Semantics: request the read only descriptive information
    for player "serial".
    
    Direction: server <=  client
    
    Context: a user must first login (:class:`PACKET_LOGIN <pokerpackets.packets.PacketLogin>`) successfully
    before sending this packet.
    
    serial: integer uniquely identifying a player.

attributes:

    serial: unsigned int (4 bytes)

c example:
```c
struct packet_poker_get_user_info {
    unsigned int serial;
}
```

### PacketPokerAnte (id: 94)

    Semantics: the player "serial" paid an amount of
    "amount" for the ante in game "game_id".
    
    Direction: server <=> client
    
    Context: the server always sends a :class:`PACKET_POKER_POSITION <pokerpackets.networkpackets.PacketPokerPosition>` before
    sending this packet. The client may send this packet after
    receiving a :class:`PACKET_POKER_ANTE_REQUEST <pokerpackets.networkpackets.PacketPokerAnteRequest>`.
    
    Note: the amount may be lower than requested by the betting structure
    when in tournament. Ring games will refuse a player to enter the with
    less than the required amount for blind or/and antes.
    
    amount: amount paid for the ante.
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    amount: unsigned int (4 bytes)

c example:
```c
struct packet_poker_ante {
    unsigned int serial;
    unsigned int game_id;
    unsigned int amount;
}
```

### PacketPokerBlind (id: 95)

    Semantics: the player "serial" paid an amount of
    "amount" for the blind and "dead" for the dead
    in game "game_id".
    
    Direction: server <=> client
    
    Context: the server always sends a :class:`PACKET_POKER_POSITION <pokerpackets.networkpackets.PacketPokerPosition>` before
    sending this packet. The client may send this packet after
    receiving a :class:`PACKET_POKER_BLIND_REQUEST <pokerpackets.networkpackets.PacketPokerBlindRequest>`.
    
    Note: the dead and amount fields are ignored in packets sent
    to the server. They are calculated by the server according to
    the state of the game.
    
    Note: the amount may be lower than requested by the betting structure
    when in tournament. Ring games will refuse a player to enter the with
    less than the required amount for blind or/and antes.
    
    dead: amount paid for the dead (goes to the pot).
    amount: amount paid for the blind (live for the next betting round).
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    amount: unsigned int (4 bytes)
    dead: unsigned int (4 bytes)

c example:
```c
struct packet_poker_blind {
    unsigned int serial;
    unsigned int game_id;
    unsigned int amount;
    unsigned int dead;
}
```

### PacketPokerWaitBigBlind (id: 96)

    Semantics: the player "serial" wants to wait for the big blind
    to reach his seat in game "game_id" before entering the game.
    
    Direction: server <=  client
    
    Context: answer to a :class:`PACKET_POKER_BLIND_REQUEST <pokerpackets.networkpackets.PacketPokerBlindRequest>`. The server
    will implicitly sit out the player by not including him in
    the :class:`PACKET_POKER_IN_GAME <pokerpackets.networkpackets.PacketPokerInGame>` packet sent at the end of the "blindAnte"
    round. The :class:`PACKET_POKER_WAIT_FOR <pokerpackets.networkpackets.PacketPokerWaitFor>` packet is inferred to avoid complex
    interpretation of :class:`PACKET_POKER_IN_GAME <pokerpackets.networkpackets.PacketPokerInGame>` and can be considered
    equivalent to a :class:`PACKET_POKER_SIT_OUT <pokerpackets.networkpackets.PacketPokerSitOut>` packet if the distinction is
    not important to the client.
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_wait_big_blind {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerAutoBlindAnte (id: 97)

    Semantics: the player "serial" asks the server to automatically post the
               blinds or/and antes for game "game_id".  In response to this
               packet, the server sends PacketPokerAutoBlindAnte() if
               AutoBlindAnte has been successfully turned on, otherwise, it
               sends PacketPokerNoautoBlindAnte().
    
    Direction: server <=  client
    
    Context: by default the server will not automatically post the blinds
    or/and antes. 
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_auto_blind_ante {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerNoautoBlindAnte (id: 98)

    Semantics: the player "serial" asks the server to send a
               :class:`PACKET_POKER_BLIND_REQUEST <pokerpackets.networkpackets.PacketPokerBlindRequest>` or/and :class:`PACKET_POKER_ANTE_REQUEST <pokerpackets.networkpackets.PacketPokerAnteRequest>`
               when a blind or/and ante for game "game_id" must be paid.
    
               In response ot this packet, the server sends
               PacketPokerNoautoBlindAnte() if AutoBlindAnte has been
               successfully turned off, otherwise, it sends
               PacketPokerAautoBlindAnte().
    
    Direction: server <=  client
    
    Context: by default the server behaves in this way.
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_noauto_blind_ante {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerCanceled (id: 99)

    Semantics: the game is canceled because only the player
    "serial" is willing to pay the blinds or/and antes.
    The "amount" paid by the player is returned to him. If
    no player is willing to pay the blinds or/and antes, the
    serial is zero.
    
    Direction: server  => client
    
    amount: the amount to return to the player.
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    amount: unsigned int (4 bytes)

c example:
```c
struct packet_poker_canceled {
    unsigned int serial;
    unsigned int game_id;
    unsigned int amount;
}
```

### PacketPokerBlindRequest (id: 100)

    Semantics: the player "serial" is required to pay the a blind
    of "amount" and a dead of "dead" for game "game_id". The logical
    state of the blind is given in "state".
    
    Direction: server  => client
    
    Context: a :class:`PACKET_POKER_POSITION <pokerpackets.networkpackets.PacketPokerPosition>` packet is sent by the server before
    this packet. The answer may be a :class:`PACKET_POKER_SIT_OUT <pokerpackets.networkpackets.PacketPokerSitOut>` (to refuse to
    pay the blind), :class:`PACKET_POKER_BLIND <pokerpackets.networkpackets.PacketPokerBlind>` (to pay the blind),
     :class:`PACKET_POKER_WAIT_BIG_BLIND <pokerpackets.networkpackets.PacketPokerWaitBigBlind>` (if not willing to pay a late blind but
    willing to pay the big blind when due).
    
    state: "small", "big", "late", "big_and_dead".
    dead: amount to pay for the dead (goes to the pot).
    amount: amount to pay for the blind (live for the next betting round).
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    amount: unsigned int (4 bytes)
    dead: unsigned int (4 bytes)
    state: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerAnteRequest (id: 101)

    Semantics: the player "serial" is required to pay the an ante
    of "amount" for game"game_id".
    
    Direction: server  => client
    
    Context: a :class:`PACKET_POKER_POSITION <pokerpackets.networkpackets.PacketPokerPosition>` packet is sent by the server before
    this packet. The answer may be a :class:`PACKET_POKER_SIT_OUT <pokerpackets.networkpackets.PacketPokerSitOut>` (to refuse to
    pay the ante), :class:`PACKET_POKER_ANTE <pokerpackets.networkpackets.PacketPokerAnte>` (to pay the ante).
    
    amount: amount to pay for the ante.
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    amount: unsigned int (4 bytes)

c example:
```c
struct packet_poker_ante_request {
    unsigned int serial;
    unsigned int game_id;
    unsigned int amount;
}
```

### PacketPokerAutoFold (id: 102)

    Semantics: the player "serial" will be folded by the server
    when in position for tournament game "game_id".
    
    Direction: server  => client
    
    Context: this packet informs the players at the table about
    a change of state for a player in tournament games. This
    state can be canceled by a :class:`PACKET_POKER_SIT <pokerpackets.networkpackets.PacketPokerSit>` packet for the same
    player.
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_auto_fold {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerWaitFor (id: 103)

    Semantics: the player "serial" waits for the late
    blind (if "reason" == "late") or the big blind (if
    "reason" == "big") in game "game_id". Otherwise equivalent
    to :class:`PACKET_POKER_SIT_OUT <pokerpackets.networkpackets.PacketPokerSitOut>`.
    
    Direction: server  => client / client <=> client
    
    Context: when sent by the server, it means that the answer of a client
    to a :class:`PACKET_POKER_BLIND_REQUEST <pokerpackets.networkpackets.PacketPokerBlindRequest>` or a :class:`PACKET_POKER_ANTE_REQUEST <pokerpackets.networkpackets.PacketPokerAnteRequest>` was to
    wait for something (i.e.  :class:`PACKET_POKER_WAIT_BIG_BLIND <pokerpackets.networkpackets.PacketPokerWaitBigBlind>`) or that the
    server denied him the right to play this hand because he was on the
    small blind or on the button. When inferred, this packet can be
    handled as if it was a :class:`PACKET_POKER_SIT_OUT <pokerpackets.networkpackets.PacketPokerSitOut>`.
    
    reason: either "big" or "late".
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    reason: bool string: <length of string as unsigned short (2 bytes)><string>, there are two special strings ('_TRUE'/'_FALSE')

### PacketPokerStreamMode (id: 104)

    Semantics: the packets received after this one are
    a stream describing poker games changing as time passes.
    
    Direction: server  => client
    
    Context: this is the default mode in which the packets
    are to be interpreted by the client. This packet is
    only needed after a :class:`PACKET_POKER_BATCH_MODE <pokerpackets.networkpackets.PacketPokerBatchMode>` packet was sent,
    to come back to the default mode.
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_stream_mode {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerBatchMode (id: 105)

    Semantics: the packets received after this one are
    a batch describing a poker game state at a given point
    in time.
    
    Direction: server  => client / client <=> client
    
    Context: the server will send this packet before sending
    a batch of packets describing the current state of a game,
    such as when joining a table. That may involve a long set
    of packets describing the whole action of the game until
    showdown. The client is free to replay it (in accelerated
    mode or as a play back) or to merely use these packets to
    rebuild the state of the game. It is produced by the client
    when the resendPacket method is called in order to send a
    sequence of packets describing a game for which the client
    already knows everything (this is handy when switching tables,
    for instance).
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_batch_mode {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerLookCards (id: 106)

    Semantics: the player "serial" is looking at his cards
    in game "game_id".
    
    Direction: server <=> client
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    state: not transmitted over network (ignored)

c example:
```c
struct packet_poker_look_cards {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerTableRequestPlayersList (id: 107)

    Semantics: client request the player list of the game "game_id".
    
    Direction: server <= client
    
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_table_request_players_list {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerPlayersList (id: 108)

    Semantics: List of players participating in "game_id". 
    
    Direction: server => client
    
    game_id: integer uniquely identifying a game.
    players: list of player serials participating in "game_id"
     for each player, a list of two numbers:
         name: name of the player
         chips: integer player chips in cent
         flag: byte 0

attributes:

    game_id: unsigned int (4 bytes)
    players: players: <number of players as unsinged short (2 bytes)>[<length of name as unsinged short (2 bytes)><name (string)><chips as unsigned int (4 bytes)><flags as unsinged char (1 bytes)>,..]

### PacketPokerPersonalInfo (id: 109)

    

attributes:

    serial: unsigned int (4 bytes)
    rating: unsigned int (4 bytes)
    affiliate: unsigned int (4 bytes)
    name: string: <length of string as unsigned short (2 bytes)><string>
    password: string: <length of string as unsigned short (2 bytes)><string>
    email: string: <length of string as unsigned short (2 bytes)><string>
    money: money: <number of currencys as unsigned short (2 bytes)>[<currency serial as unsinged integer (4 bytes)><money as unsigned long long (8 bytes)><in game money as unsinged long long (8 bytes)><points as unsgined long long (8 bytes)>,..]
    firstname: string: <length of string as unsigned short (2 bytes)><string>
    lastname: string: <length of string as unsigned short (2 bytes)><string>
    addr_street: string: <length of string as unsigned short (2 bytes)><string>
    addr_street2: string: <length of string as unsigned short (2 bytes)><string>
    addr_zip: string: <length of string as unsigned short (2 bytes)><string>
    addr_town: string: <length of string as unsigned short (2 bytes)><string>
    addr_state: string: <length of string as unsigned short (2 bytes)><string>
    addr_country: string: <length of string as unsigned short (2 bytes)><string>
    phone: string: <length of string as unsigned short (2 bytes)><string>
    gender: string: <length of string as unsigned short (2 bytes)><string>
    birthdate: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerGetPersonalInfo (id: 110)

    Semantics: request the read only descriptive information
    for player "serial".
    
    Direction: server <=  client
    
    Context: a personal must first login (:class:`PACKET_LOGIN <pokerpackets.packets.PacketLogin>`) successfully
    before sending this packet.
    
    serial: integer uniquely identifying a player.

attributes:

    serial: unsigned int (4 bytes)

c example:
```c
struct packet_poker_get_personal_info {
    unsigned int serial;
}
```

### PacketPokerTourneySelect (id: 111)

    Semantics: request the list of tourneys matching the "string" constraint.
    The answer is a :class:`PACKET_POKER_TOURNEY_LIST <pokerpackets.networkpackets.PacketPokerTourneyList>` packet. If no tournament matches
    the constraint, the list will be empty.
    
    Direction: server <=  client
    
    string: 1) empty string selects all tournaments
            2) a string that contains no tabulation selects
               the tournament with the same name
            3) a string with a tabulation selects all tournaments
               of a given type (sit&go or regular) that can be played
               using a given currency. The string before the tabulation
               is the name of the currency, the string after the tabulation
               distinguishes between sit&go and regular.
    
            Examples: 1<tabulation>sit_n_go selects all sit&go tournaments
                      using currency 1.
                      2<tabulation>regular selects all regular tournaments
                      using currency 2

attributes:

    string: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerTourney (id: 112)

    

attributes:

    serial: unsigned int (4 bytes)
    schedule_serial: not transmitted over network (ignored)
    buy_in: unsigned int (4 bytes)
    rake: unsigned int (4 bytes)
    start_time: unsigned int (4 bytes)
    rebuy_time_remaining: unsigned int (4 bytes)
    kick_timeout: unsigned int (4 bytes)
    sit_n_go: unsigned char (1 byte, 'y' = 1, everything else = 0
    players_quota: unsigned short (2 bytes)
    registered: unsigned short (2 bytes)
    currency_serial: unsigned int (4 bytes)
    breaks_first: unsigned short (2 bytes)
    breaks_interval: unsigned short (2 bytes)
    breaks_duration: unsigned short (2 bytes)
    description_short: string: <length of string as unsigned short (2 bytes)><string>
    variant: string: <length of string as unsigned short (2 bytes)><string>
    state: string: <length of string as unsigned short (2 bytes)><string>
    name: string: <length of string as unsigned short (2 bytes)><string>
    skin: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerTourneyInfo (id: 113)

    

attributes:

    serial: unsigned int (4 bytes)
    schedule_serial: not transmitted over network (ignored)
    buy_in: unsigned int (4 bytes)
    rake: unsigned int (4 bytes)
    start_time: unsigned int (4 bytes)
    rebuy_time_remaining: unsigned int (4 bytes)
    kick_timeout: unsigned int (4 bytes)
    sit_n_go: unsigned char (1 byte, 'y' = 1, everything else = 0
    players_quota: unsigned short (2 bytes)
    registered: unsigned short (2 bytes)
    currency_serial: unsigned int (4 bytes)
    breaks_first: unsigned short (2 bytes)
    breaks_interval: unsigned short (2 bytes)
    breaks_duration: unsigned short (2 bytes)
    description_short: string: <length of string as unsigned short (2 bytes)><string>
    variant: string: <length of string as unsigned short (2 bytes)><string>
    state: string: <length of string as unsigned short (2 bytes)><string>
    name: string: <length of string as unsigned short (2 bytes)><string>
    skin: string: <length of string as unsigned short (2 bytes)><string>
    description_long: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerTourneyList (id: 114)

    Semantics: a list of :class:`PACKET_POKER_TOURNEY <pokerpackets.networkpackets.PacketPokerTourney>` packets sent as a
    response to a PACKET_POKER_SELECT request.
    
    Direction: server  => client
    
    packets: a list of :class:`PACKET_POKER_TOURNEY <pokerpackets.networkpackets.PacketPokerTourney>` packets.

attributes:

    packets: packet list: <number of packets as unsigned short (2 bytes)>[<binary packed packet>,..]
    players: unsigned int (4 bytes)
    tourneys: unsigned int (4 bytes)

### PacketPokerTourneyRequestPlayersList (id: 115)

    Semantics: client request the player list of the tourney "tourney_serial".
    
    Direction: server <= client
    
    Context: If the tournament "tourney_serial" is among the list of known tournamens,
    a PacketPokerTourneyPlayersList is returned by the server. Otherwise,
    a PacketError is returned with the code set to
    PacketPokerTourneyRegister.DOES_NOT_EXIST.
    
    tourney_serial: integer uniquely identifying a tournament.

attributes:

    serial: unsigned int (4 bytes)
    tourney_serial: unsigned int (4 bytes)

c example:
```c
struct packet_poker_tourney_request_players_list {
    unsigned int serial;
    unsigned int tourney_serial;
}
```

### PacketPokerTourneyRegister (id: 116)

    Semantics: register player "serial" to tournament "tourney_serial".
    
    Direction: server <= client
    
    If the player is registered successfully, the server will send
    back the packet to the client.
    
    If an error occurs during the tournament registration, the server
    will send back
    
      PacketError(other_type = :class:`PACKET_POKER_TOURNEY_REGISTER <pokerpackets.networkpackets.PacketPokerTourneyRegister>`)
    
    with the "code" field name set as follows:
    
    DOES_NOT_EXIST : the "tourney_serial" field does not match any existing
                     tournaments.
    ALREADY_REGISTERED : the "serial" player is already listed as
                     a registered player in the "tourney_serial" tournament.
    REGISTRATION_REFUSED : the "serial" player registration was refused
                     because the "tourney_serial" tournament is no longer in
                     the registration phase or because the players
                     quota was exceeded.
    NOT_ENOUGH_MONEY : the "serial" player does not have enough money
                     to pay the "tourney_serial" tournament.
    SERVER_ERROR : the server failed to register the player because the
                   database is inconsistent.
    VIA_SATELLITE : registration is only allowed by playing a satellite
    
    serial: integer uniquely identifying a player.
    tourney_serial: integer uniquely identifying a tournament.

attributes:

    serial: unsigned int (4 bytes)
    tourney_serial: unsigned int (4 bytes)

c example:
```c
struct packet_poker_tourney_register {
    unsigned int serial;
    unsigned int tourney_serial;
}
```

### PacketPokerTourneyUnregister (id: 117)

    Semantics: unregister player "serial" from tournament "tourney_serial".
    
    Direction: server <= client
    
    If the player is successfully unregistered, the server will send
    back the packet to the client.
    
    If an error occurs during the tournament registration, the server
    will send back
    
      PacketError(other_type = :class:`PACKET_POKER_TOURNEY_UNREGISTER <pokerpackets.networkpackets.PacketPokerTourneyUnregister>`)
    
    with the "code" field name set as follows:
    
    DOES_NOT_EXIST : the "tourney_serial" field does not match any existing
                     tournaments.
    NOT_REGISTERED : the "serial" player is not listed as
                     a registered player in the "tourney_serial" tournament.
    TOO_LATE : the "serial" player cannot unregister from the tournament
               because it already started.
    SERVER_ERROR : the server failed to unregister the player because the
                   database is inconsistent.
    
    serial: integer uniquely identifying a player.
    tourney_serial: integer uniquely identifying a tournament.

attributes:

    serial: unsigned int (4 bytes)
    tourney_serial: unsigned int (4 bytes)

c example:
```c
struct packet_poker_tourney_unregister {
    unsigned int serial;
    unsigned int tourney_serial;
}
```

### PacketPokerTourneyPlayersList (id: 118)

    Semantics: List of players participating in tourney "serial". 
    
    Direction: server => client
    
    serial: integer uniquely identifying a tourney.
    players: list of player serials participating in tourney "tourney_serial"
     for each player, a list of two numbers:
         name: name of the player
         chips: integer -1
         flag: byte 0

attributes:

    tourney_serial: unsigned int (4 bytes)
    players: players: <number of players as unsinged short (2 bytes)>[<length of name as unsinged short (2 bytes)><name (string)><chips as unsigned int (4 bytes)><flags as unsinged char (1 bytes)>,..]

### PacketPokerHandHistory (id: 119)

    

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    history: string: <length of string as unsigned short (2 bytes)><string>
    serial2name: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerSetAccount (id: 120)

    

attributes:

    serial: unsigned int (4 bytes)
    rating: unsigned int (4 bytes)
    affiliate: unsigned int (4 bytes)
    name: string: <length of string as unsigned short (2 bytes)><string>
    password: string: <length of string as unsigned short (2 bytes)><string>
    email: string: <length of string as unsigned short (2 bytes)><string>
    money: money: <number of currencys as unsigned short (2 bytes)>[<currency serial as unsinged integer (4 bytes)><money as unsigned long long (8 bytes)><in game money as unsinged long long (8 bytes)><points as unsgined long long (8 bytes)>,..]
    firstname: string: <length of string as unsigned short (2 bytes)><string>
    lastname: string: <length of string as unsigned short (2 bytes)><string>
    addr_street: string: <length of string as unsigned short (2 bytes)><string>
    addr_street2: string: <length of string as unsigned short (2 bytes)><string>
    addr_zip: string: <length of string as unsigned short (2 bytes)><string>
    addr_town: string: <length of string as unsigned short (2 bytes)><string>
    addr_state: string: <length of string as unsigned short (2 bytes)><string>
    addr_country: string: <length of string as unsigned short (2 bytes)><string>
    phone: string: <length of string as unsigned short (2 bytes)><string>
    gender: string: <length of string as unsigned short (2 bytes)><string>
    birthdate: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerCreateAccount (id: 121)

    

attributes:

    serial: unsigned int (4 bytes)
    rating: unsigned int (4 bytes)
    affiliate: unsigned int (4 bytes)
    name: string: <length of string as unsigned short (2 bytes)><string>
    password: string: <length of string as unsigned short (2 bytes)><string>
    email: string: <length of string as unsigned short (2 bytes)><string>
    money: money: <number of currencys as unsigned short (2 bytes)>[<currency serial as unsinged integer (4 bytes)><money as unsigned long long (8 bytes)><in game money as unsinged long long (8 bytes)><points as unsgined long long (8 bytes)>,..]
    firstname: string: <length of string as unsigned short (2 bytes)><string>
    lastname: string: <length of string as unsigned short (2 bytes)><string>
    addr_street: string: <length of string as unsigned short (2 bytes)><string>
    addr_street2: string: <length of string as unsigned short (2 bytes)><string>
    addr_zip: string: <length of string as unsigned short (2 bytes)><string>
    addr_town: string: <length of string as unsigned short (2 bytes)><string>
    addr_state: string: <length of string as unsigned short (2 bytes)><string>
    addr_country: string: <length of string as unsigned short (2 bytes)><string>
    phone: string: <length of string as unsigned short (2 bytes)><string>
    gender: string: <length of string as unsigned short (2 bytes)><string>
    birthdate: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerPlayerSelf (id: 122)

    

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_player_self {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerGetPlayerInfo (id: 123)

    Semantics: ask the server for a PacketPokerPlayerInfo packet
    describing the player that is logged in with this connection.
    
    If the user is not logged in the following packet is returned
    
    PacketError(code = PacketPokerGetPlayerInfo.NOT_LOGGED,
                message = "Not logged in",
                other_type = :class:`PACKET_POKER_GET_PLAYER_INFO <pokerpackets.networkpackets.PacketPokerGetPlayerInfo>`)
    
    If the user is logged in a PacketPokerPlayerInfo packet is sent
    to the client.
    
    Direction: server <= client

### PacketPokerRoles (id: 124)

    

attributes:

    serial: unsigned int (4 bytes)
    roles: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerSetRole (id: 125)

    Semantics: tell the server the purpose of the connection.
    There are two possible roles : PLAY for a regular client
    that plays poker, EDIT for a connection used to edit the
    player properties but not play. There can only be one
    active role per user at a given time.
    
    The user must not be not logged in when this packet is
    sent or undefined results will occur.
    
    Direction: server <= client
    
    roles: string PLAY or EDIT

attributes:

    serial: unsigned int (4 bytes)
    roles: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerReadyToPlay (id: 126)

    Semantics: the "serial" player is ready to begin a new
    hand at table "game_id".
    
    Direction: server <= client
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_ready_to_play {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerProcessingHand (id: 127)

    Semantics: the "serial" player is not ready to begin a new
    hand at table "game_id" because the client is still processing
    the data related to the previous hand.
    
    Direction: server <= client
    
    Context: should be sent by the client immediately after receiving
    the :class:`POKER_START <pokerpackets.networkpackets.PacketPokerStart>` packet.
    
    Note: the packet is ignored if the "serial" player is not at the table.
    
    Note: because of a race condition, it will not work as expected
    if the game plays too fast. For instance, if the hand finishes
    before the packet :class:`POKER_PROCESSING_HAND <pokerpackets.networkpackets.PacketPokerProcessingHand>` is received by the server.
    This will typically happen the first time a player gets a seat at the 
    table.
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_processing_hand {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerMuckRequest (id: 128)

    Semantics: server is announcing a muck request to muckable players
    in game "game_id". The packet is sent to all players at the table.
    If a player in the list does not respond in time (the actual timeout
    value depends on the server configuration and is usualy 5 seconds),
    her hand will be mucked.
    
    Direction: server <=> client
    game_id: integer uniquely identifying a game.
    muckable_serials: list of serials of players that are given a the choice to muck.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    muckable_serials: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned int (4 bytes)>,..]

### PacketPokerAutoMuck (id: 129)

    Semantics: By default the client will not be proposed to muck : the
    server will always muck for him.
    The client may send the PacketPokerAutoMuck to inform the server of its
    muck preferences for "game_id". The "info" field must be set to one
    of the following:
    
    AUTO_MUCK_NEVER  0x00
    AUTO_MUCK_WIN    0x01
    AUTO_MUCK_LOSE   0x02
    AUTO_MUCK_ALWAYS AUTO_MUCK_WIN + AUTO_MUCK_LOSE
    
    When "info" is set to AUTO_MUCK_NEVER, the server will always send
    a PacketPokerMuckRequest including the serial of the player for
    this "game_id" when mucking is an option. If "info" is set to
    AUTO_MUCK_WIN the server will
    not include the serial of the player in the PacketPokerMuckRequest packet
    for this "game_id" if the player wins but is not forced to
    how its cards (i.e. when the opponent folded to him).
    If "info" is set to AUTO_MUCK_LOSE the server will not include the serial
    of the player in the PacketPokerMuckRequest packet for this "game_id"
    when the player loses the hand but is not forced to show his cards.
    AUTO_MUCK_ALWAYS is the equivalent of requesting AUTO_MUCK_LOSE and
    AUTO_MUCK_WIN at the same time and is the default.
    
    Direction: server <= client
    game_id: integer uniquely identifying a game.
    info: bitfield indicating what muck situations are of interest.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    auto_muck: unsigned char (1 byte)

c example:
```c
struct packet_poker_auto_muck {
    unsigned int serial;
    unsigned int game_id;
    unsigned char auto_muck;
}
```

### PacketPokerMuckAccept (id: 130)

    

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_muck_accept {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerMuckDeny (id: 131)

    

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_muck_deny {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerCashIn (id: 132)

    Semantics: add "value" cents of currency "url" to the
    "serial" player account using the "name"/"bserial" note.
    
    Context: If the CASH_IN is successfull, PacketAck is returned.
    Otherwise PacketError is returned with the "message" field set
    to a human readable error explanation. The poker server must
    be able to check the validity of the note provided
    by accessing the currency server at "url".
    
    The url, bserial, name, value fields content are filled from
    the result of a request to a currency web service. For instance:
    
    http://localhost/poker-web/currency_one.php?command=get_note&value=100&autocommit=yes
    
    will return the following content
    
    http://localhost/poker-web/currency_one.php     22      cfae906e9d7d6f6321b04d659059f4d6f8b86a34      100
    
    that can be used to build a packet by setting:
    
    url = http://localhost/poker-web/currency_one.php
    bserial = 22
    name = cfae906e9d7d6f6321b04d659059f4d6f8b86a34
    value = 100
    
    When the poker server honors the PacketPokerCashIn packet, it will
    contact the currency server to change the note. It means the note sent
    will become invalid and be replaced by a new one, known only to the
    poker server.
    
    Direction: server <= client
    
    value: integer value of the note in cent
    currency: url string of the currency server
    bserial: integer value of the serial of the note
    name: string cryptographic name of the note
    note: tuple of (url, bserial, name, value) that overrides the parameters
          of the same name
    serial: integer uniquely identifying a player.

attributes:

    serial: unsigned int (4 bytes)
    url: string: <length of string as unsigned short (2 bytes)><string>
    name: string: <length of string as unsigned short (2 bytes)><string>
    application_data: string: <length of string as unsigned short (2 bytes)><string>
    bserial: unsigned int (4 bytes)
    value: unsigned int (4 bytes)

### PacketPokerCashOut (id: 133)

    

attributes:

    serial: unsigned int (4 bytes)
    url: string: <length of string as unsigned short (2 bytes)><string>
    name: string: <length of string as unsigned short (2 bytes)><string>
    application_data: string: <length of string as unsigned short (2 bytes)><string>
    bserial: unsigned int (4 bytes)
    value: unsigned int (4 bytes)

### PacketPokerCashOutCommit (id: 134)

    

attributes:

    transaction_id: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerCashQuery (id: 135)

    

attributes:

    application_data: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerRake (id: 136)

    

attributes:

    value: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_rake {
    unsigned int value;
    unsigned int game_id;
}
```

### PacketPokerTourneyRank (id: 137)

    Semantics: a :class:`PACKET_POKER_TOURNEY_RANK <pokerpackets.networkpackets.PacketPokerTourneyRank>` sent to the player who leaves the tournament
    
    Direction: server  => client
    
    serial: serial of the tourney
    
    rank: the rank.
    
    players: the number of players in this tourney
    
    money: the money won

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    players: unsigned int (4 bytes)
    money: unsigned int (4 bytes)
    rank: unsigned int (4 bytes)

c example:
```c
struct packet_poker_tourney_rank {
    unsigned int serial;
    unsigned int game_id;
    unsigned int players;
    unsigned int money;
    unsigned int rank;
}
```

### PacketPokerHandReplay (id: 140)

    

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_hand_replay {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerGameMessage (id: 141)

    

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    string: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerExplain (id: 142)

    Semantics: control the level of verbosity of the server
    according to the "value" bit field as follows:
    
    Context: If the server accepts the request, a PacketAck is
    returned. Otherwise a PacketError is returned with
    other_type set to :class:`PACKET_POKER_EXPLAIN <pokerpackets.networkpackets.PacketPokerExplain>`.
    
    Note: in order to produce the desired behaviour, the
    PACKET_POKER_EXPLAIN must be sent before starting to
    observe the action at a table (i.e. before sending PACKET_POKER_JOIN)
    and before any PACKET_POKER_LOGIN is sent.
    
    value == NONE
      The server assumes the client knows the poker rules, presumably
      by using poker-engine.
    
    value == ALL
      The server assumes the client does not know poker and will
      explain every game event in great detail.
    
    Direction: server <= client

attributes:

    value: unsigned int (4 bytes)

c example:
```c
struct packet_poker_explain {
    unsigned int value;
}
```

### PacketPokerStatsQuery (id: 143)

    

attributes:

    string: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerStats (id: 144)

    

attributes:

    players: unsigned int (4 bytes)
    hands: unsigned int (4 bytes)
    bytesin: unsigned int (4 bytes)
    bytesout: unsigned int (4 bytes)

c example:
```c
struct packet_poker_stats {
    unsigned int players;
    unsigned int hands;
    unsigned int bytesin;
    unsigned int bytesout;
}
```

### PacketPokerBuyInLimits (id: 145)

    Semantics: the buy-in boundaries for "game_id" in the range
    ["min","max"]. An optimal buy-in is suggested in "best". A
    player is considered broke unless he has at least "rebuy_min"
    at the table.
    
    Direction: server => client
    
    Context: sent immediately after the PacketPokerTable packet.
    
    min: minimum buy-in in cent.
    max: minimum buy-in in cent.
    best: optimal buy-in in cent.
    rebuy_min: the minimum amount to play a hand.
    game_id: integer uniquely identifying a game.

attributes:

    game_id: unsigned int (4 bytes)
    min: unsigned int (4 bytes)
    max: unsigned int (4 bytes)
    best: unsigned int (4 bytes)
    rebuy_min: unsigned int (4 bytes)

c example:
```c
struct packet_poker_buy_in_limits {
    unsigned int game_id;
    unsigned int min;
    unsigned int max;
    unsigned int best;
    unsigned int rebuy_min;
}
```

### PacketPokerMonitor (id: 146)

    

### PacketPokerMonitorEvent (id: 147)

    

attributes:

    event: unsigned int (4 bytes)
    param1: unsigned int (4 bytes)
    param2: unsigned int (4 bytes)
    param3: unsigned int (4 bytes)

c example:
```c
struct packet_poker_monitor_event {
    unsigned int event;
    unsigned int param1;
    unsigned int param2;
    unsigned int param3;
}
```

### PacketPokerGetTourneyManager (id: 148)

    Semantics: Get tournement manager packet for tourney_serial
    
    Direction: server <= client
    
    If the tourney_serial is not found occurs, the server will send back
    
      PacketError(other_type = :class:`PACKET_POKER_GET_TOURNEY_MANAGER <pokerpackets.networkpackets.PacketPokerGetTourneyManager>`)
    
    with the "code" field name set as follows:
    
    DOES_NOT_EXIST : the "tourney_serial" field does not match any existing
                     tournaments.

attributes:

    tourney_serial: unsigned int (4 bytes)

c example:
```c
struct packet_poker_get_tourney_manager {
    unsigned int tourney_serial;
}
```

### PacketPokerTourneyManager (id: 149)

    

### PacketPokerAutoPlay (id: 150)

    Semantics: If the player leaves the keybord, or the connection breaks, a bot could play for player instead
    This Behaviour could be defined by this package.
    
    As soon as the player returns, or the connection is rebuild, the player should send a :class:`POKER_SIT <pokerpackets.networkpackets.PacketPokerSit>` packet.
    
    AUTOPLAY_NO  0x00
    AUTOPLAY_YES 0x01
    
    Direction: server <= client
    game_id: integer uniquely indentifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    auto_play: unsigned char (1 byte)

c example:
```c
struct packet_poker_auto_play {
    unsigned int serial;
    unsigned int game_id;
    unsigned char auto_play;
}
```

### PacketPokerGetPlayerPlaces (id: 151)

    

attributes:

    serial: unsigned int (4 bytes)
    name: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerPlayerPlaces (id: 152)

    

attributes:

    serial: unsigned int (4 bytes)
    tables: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned int (4 bytes)>,..]
    tourneys: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned int (4 bytes)>,..]

### PacketPokerSetLocale (id: 153)

    Semantics: the player "serial" is required to set the "locale" string,
    which must be a locale supported by the server.  If the locale is
    supported by the server, it will be made the locale used for strings sent
    by PokerExplain packets.
    
    Direction: server  <= client
    
    Context: If the locale is supported by the server, a PacketAck is
    returned, and future PokerExplain strings will be localized to the
    requested language.  Otherwise a PacketError is returned with other_type
    set to :class:`PACKET_POKER_SET_LOCALE <pokerpackets.networkpackets.PacketPokerSetLocale>`.
    
    locale: string representing a valid locale supported by the server configuration (e.g.,  "fr_FR" or "fr")
    serial: integer uniquely identifying a player.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    locale: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerTableTourneyBreakBegin (id: 154)

    Semantics: Players at table "game_id" will receive this packet when a
    tournament break offically begins.
    
    Direction: server  => client
    
    Context: 
    
    game_id: integer uniquely identifying a game.
    resume_time: time that the tourney will resume, in seconds since 1970-01-01 00:00:00 UTC.

attributes:

    game_id: unsigned int (4 bytes)
    resume_time: unsigned int (4 bytes)

c example:
```c
struct packet_poker_table_tourney_break_begin {
    unsigned int game_id;
    unsigned int resume_time;
}
```

### PacketPokerTableTourneyBreakDone (id: 155)

    Semantics: Players at table "game_id" will receive this packet when a
    tournament break offically ends.
    
    Direction: server  => client
    
    Context: 
    
    game_id: integer uniquely identifying a game.

attributes:

    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_table_tourney_break_done {
    unsigned int game_id;
}
```

### PacketPokerTourneyStart (id: 156)

    Semantics: If sent from the server: The "tourney_serial" tournament started and
    the player is seated at table "table_serial". If sent from a client with appropriate
    permissions, the tourney will be started before it's start_time.
    
    Direction: server <=> client
    
    Context: this packet is sent to the client when it is logged in. The 
    player seated at the table "table_serial" is implicitly the logged in player.
    
    serial: integer uniquely identifying a player. 
    tourney_serial: integer uniquely identifying a tournament.
    table_serial: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    tourney_serial: unsigned int (4 bytes)
    table_serial: unsigned int (4 bytes)

c example:
```c
struct packet_poker_tourney_start {
    unsigned int serial;
    unsigned int tourney_serial;
    unsigned int table_serial;
}
```

### PacketPokerGetTourneyPlayerStats (id: 157)

    Semantics: if the player "serial" is participating in the tourney
               "tourney_serial", he can ask for information about his
               current performance (i.e. his rank) in the tourney and
               compare it to the chips leader and the average chips 
               amount.
    
    Direction: server  <=  client
    
    Context: the packet can be sent by the player as long as the tourney
             is loaded in memory on the server. he will receive an error
             if the tourney is not existing (DOES_NOT_EXIST) or he is or
             was not participating in the tourney (NOT_PARTICIPATING).
    
    serial: integer uniquely identifying a player.
    tourney_serial: integer uniquely indentifying a tourney.

attributes:

    serial: unsigned int (4 bytes)
    tourney_serial: unsigned int (4 bytes)

c example:
```c
struct packet_poker_get_tourney_player_stats {
    unsigned int serial;
    unsigned int tourney_serial;
}
```

### PacketPokerTourneyPlayerStats (id: 158)

    Semantics: contains personalized information for user "serial"
               for tourney "tourney_serial" such as his rank, the 
               current chips leader, and so forth.
    
    Direction: server  =>  client
    
    Context: the packet is sent as a response to PacketPokerGetTourneyPlayerStats
    
    serial: integer uniquely identifying a player.
    tourney_serial: integer uniquely indentifying a tourney.
    rank: integer the current rank of the player
    players_active: integer the number of players who are 
                    still participating in the tourney
    chips_avg: the average amount of chips an active player has
    chips_max: the amount of chips the highest ranked player has
    player_chips_max_serial: the serial of the currently leading player
    player_chips_max_name: the name of the currently leading player

attributes:

    serial: unsigned int (4 bytes)
    tourney_serial: unsigned int (4 bytes)
    rank: unsigned short (2 bytes)
    players_active: unsigned short (2 bytes)
    chips_avg: unsigned long long (8 bytes)
    chips_max: unsigned long long (8 bytes)
    player_chips_max_serial: unsigned int (4 bytes)
    player_chips_max_name: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerTourneyCancel (id: 159)

    Semantics: If sent from a client with appropriate permissions, the tourney 
    will be canceled. This can only happen while the tourney is in the REGISTERING state.
    
    Direction: server <= client
    
    Context: This packet can be sent by a bailor or a user with administrative rights for
    a tourney
    
    serial: integer uniquely identifying a player. 
    tourney_serial: integer uniquely identifying a tournament.

attributes:

    serial: unsigned int (4 bytes)
    tourney_serial: unsigned int (4 bytes)

c example:
```c
struct packet_poker_tourney_cancel {
    unsigned int serial;
    unsigned int tourney_serial;
}
```

### PacketPokerStateInformation (id: 160)

    Semantics: This message is sent to a client whenever the server
               has an inconsistent or otherwise not useful state of the player's
               session object. This packet should help the user to decide how to
               reinstate a correct connection by e.g. re-issuing a PacketPokerTableJoin
               or a PacketLogin packet
               
    Direction: server  =>  client
    
    Context: Since this packet is sent on the server's behalf, usually without the 
             client's direct interaction. It is difficult to define a determined context 
             for it. It is however possible to deduce if the packet is referring to a 
             determined game or not, by looking at the "game_id" field.
             The following error codes are currently used:
             - REMOTE_CONNECTION_LOST: The server is closing the connection to another
                                       remote server, because the session on the server the
                                       client is connected to is expired. 
             - REMOTE_TABLE_EPHEMERAL: Denotes the fact that after the current request the
                                       client's session will be destroyed again. This usually
                                       happens if the server never received a PacketPokerTable 
                                       packet on this connection --> send a PacketPokerTableJoin
                                       packet.
             - SHUTTING_DOWN:          The table at game_id will be gone after the current hand.
                                       This message is sent to the clients on behalf of the server
                                       when the server is shutting down.
              
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.
    message: string representing the error.
    code: integer representing the error.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    code: unsigned int (4 bytes)
    message: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerPlayerStats (id: 161)

    Semantics: the "rank" and "percentile" of the player "serial"
    for the "currency_serial" currency. The player with the largest
    amount of "currency_serial" money has "rank" 1. The "rank" is therefore
    in the range [1..n] where n is the total number of players registered
    on the poker server. The players are divided in G groups and the "percentile" is
    the number of the player group. For instance, if the players are divided in 4 groups
    the top 25% players will be in "percentile" 0, the next
    25% will be in "percentile" 1 and the last
    25% will be in "percentile" 3. The player with "rank" is always in
    "percentile" 0 and the player with least chips in the "currency_serial"
    money is always in the last "percentile".
    
    Direction: server  => client
    
    Context: 
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game. (optional)
    currency_serial: int currency id
    rank: rank of the player 
    percentile: percentile of the player

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    currency_serial: unsigned int (4 bytes)
    rank: unsigned int (4 bytes)
    percentile: unsigned int (4 bytes)

c example:
```c
struct packet_poker_player_stats {
    unsigned int serial;
    unsigned int game_id;
    unsigned int currency_serial;
    unsigned int rank;
    unsigned int percentile;
}
```

### PacketPokerTourneyRebuy (id: 162)

    Semantics: When a client wants to rebuy during a tourney he sends this packet.
    
    Direction: client => server
    
    
    serial: user_serial
    tourney_serial: serial of the tourney

attributes:

    serial: unsigned int (4 bytes)
    tourney_serial: unsigned int (4 bytes)

c example:
```c
struct packet_poker_tourney_rebuy {
    unsigned int serial;
    unsigned int tourney_serial;
}
```

### PacketPokerBetLimits (id: 163)

    

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    min: unsigned int (4 bytes)
    max: unsigned int (4 bytes)
    step: unsigned int (4 bytes)
    cap: unsigned char (1 byte)
    limit: unsigned char (1 byte)

c example:
```c
struct packet_poker_bet_limits {
    unsigned int serial;
    unsigned int game_id;
    unsigned int min;
    unsigned int max;
    unsigned int step;
    unsigned char cap;
    unsigned char limit;
}
```

### PacketPokerTablePicker (id: 165)

    Semantics: The player "serial" wishes to join a table that matches the
               criteria sent.  Empty or non existing entries in criteria means
               "match any".  The table that matches the given criteria, and
               has the most players already seated (but with a seat available
               for the requesting player) will be returned.  An error is
               returned if such a table cannot be found.  If multiple tables
               are equally appropriate, the one with the smallest serial is
               returned.
    
               Note that the player has to be logged in order to pick a table,
               the "serial" field is mandatory.
    
               An additional criterion that is *not* sent by the user (but
               rather inferred by the server) is as follows: cash game tables
               whose minimum buy-in is less than the amount of money available
               to the player in a given currency are eliminated from
               consideration.
    
               If a table matching the criteria is available, it will be as if
               the client had sent the following sequence of packets (plus
               performed the pseudo-code logic below on client side):
    
                   Send: PacketPokerTableJoin()
                   Send: PacketPokerSeat()
                   if auto_blind_ante: # in original packet
                        Send: PacketPokerAutoBlindAnte()
                   Receive: PacketPokerBuyInLimits() [ returning "best", "min" ]
                   if player.money_available < best:
                        Send: PacketPokerBuyIn(amount = min)
                   else:
                        Send: PacketPokerBuyIn(amount = best)
                   Send: PacketPokerSit()
    
               In the case of failure, an error packet as follows will be sent
               to the client:
                 PacketPokerError(code      = PacketPokerTableJoin.GENERAL_FAILURE,
                                  message   = <some string of non-zero length, for use
                                              in displaying to the user>,
                                 other_type = :class:`PACKET_POKER_TABLE_PICKER <pokerpackets.networkpackets.PacketPokerTablePicker>`,
                                 serial     = <player's serial id>,
                                 game_id    = <if failure occured before table matching criteria was identified: 0
                                               else: game.id for table where join was attempted>)
    
               In this case of success, the client can expect to receive all
               the packets that it would expect to receive in response to any
               of the packets listed in "Send" above.  These include:
                      PacketPokerTable()        # info about the table joined
                      PacketPokerBuyInLimits()  # still sent despite mention in pseudo-code above
                      PacketPokerPlayerArrive() # for client.serial
                      PacketPokerPlayerChips()  # for client.serial
                      if auto_blind_ante:
                        PacketPokerAutoBlindAnte()
                      PacketPokerSit()          # for client.serial
                      PacketPokerSeats()
                  
               Note even if a valid PacketPokerTable() is received, it's
               possible, although unlikely, that the intervening operations --
               PacketPokerSeat(), PacketPokerBuyIn() and PacketPokerSit() --
               might fail.  If one of them fails, the client should expect to
               receive the normal errors it would receive if such an operation
               failed.  Clients are advised, upon receiving a valid
               PacketPokerTable() in response, to use the same handling
               routines that it uses for PacketPokerSeat(), PacketPokerBuyIn()
               and PacketPokerSit() to keep parity with the operations the
               server is performing on the client's behalf.
    
    Direction: server <=  client
    
    Context:
    
    serial: integer uniquely identifying a player.
    currency_serial: int currency id (criteria for search)
    variant: base name of the variant sought.
    betting_structure: base name of the betting structure.
    auto_blind_ante: boolean, if True server will act as if
                    PacketPokerAutoBlindAnte() were also sent by client.
                    Defaults to False.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    currency_serial: unsigned int (4 bytes)
    min_players: unsigned int (4 bytes)
    variant: string: <length of string as unsigned short (2 bytes)><string>
    betting_structure: string: <length of string as unsigned short (2 bytes)><string>
    auto_blind_ante: unsigned char (1 byte, true = 1 false = 0)

### PacketPokerCreateTourney (id: 166)

    Semantics: The authorized player represented by "serial",
               seeks to create a new sit-n-go tournament for the players in
               the "players" list of serials. Each player in the list will
               be registered for the new tournament.
    
               The fields "name", "description_short", "description_long", "variant",
               "betting_structure", "seats_per_game", "player_timeout", "currency_serial"
               and "buy_in" have the same semantics as described in the database schema.
    
               Upon success, the response will be PacketAck() for the new sit-n-go tournament.
               If the request is issued by a user that is not authentified, the response will be:
                     PacketAuthRequest()
               If at least one user cannot be registered, the response will be:
                     PacketPokerError(
                       other_type = :class:`PACKET_POKER_CREATE_TOURNEY <pokerpackets.networkpackets.PacketPokerCreateTourney>`,
                       code       = REGISTRATION_FAILED 
                       serial     = the serial of the tournament for which registration failed
    
                       Note: the list of players for which registration has failed is included
                       in the message. An error message will be sent to each players for which
                       registration failed, if they have an active session.
    
    Direction: server <=  client
    
    Context:
    
    serial:            integer uniquely identifying the administrative-level player.
    name:              name for tournament
    description_short: Short description of tournament
    description_long:  Long description of tournament
    variant:           base name of the variant for the new sit-n-go
    betting_structure: base name of the betting structure that must
                       match a poker.<betting_structure>.xml file containing
                       a full description of the betting structure.
    skin:              The skin used for all tourneys and its tables 
    seats_per_game:    Maximum number of seats for each table in this tournament.
    player_timeout:    the number of seconds after which a player in position is forced to
                       play (by folding).
    currency_serial:   int currency id
    buy_in:            Amount, in currency_serial, for buying into this tournament.
    players_quota      Quota of the tournament. If smaller than len(players), len(players) 
                       is used (i.e. the tourney starts immediately).
    players:           Serials of the players participating in the tournament.

attributes:

    serial: unsigned int (4 bytes)
    name: string: <length of string as unsigned short (2 bytes)><string>
    description_short: string: <length of string as unsigned short (2 bytes)><string>
    description_long: string: <length of string as unsigned short (2 bytes)><string>
    players_quota: unsigned int (4 bytes)
    variant: string: <length of string as unsigned short (2 bytes)><string>
    betting_structure: string: <length of string as unsigned short (2 bytes)><string>
    skin: string: <length of string as unsigned short (2 bytes)><string>
    seats_per_game: unsigned int (4 bytes)
    player_timeout: unsigned int (4 bytes)
    currency_serial: unsigned int (4 bytes)
    prize_currency: unsigned int (4 bytes)
    prize_min: unsigned int (4 bytes)
    bailor_serial: unsigned int (4 bytes)
    buy_in: unsigned int (4 bytes)
    rake: unsigned int (4 bytes)
    sit_n_go: unsigned char (1 byte, 'y' = 1, everything else = 0
    start_time: unsigned int (4 bytes)
    players: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned int (4 bytes)>,..]

### PacketPokerLongPoll (id: 167)

    ########################################

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_long_poll {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerLongPollReturn (id: 168)

    ########################################

### PacketSetOption (id: 169)

    serial:     the user_serial that wants to set an option.
    game_id:    the game that should be affetcted by this option.
    name:       the option name.
    value:      the option value as a string.
    
    If the name is not known, or the value doesn't match to the name an PACKET_ERROR is send.
    If everything is Ok, a PACKET_ACK is sent.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    option_id: unsigned char (1 byte)
    value: unsigned char (1 byte)

c example:
```c
struct packet_set_option {
    unsigned int serial;
    unsigned int game_id;
    unsigned char option_id;
    unsigned char value;
}
```

### PacketPokerBestCards (id: 170)

    Semantics: ordered list  of five "bestcards" hand for
    player "serial" in game "game_id" that won the "side"
    side of the pot. The "board", if not empty, is the list
    of community cards at showdown. Also provides the
    "cards" of the player.
    
    Direction: client <=> client
    
    cards: list of integers describing the player cards:
    
           2h/00  2d/13  2c/26  2s/39
           3h/01  3d/14  3c/27  3s/40
           4h/02  4d/15  4c/28  4s/41
           5h/03  5d/16  5c/29  5s/42
           6h/04  6d/17  6c/30  6s/43
           7h/05  7d/18  7c/31  7s/44
           8h/06  8d/19  8c/32  8s/45
           9h/07  9d/20  9c/33  9s/46
           Th/08  Td/21  Tc/34  Ts/47
           Jh/09  Jd/22  Jc/35  Js/48
           Qh/10  Qd/23  Qc/36  Qs/49
           Kh/11  Kd/24  Kc/37  Ks/50
           Ah/12  Ad/25  Ac/38  As/51
           
    bestcards: list of integers describing the winning combination cards:
    board: list of integers describing the community cards:
    hand: readable string of the name best hand
    besthand: 0 if it's not the best hand and 1 if it's the best hand
             best hand is the hand that win the most money
           
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    cards: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned char (1 byte)>,..]
    side: string: <length of string as unsigned short (2 bytes)><string>
    hand: string: <length of string as unsigned short (2 bytes)><string>
    bestcards: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned char (1 byte)>,..]
    board: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned char (1 byte)>,..]
    besthand: unsigned char (1 byte)

### PacketPokerPotChips (id: 171)

    Semantics: the "bet" put in the "index" pot of the "game_id" game.
    
    Direction: client <=> client
    
    context: this packet is sent at least each time the pot index is
    updated.
    
    bet: list of pairs ( chip_value, chip_count ).
    index: integer uniquely identifying a side pot in the range [0,10[
    game_id: integer uniquely identifying a game.

attributes:

    game_id: unsigned int (4 bytes)
    index: unsigned char (1 byte)
    bet: unsigned int (4 bytes)

### PacketPokerBetLimit (id: 173)

    Semantics: a raise must be at least "min" and most "max".
    A call means wagering an amount of "call". The suggested
    step to slide between "min" and "max" is "step". The step
    is guaranteed to be an integral divisor of "call". The
    player would be allin for the amount "allin". The player
    would match the pot if betting "pot".
    
    Context: this packet is issued each time a position change
    occurs.
    
    Direction: client <=> client
    
    min: the minimum amount of a raise.
    max: the maximum amount of a raise.
    step: a hint for sliding in the [min, max] interval.
    call: the amount of a call.
    allin: the amount for which the player goes allin.
    pot: the amount in the pot.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    min: unsigned int (4 bytes)
    max: unsigned int (4 bytes)
    step: unsigned int (4 bytes)
    call: unsigned int (4 bytes)
    allin: unsigned int (4 bytes)
    pot: unsigned int (4 bytes)

c example:
```c
struct packet_poker_bet_limit {
    unsigned int serial;
    unsigned int game_id;
    unsigned int min;
    unsigned int max;
    unsigned int step;
    unsigned int call;
    unsigned int allin;
    unsigned int pot;
}
```

### PacketPokerSitRequest (id: 174)

    

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_sit_request {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerPlayerNoCards (id: 175)

    Semantics: the player "serial" has no cards in game "game_id".
    
    Direction: client <=> client
    
    Context: inferred at showdown.
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_player_no_cards {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerChipsPlayer2Bet (id: 176)

    Semantics: move "chips" from the player "serial" money chip stack
    to the bet chip stack.
    
    Direction: client <=> client
    
    chips: list of pairs ( chip_value, chip_count ).
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    chips: unsigned int (4 bytes)

### PacketPokerChipsBet2Pot (id: 177)

    Semantics: move "chips" from the player "serial" bet chip stack
    to the "pot" pot.
    
    Direction: client <=> client
    
    Context: the pot index is by definition in the range [0,9] because
    it starts at 0 and because there cannot be more pots than players.
    The creation of side pots is inferred by the client when a player
    is all-in and it is guaranteed that pots are numbered sequentially.
    
    pot: the pot index in the range [0,9].
    chips: list of integers counting the number of chips to move.
         The value of each chip is, respectively:
         1 2 5 10 20 25 50 100 250 500 1000 2000 5000.
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    chips: unsigned int (4 bytes)
    pot: unsigned char (1 byte, -1 encoded as 255)

### PacketPokerChipsPot2Player (id: 178)

    Semantics: move "chips" from the pot "pot" to the player "serial"
    money chip stack. The string "reason" explains why these chips 
    are granted to the player. If reason is "win", it means the player
    won the chips either because all other players folded or because
    he had the best hand at showdown. If reason is "uncalled", it means
    the chips are returned to him because no other player was will or
    able to call his wager. If reason is "left-over", it means the chips
    are granted to him because there was an odd chip while splitting the pot.
    
    Direction: client <=> client
    
    Context: the pot index is by definition in the range [0,9] because
    it starts at 0 and because there cannot be more pots than players.
    The creation of side pots is inferred by the client when a player
    is all-in and it is guaranteed that pots are numbered sequentially.
    
    reason: may be one of "win", "uncalled", "left-over"
    pot: the pot index in the range [0,9].
    chips: list of integers counting the number of chips to move.
         The value of each chip is, respectively:
         1 2 5 10 20 25 50 100 250 500 1000 2000 5000.
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    chips: unsigned int (4 bytes)
    pot: unsigned char (1 byte, -1 encoded as 255)
    reason: string: <length of string as unsigned short (2 bytes)><string>

### PacketPokerChipsPotMerge (id: 179)

    Semantics: merge the pots whose indexes are listed in
    "sources" into a single pot at index "destination" in game "game_id".
    
    Direction: client <=> client
    
    Context: when generating PACKET_POKER_CHIPS_POT2PLAYER packets, if
    multiple packet can be avoided by merging pots (e.g. when one player
    wins all the pots).
    
    destination: a pot index in the range [0,9].
    sources: list of pot indexes in the range [0,9].
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    sources: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned char (1 byte)>,..]
    destination: unsigned char (1 byte)

### PacketPokerChipsPotReset (id: 180)

    Semantics: all pots for game "game_id" are set to zero.
    
    Direction: client <=> client
    
    Context: it is inferred after a :class:`PACKET_POKER_TABLE <pokerpackets.networkpackets.PacketPokerTable>` or a
     :class:`PACKET_POKER_START <pokerpackets.networkpackets.PacketPokerStart>` packet is sent by the server. It is inferred
    after the pot is distributed (i.e. after the game terminates
    because a :class:`PACKET_POKER_WIN <pokerpackets.networkpackets.PacketPokerWin>` or :class:`PACKET_POKER_CANCELED <pokerpackets.networkpackets.PacketPokerCanceled>` is received).
    
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_chips_pot_reset {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerChipsBet2player (id: 181)

    chips move from bet to player

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    chips: unsigned int (4 bytes)

### PacketPokerEndRound (id: 182)

    Semantics: closes a betting round for game "game_id".
    
    Direction: client <=> client
    
    Context: inferred at the end of a sequence of packet related to
    a betting round. Paying the blind / ante is not considered a
    betting round. This packet is sent when the client side
    knows that the round is finished but before the corresponding
    packet (:class:`PACKET_POKER_STATE <pokerpackets.networkpackets.PacketPokerState>`) has been received from the server.
    It will be followed by the :class:`POKER_BEGIN_ROUND <pokerpackets.clientpackets.PacketPokerBeginRound>` packet, either
    immediately if the server has no delay between betting rounds
    or later if the server waits a few seconds between two betting
    rounds.
    It is not inferred at the end of the last betting round.
    
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_end_round {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerDealCards (id: 184)

    Semantics: deal "numberOfCards" down cards for each player listed
    in "serials" in game "game_id".
    
    Direction: client <=> client
    
    Context: inferred after the beginning of a betting round (i.e.
    after the :class:`PACKET_POKER_STATE <pokerpackets.networkpackets.PacketPokerState>` packet is received) and after
    the chips involved in the previous betting round have been
    sorted (i.e. after PACKET_POKER_CHIPS_BET2POT packets are
    inferred). Contrary to the :class:`PACKET_POKER_PLAYER_CARDS <pokerpackets.networkpackets.PacketPokerPlayerCards>`,
    this packet is only sent if cards must be dealt. It
    is guaranteed that this packet will always occur before
    the :class:`PACKET_POKER_PLAYER_CARDS <pokerpackets.networkpackets.PacketPokerPlayerCards>` that specify the cards to
    be dealt and that these packets will follow immediately
    after it (no other packet will be inserted between this packet
    and the first :class:`PACKET_POKER_PLAYER_CARDS <pokerpackets.networkpackets.PacketPokerPlayerCards>`). It is also guaranteed
    that exactly one :class:`PACKET_POKER_PLAYER_CARDS <pokerpackets.networkpackets.PacketPokerPlayerCards>` will occur for each
    serial listed in "serials".
    
    numberOfCards: number of cards to be dealt.
    serials: integers uniquely identifying players.
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    numberOfCards: unsigned char (1 byte)
    serials: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned int (4 bytes)>,..]

### PacketPokerSelfInPosition (id: 187)

    Semantics: the player authenticated for this connection
    is in position. Otherwise identical to :class:`PACKET_POKER_POSITION <pokerpackets.networkpackets.PacketPokerPosition>`.

attributes:

    game_id: unsigned int (4 bytes)
    position: unsigned char (1 byte, -1 encoded as 255)
    serial: unsigned int (4 bytes)

### PacketPokerSelfLostPosition (id: 188)

    Semantics: the player authenticated for this connection
    is in position. Otherwise identical to :class:`PACKET_POKER_POSITION <pokerpackets.networkpackets.PacketPokerPosition>`.

attributes:

    game_id: unsigned int (4 bytes)
    position: unsigned char (1 byte, -1 encoded as 255)
    serial: unsigned int (4 bytes)

### PacketPokerHighestBetIncrease (id: 189)

    Semantics: a wager was made in game "game_id" that increases
    the highest bet amount. 
    
    Direction: client <=> client
    
    Context: inferred whenever a wager is made that changes
    the highest bet (live blinds are considered a wager, antes are not).
    Inferred once per blindAnte round: when the
    first big blind is posted. It is therefore guaranteed not to be posted
    if a game is canceled because noone wanted to pay the big blind, even
    if someone already posted the small blind. In all other betting rounds it
    is inferred for each raise.
    
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_highest_bet_increase {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerPlayerWin (id: 190)

    Semantics: the player "serial" win.
    
    Direction: client <=> client
    
    Context: when a PacketPokerWin arrive from server. The packet is generated
    from PACKET_PLAYER_WIN. For each player that wins something a packet
    PlayerWin is generated.
    
    serial: integer uniquely identifying a player.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_player_win {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerBeginRound (id: 197)

    Semantics: opens a betting round for game "game_id".
    
    Direction: client <=> client
    
    Context: inferred when the client knows that a betting round will
    begin although it does not yet received information from the server to
    initialize it. Paying the blind / ante is not considered a betting
    round. It follows the :class:`POKER_END_ROUND <pokerpackets.clientpackets.PacketPokerEndRound>` packet, either
    immediatly if the server has no delay between betting rounds
    or later if the server waits a few seconds between two betting
    rounds.
    
    Example applied to holdem:
    
             state
    
             blind     END
    BEGIN    preflop   END
    BEGIN    flop      END
    BEGIN    turn      END
    BEGIN    river
             end
    
    game_id: integer uniquely identifying a game.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_begin_round {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerCurrentGames (id: 198)

    Semantics: "game_ids" contains the the list of games to 
    which the client is connected. "count" is the length of
    the "game_ids" list.
    
    Direction: client <=> client
    
    Context: inferred when the client receives a :class:`POKER_TABLE <pokerpackets.networkpackets.PacketPokerTable>` packet (for
    instance, a :class:`POKER_TABLE <pokerpackets.networkpackets.PacketPokerTable>` packet is sent to the client when a
    POKER_TABLE_JOIN was sent to the server).  The list of game ids
    contains the id matching the :class:`POKER_TABLE <pokerpackets.networkpackets.PacketPokerTable>` packet that was just
    received.
    
    Note to applications embedding the poker-network python library:
    When not in the context of a :class:`POKER_EXPLAIN <pokerpackets.networkpackets.PacketPokerExplain>` server mode,
    the packet is also inferred as a side effect of the 
    PokerExplain.packetsTableQuit method that is called by the application 
    when the user decides to leave the table.
    
    game_ids: integers uniquely identifying a game.
    count: length of game_ids.

attributes:

    game_ids: list of numbers, <length of list as unsigned char(1 byte)>[<number as unsigned int (4 bytes)>,..]
    count: unsigned char (1 byte)

### PacketPokerEndRoundLast (id: 199)

    

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_end_round_last {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerSitOutNextTurn (id: 201)

    

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_sit_out_next_turn {
    unsigned int serial;
    unsigned int game_id;
}
```

### PacketPokerShowdown (id: 204)

    

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    showdown_stack: json: <length of content as unsgined short (2 bytes)><json string>

### PacketPokerClientPlayerChips (id: 205)

    

attributes:

    game_id: unsigned int (4 bytes)
    serial: unsigned int (4 bytes)
    bet: unsigned int (4 bytes)
    money: unsigned int (4 bytes)

### PacketPokerAllinShowdown (id: 209)

    Semantics: the game "game_id" will automatically go to showdown
    
    Direction: client <=> client
    
    Context: when all players are all-in, the board cards will be
    dealt automatically. The :class:`POKER_ALLIN_SHOWDOWN <pokerpackets.clientpackets.PacketPokerAllinShowdown>` packet is created
    as soon as such a situation is detected. The client can chose
    to behave differently, for instance to postpone the display of
    the board cards until after the muck phase of the game.
    
    game_id: integer uniquely identifying a game.

attributes:

    game_id: unsigned int (4 bytes)

c example:
```c
struct packet_poker_allin_showdown {
    unsigned int game_id;
}
```

### PacketPokerPlayerHandStrength (id: 210)

    Semantics: "hand" is the human-readable description of the best
    possible poker hand the player (represented by "serial") can currently
    make in current hand being played in game, "game_id".  This
    description includes only 'made' poker hands, not draws or potential
    hands.  This description will be sent in the the language of the
    players currently set locale (see PacketPokerSetLocale()), or "en.US"
    if no translation is available.
    
    Direction: client <=> client
    
    Context: inferred on each street.
    
    serial: integer uniquely identifying a player.
    game_id: integer uniquely identifying a game.
    hand: readable player best hand.

attributes:

    serial: unsigned int (4 bytes)
    game_id: unsigned int (4 bytes)
    hand: string: <length of string as unsigned short (2 bytes)><string>
