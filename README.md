# bsc-sniper-bot

I built this to grab tokens the second liquidity is added on PancakeSwap. It's tuned for speed and bypasses most of the high-level abstractions that slow down typical scripts.

## setup

1. copy `.env.example` to `.env` and fill in your keys
2. `pip install -r requirements.txt` 
3. `python -m sniper.main` 

## how it works

It polls the factory contract for `PairCreated` events. When a match is found for a token we're watching, it pushes a swap transaction immediately. I'm using a slightly higher gas tip by default to jump the queue.

Don't run this with big amounts unless you've checked the honeypot logic recently. It's basic.

## todo
- [ ] migration to websockets for lower latency
- [ ] check if token is verified on bscscan automatically
- [ ] fix the weird hang when node drops connection

license: MIT
 