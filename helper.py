"""
A command-line Python tool powered by OpenAI's models that suggests and runs `zsh` commands based on user-prompted tasks.

Note: once the command is executed succesfully, the program exists by showing you the output
"""
import os
from openai import OpenAI
import subprocess


client = OpenAI()


# Ensure OpenAI API key is loaded from the environment
client.api_key = os.getenv("OPENAI_API_KEY")

if not client.api_key:
    print("Error: OpenAI API key not found. Please set the 'OPENAI_API_KEY' environment variable.")
    exit(1)

def get_llm_command(task_description):
    """Uses OpenAI GPT to suggest a zsh-compatible command."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that suggests zsh-compatible commands for tasks."},
                {"role": "user", "content": f"Task: {task_description}\nSuggest a zsh command to accomplish this."}
            ],
            max_tokens=100,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def get_error_suggestion(command, error_message):
    """Gets suggestions from ChatGPT to debug the error."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a troubleshooting assistant for zsh commands."},
                {"role": "user", "content": f"I ran the following command:\n\n{command}\n\nIt failed with the following error:\n\n{error_message}\n\nCan you help debug this issue and suggest a fix?"}
            ],
            max_tokens=200,
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error while getting suggestions: {e}"

def main():
    print("Welcome to the LLM Command Line Helper!")
    print("Type 'exit' to quit.")
    while True:
       
        task_description = input("\nWhat would you like to do today with bash? ")
        if task_description.lower() == "exit":
            print("Bye, See you later!")
            break
        
        #LLM suggestion
        suggested_command = get_llm_command(task_description)
        print(f"\nSuggested Command: {suggested_command}")

        # Get user approval
        user_input = input("Do you want to run this command? (yes/no): ").strip().lower()
        if user_input == "yes":
            try:
                print("\nExecuting command in zsh...")
                # Run the command in zsh
                result = subprocess.run(
                    ["zsh", "-c", suggested_command],
                    text=True, capture_output=True, check=True
                )
                print("\nCommand Output:")
                print(result.stdout)
                if result.stderr:
                    print("\nError Output:")
                    print(result.stderr)
            except subprocess.CalledProcessError as cmd_error:
                print(f"\nThe command failed with return code {cmd_error.returncode}: {cmd_error}")
                print("\nFetching suggestions to debug the error...\n")
                suggestion = get_error_suggestion(suggested_command, cmd_error.stderr)
                print(f"Suggestion from ChatGPT:\n{suggestion}")
                
                # Ask user to input one of the suggested commands
                while True:
                    retry_command = input("\nPlease type a corrected command based on the suggestions: ").strip()
                    if retry_command.lower() == "exit":
                        print("Goodbye!")
                        return
                    try:
                        print("\nRetrying command in zsh...")
                        result = subprocess.run(
                            ["zsh", "-c", retry_command],
                            text=True, capture_output=True, check=True
                        )
                        print("\nCommand Output:")
                        print(result.stdout)
                        if result.stderr:
                            print("\nError Output:")
                            print(result.stderr)
                        break  # Exit retry loop after successful execution
                    except subprocess.CalledProcessError as retry_error:
                        print(f"\nRetry failed with return code {retry_error.returncode}: {retry_error}")
                        print("\nYou can try another corrected command or type 'exit' to quit.")
                    except Exception as retry_exception:
                        print(f"An unexpected error occurred during retry: {retry_exception}")
            except Exception as general_error:
                print(f"An unexpected error occurred: {general_error}")
        elif user_input == "no":
            print("Command rejected. Let's try again.")
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

if __name__ == "__main__":
    main()
