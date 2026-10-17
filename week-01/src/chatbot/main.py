from typing import List

from src.chatbot.models import ChatMessage
from src.chatbot.api import create_client, get_chat_response, create_system_message
from src.chatbot import ui
from src.settings import settings


def should_quit(user_input: str) -> bool:
    quit_commands = {"quit", "exit", "bye", "goodbye"}
    return user_input.strip().lower() in quit_commands


def run_conversation_loop() -> None:
    client = create_client()

    conversation_history: List[ChatMessage] = [create_system_message()]

    ui.display_welcome()

    while True:
        try:
            user_input = ui.get_user_input().strip()

            if should_quit(user_input):
                ui.display_goodbye()
                break

            if not user_input:
                ui.display_error("Please enter a message!")
                continue

            user_message = ChatMessage(role="user", content=user_input)

            ui.display_loading()

            assistant_message = get_chat_response(
                client, conversation_history + [user_message], settings.OPENAI_MODEL
            )
            conversation_history.append(user_message)
            conversation_history.append(assistant_message)
            ui.display_assistant_message(assistant_message.content)

        except KeyboardInterrupt:
            ui.display_goodbye()
            break
        except EOFError:
            ui.display_goodbye()
            break
        except Exception as e:
            ui.display_error(f"An error occurred: {e}")
            continue


def main() -> None:
    try:
        run_conversation_loop()
    except KeyboardInterrupt:
        print("\n")
        ui.display_goodbye()
    except Exception as e:
        ui.display_error(f"Fatal error: {e}")
        ui.display_system_message(
            "Please check your configuration and try again.", "red"
        )


if __name__ == "__main__":
    main()
