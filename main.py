import asyncio
import sys

from willump import Willump

# Fix windows eventloop bug
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    wllp = await Willump.start()
    friends = await (await wllp.request("GET", "/lol-chat/v1/friends")).json()

    for friend in friends:
        print(f"Deleting {friend['gameName']}")
        await wllp.request("DELETE", f"/lol-chat/v1/friends/{friend['id']}")
    await wllp.close()
    print("Deleted all friends, it could take some time to show up in the lol client.")


def confirm() -> bool:
    yes = {'yes', 'y', 'ye', ''}
    no = {'no', 'n'}
    choice = input().lower()
    if choice in yes:
        return True
    elif choice in no:
        return False
    else:
        sys.stdout.write("Please respond with 'yes' or 'no'")


if __name__ == '__main__':
    print("Please confirm the deletion of all friends")
    if confirm():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
    else:
        print("Aborted")
