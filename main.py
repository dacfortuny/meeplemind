import asyncio

from llama_index.core.agent.workflow import (
    ToolCall,
    ToolCallResult,
)
from llama_index.core.workflow import Context

from agent import agent


async def main():
    ctx = Context(agent)
    while True:
        user_msg = input("\nYou: ")

        if user_msg.lower() in {"exit", "quit", "bye"}:
            print("Bye! 🎲")
            break

        handler = agent.run(
            user_msg=user_msg,
            ctx=ctx,
        )
        async for event in handler.stream_events():
            if isinstance(event, ToolCall):
                print(f"\nCalling tool: {event.tool_name}")
                print(f"Arguments: {event.tool_kwargs}")

            elif isinstance(event, ToolCallResult):
                print(f"Tool result: {event.tool_output}")

        response = await handler

        print(f"\nMeepleMind: {response}")


if __name__ == "__main__":
    asyncio.run(main())