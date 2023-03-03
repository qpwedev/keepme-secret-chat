# Telegram Secret Chat

Telegram Secret Chat is a Python project that allows for the creation of a fully protected channel for communication via Telegram chat using Diffie-Hellman key exchange algorithm and SHA-256 encryption.

## Getting Started

1. Go to the [Telegram API Portal](https://my.telegram.org/auth).
2. Login with your phone number.
3. Click on the API development tools link.
4. Click on the Create New Application button.
5. Fill in the required fields and click on the Create button.
6. Your `API_ID` and `API_HASH` will be displayed on the next page.

To get the `PEER_CHAT_ID` of a channel in Telegram, you can use the `@username_to_id_bot`. Follow these steps:

1. Send a message to the `@username_to_id_bot` to get the `PEER_CHAT_ID`.
2. The bot will send you a message with the `PEER_CHAT_ID` of the channel.

Once you have obtained the `API_ID`, `API_HASH`, and `PEER_CHAT_ID`, you can run the script with `python3 ./src/bot.py` and input them into console or use .env file.

## Inputting values directly

To input the values directly when running the script, follow these steps:

1. Open the terminal or command prompt.
1. Navigate to the root directory of the project.
1. Run the script with python3 `./src/bot.py`.
1. When prompted, input the `PEER_CHAT_ID`, `API_ID`, and `API_HASH` values.

## Using a .env file

To use a .env file, follow these steps:

1. Create a file named `.env` in the root directory of the project.
2. Define the `PEER_CHAT_ID`, `API_ID`, and `API_HASH` values in the file in the following format:

```
PEER_CHAT_ID=<your_peer_chat_id>
API_ID=<your_api_id>
API_HASH=<your_api_hash>
```

3. Save the file.

When you run the script with `python3 ./src/bot.py`, the values from the `.env` file will be automatically loaded.

## Encryption

The Diffie-Hellman key exchange algorithm is a cryptographic protocol that allows two parties to securely exchange cryptographic keys over a public channel. The protocol was invented by Whitfield Diffie and Martin Hellman in 1976 and is widely used in modern cryptography.

The basic idea behind the Diffie-Hellman key exchange algorithm is to use modular arithmetic to generate a shared secret key that can be used for encryption and decryption. The algorithm works as follows:

1. Alice and Bob agree on a large prime number `p` and a primitive root `g` of `p`.
1. Alice selects a random secret number `a` and calculates `A = g^a mod p`.
1. Bob selects a random secret number `b` and calculates `B = g^b mod p`.
1. Alice and Bob exchange `A` and `B` over the public channel.
1. Alice calculates the shared secret key `s = B^a mod p`.
1. Bob calculates the shared secret key `s = A^b mod p`.

Both Alice and Bob now have the same shared secret key, which can be used for encryption and decryption.

## Disclaimer

This project is for educational purposes only. The developers of this project are not responsible for any illegal or unethical use of the software.
