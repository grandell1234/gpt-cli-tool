# gpt-cli-tool
A versatile CLI tool for managing and interacting with OpenAI chat sessions, including saving, loading, and copying conversations.
___
### How to install:
Run this command to download the CLI:

```$ git clone https://github.com/grandell1234/gpt-cli-tool.git ```

Move into the correct folder with this:

```$ cd gpt-cli-tool```

Install dependencies:

```$ pip3 install openai```

```$ pip3 install pyperclip```

You are now ready to use it by running:

```$ python3 cli.py```
___
### Setup API Keys
If you already have an API key setup in environment variables, you can skip to Instructions for use. Otherwise, you will need to open up the file in your favorite IDE where there are instructions for setting it up with an API key at the top of the file.
___
### Instructions for use:

When you boot it up with ```$ python3 cli.py``` the help menu appears which contains all the commands you can use with it:

![Screenshot 2024-05-27 at 10 11 36 AM](https://github.com/grandell1234/gpt-command-line-tool/assets/78573365/b8229999-2689-4639-b3d7-81229cf76ab2)

Some commands contain aliases such as ```?exit``` working like ```?quit```.

You can do ```?copy all``` to copy the entire conversation
___
Sample Conversation:

![Screenshot 2024-05-27 at 10 12 59 AM](https://github.com/grandell1234/gpt-command-line-tool/assets/78573365/715f774b-c6be-439e-b0c0-7ce1466d2c9e)

When saving conversations you can give it a name you want or it will use GPT-3.5-Turbo to generate a name for you.

![Screenshot 2024-05-27 at 10 14 44 AM](https://github.com/grandell1234/gpt-command-line-tool/assets/78573365/cae59f0a-7fbe-47ab-ad5f-a537a585aad2)

This tool makes it super easy to switch out models or to save a conversation and then branch it into two separate discussions that go separate ways or that use different models.

![Screenshot 2024-05-27 at 10 16 17 AM](https://github.com/grandell1234/gpt-command-line-tool/assets/78573365/7bc95bb2-8f38-4866-b689-9d997cc44df8)
___
