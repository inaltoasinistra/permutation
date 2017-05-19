permutation
===========
Hide your seed in a deck of cards and don't worry

$ permutation --sep , encode
BIP39 seed: tragedia malinteso attorno lacuna invece michele produrre vispo
            brillante buio valgo umano
Insert the password: passw0rd
Confirm the password: passw0rd

5♠,10♠,3♥,Q♠,3♦,K♥,Q♦,4♣,6♣,A♥,6♥,10♥,8♥,5♥,3♠,J♠,5♣,6♠,4♦,4♥,10♣,6♦,A♠,9♦,K♣,
2♥,9♥,7♠,8♠,A♦,A♣,J♥,7♦,J♦,9♠,K♦,J♣,10♦,Q♥,4♠,9♣,8♣,7♥,3♣,5♦,2♠,7♣,8♦,K♠,2♣,2♦,
Q♣

$ permutation --language italian --sep , decode
Cards permutation: 5♠,10♠,3♥,Q♠,3♦,K♥,Q♦,4♣,6♣,A♥,6♥,10♥,8♥,5♥,3♠,J♠,5♣,6♠,4♦,
4♥,10♣,6♦,A♠,9♦,K♣,2♥,9♥,7♠,8♠,A♦,A♣,J♥,7♦,J♦,9♠,K♦,J♣,10♦,Q♥,4♠,9♣,8♣,7♥,3♣,
5♦,2♠,7♣,8♦,K♠,2♣,2♦,Q♣
Insert the password: passw0rd
Confirm the password: passw0rd

tragedia malinteso attorno lacuna invece michele produrre vispo brillante buio
valgo umano


Install
¯¯¯¯¯¯¯
pip install -r requirements.txt
python setup.py install
