permutation
===========
Hide your seed in a deck of cards.

`permutation` encodes wallets seed into permutations of decks of cards.
Are supported BIP39 wordlists but the BIP39 checksum is not used, in
order to support all the HD wallets.

`permutation` supports encryption through the
[xxtea](https://en.wikipedia.org/wiki/XXTEA) algorithm.
It was chosen because it has a low overhead.

The purpose of `permutation` is provide plausible deniability, so effort
was spent to avoid to reveal any information without the user password.
A deck of cards ordered with `permutation` should be undistinguished
from a shuffled deck of cards.

A said *should* because this software is experimental and not ready to
protect real wallets. I would appreciate testing and code review.

$ permutation --sep , encode
BIP39 seed: tragedia,malinteso,attorno,lacuna,invece,michele,produrre,
            vispo,brillante,buio,valgo,umano
Insert the password: passw0rd
Confirm the password: passw0rd

9♠,A♣,10♥,2♥,4♦,K♣,10♣,J♥,6♠,5♦,5♣,7♠,9♣,★,3♣,6♦,8♥,☆,J♠,10♦,A♥,4♣,J♣,A♦
,K♦,5♠,5♥,K♥,7♥,Q♣,3♠,8♣,3♦,3♥,7♦,A♠,K♠,2♦,2♠,Q♠,6♥,7♣,6♣,Q♥,8♠,10♠,4♥,
Q♦,8♦,9♦,2♣,J♦,9♥,4♠

$ permutation --language italian --sep , decode
Cards permutation: 9♠,A♣,10♥,2♥,4♦,K♣,10♣,J♥,6♠,5♦,5♣,7♠,9♣,★,3♣,6♦,8♥,☆
,J♠,10♦,A♥,4♣,J♣,A♦,K♦,5♠,5♥,K♥,7♥,Q♣,3♠,8♣,3♦,3♥,7♦,A♠,K♠,2♦,2♠,Q♠,6♥,
7♣,6♣,Q♥,8♠,10♠,4♥,Q♦,8♦,9♦,2♣,J♦,9♥,4♠
Insert the password: passw0rd
Confirm the password: passw0rd

tragedia,malinteso,attorno,lacuna,invece,michele,produrre,vispo,
brillante,buio,valgo,umano


Install
-------
pip install -r requirements.txt
python setup.py install
