import asyncio
import os
from pyrogram import Client
from crypto import calculate_shared_secret, generate_key, validate_public_key, p, g
from pyrogram import enums
from pyrogram.types.messages_and_media.message import Message
from encryption import decrypt_message, encrypt_message, generate_key_by_passphrase
import aioconsole
from dotenv import load_dotenv
load_dotenv()

SHARED_SECRET = None


PEER_CHAT_ID = int(os.getenv("PEER_CHAT_ID")) if os.getenv(
    "PEER_CHAT_ID") else input("Enter your PEER_CHAT_ID: ")
API_ID = int(os.getenv("API_ID")) if os.getenv(
    "API_ID") else input("Enter your API ID: ")
API_HASH = os.getenv("API_HASH") if os.getenv(
    "API_HASH") else input("Enter your API HASH: ")


async def get_last_messages(app: Client, limit: int) -> Message | None:
    """
    Get last messages from peer. Return list of messages.
    """

    global PEER_CHAT_ID
    last_messages = []
    async for message in app.get_chat_history(PEER_CHAT_ID, limit):
        last_messages.append(message)

    return last_messages


def get_public_key_from_message(message: Message) -> int:
    """
    Get public key from message. Return public key.
    """

    public_key = int(
        message.text
        .split("\n\n")[1]
        .split("</code>")[0]
    )

    validate_public_key(p, public_key)

    return public_key


def get_shared_secret(a1_private_part_key: int, b1_public_key: int) -> bytes:
    """
    Calculate shared secret from private part key and public key.
    """

    shared_secret = calculate_shared_secret(
        p, a1_private_part_key,
        b1_public_key
    )

    return shared_secret


async def waiting_for_public_key(app: Client) -> int | None:
    """
    Waiting for public key from peer. Return public key if received, else return None.
    """

    loading_amination = ["|", "/", "-", "\\"]

    attempt = 0
    while attempt < 60 * 5:
        last_message = (await get_last_messages(app, 1))[0]

        if last_message and last_message.text and last_message.text.startswith("[N2] Public key:"):
            b1_public_key = get_public_key_from_message(last_message)

            return b1_public_key

        print(
            f"Waiting for public key... {loading_amination[attempt % len(loading_amination)]}", end="\r"
        )

        await asyncio.sleep(1)
        attempt += 1

    print("Timeout")


async def establish_connection(app: Client, a1_private_part_key: int, a1_public_key: int) -> bool:
    """
    Establish connection with peer. Return True if connection established, else return False.
    """

    global SHARED_SECRET
    last_message = (await get_last_messages(app, 1))[0]

    if not last_message or not last_message.text or not last_message.text.startswith("[N1] Public key:"):
        await app.send_message(
            PEER_CHAT_ID,
            f"<b>[N1] Public key</b>:\n\n<code>{a1_public_key}</code>", parse_mode=enums.ParseMode.HTML
        )

        b1_public_key = await waiting_for_public_key(app)

        shared_secret = get_shared_secret(
            a1_private_part_key,
            b1_public_key
        )

        SHARED_SECRET = shared_secret

        print("Shared secret:", SHARED_SECRET.hex())
        print("Connection established!")
        return True
    elif last_message.text.startswith("[N1] Public key:") and last_message.from_user.id == PEER_CHAT_ID:
        b1_public_key = get_public_key_from_message(last_message)

        shared_secret = get_shared_secret(
            a1_private_part_key,
            b1_public_key
        )

        SHARED_SECRET = shared_secret

        await app.send_message(
            PEER_CHAT_ID,
            f"<b>[N2] Public key</b>:\n\n<code>{a1_public_key}</code>", parse_mode=enums.ParseMode.HTML
        )

        print("Shared secret:", SHARED_SECRET.hex())
        print("Connection established!")
        return True
    else:
        print("Something went wrong")
        return False


async def message_getting_routine(app: Client, last_message_id: int, key: bytes):
    """
    Message getting routine.
    Gets messages from peer and prints them to console.
    """

    last_read_message_id = last_message_id
    while True:
        last_messages = await get_last_messages(app, 6)

        for message in last_messages:
            if message.id > last_read_message_id and message.from_user.id == PEER_CHAT_ID:
                # try:
                message_text = decrypt_message(message.text, key)
                print("• " + message_text)
                # except Exception as e:
                #     print(e)

                last_read_message_id = message.id

        await asyncio.sleep(1)


async def message_sending_routine(app: Client, key: bytes):
    """
    Message sending routine. 
    Gets message from user and sends it encrypted to peer.
    """

    while True:
        message = await aioconsole.ainput()

        message = encrypt_message(message, key)

        await app.send_message(
            PEER_CHAT_ID,
            message
        )


async def start_chat(app: Client) -> None:
    """
    Start chat with peer
    """
    global SHARED_SECRET

    key = generate_key_by_passphrase(SHARED_SECRET)

    last_read_message_id = (await get_last_messages(app, 1))[0].id

    message_getter = asyncio.create_task(
        message_getting_routine(app, last_read_message_id, key)
    )

    message_sender = asyncio.create_task(message_sending_routine(app, key))

    print("Chat started!")
    await asyncio.gather(message_getter, message_sender)


async def main():
    """
    Main function
    """

    a1_private_part_key, a1_public_key = generate_key(p, g)
    validate_public_key(p, a1_public_key)

    async with Client("my_account", API_ID, API_HASH) as app:
        await establish_connection(
            app,
            a1_private_part_key,
            a1_public_key,
        )

        await start_chat(app)


asyncio.run(main())
