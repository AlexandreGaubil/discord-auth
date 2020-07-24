# Discord Auth

This Discord Bot allows you to whitelist certain people (by email address) to ensure they are the only ones that can access your Discord Guild.

## Features

* Verifies the identity of users through their provided email address using one-time codes
* Automatically assigns validated users a new role (e.g., "Member") to allow them access to the rest of the server

## Usage

This requires Python 3.7 or higher. Make sure that `pip` is installed as well.

Start by installing [discord.py](https://pypi.org/project/discord.py/) by running:

```console
$ pip install discord.py
```

You also need to install [smtplib](https://docs.python.org/3/library/smtplib.html) by running:

```console
$ pip install smtplib
```

Duplicate the file named `setup_info.json.template`, rename it to `setup_info.json`, duplicate the file named `authorized_users.json.template` and rename it to `authorized_users.json`.

Create a new application in [Discord's developer portal](https://discord.com/developers/). Copy the Discord token of your bot and set it as the value of `discord_bot_token` in the `setup_info.json` file.

Copy the ID of your Guild from Discord and set it as the value of `discord_guild_id` in the `setup_info.json` file. Copy the ID of the welcome channel (a channel on your server where @everyone has access) and set it as the value of `discord_welcome_channel_id` in the `setup_info.json` file. Copy the ID of the Role you want assigned to the validated users and set it as `discord_role_to_assign_id` in the `setup_info.json` file.

In order to make sure that only authenticated users have access to your Discord, change the permissions of @everyone in Discord to off for all options.

Set the `email_address`, `email_password`, `email_smtp_server` and `email_port` in `setup_info.json`. The defaults are for a Gmail account. These are used to send the authentication email.

If you want to ask the user to use a specific kind of email address (e.g., a work email or a university email), set the value of `email_type_specifier` in the `setup_info.json`. Otherwise, leave it blank.

Finally, set the value of `authorized_users` in the file `authorized_users.json` to the list of emails you want the bot to authorize access to your Discord. Separate the emails by a comma (i.e., ',').

Now, open a terminal, `cd` into the directory where the project is and type:

```console
$ python3 main.py
```

## Contributing

Any contributions are welcome! Take a look at the [Issues](https://github.com/AlexandreGaubil/discord-auth/issues) or, if you have features you want to implement, go ahead and make a suggestion!

Discord Auth follows the standard fork/commit/pull request process. To contribute changes:
1. Fork and clone the repository,
2. Commit your changes,
3. **Test your changes**,
4. Push them to your repository,
5. Make a pull request against the `master` branch.

##  License

Copyright 2020 Alexandre Gaubil.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.