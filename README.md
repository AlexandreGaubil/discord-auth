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

Finally, set the value of `authorized_users` in the file `authorized_users.json` to the list of emails you want the bot to authorize access to your Discord. Separate the emails by a comma (i.e., `,`). Add, after each email, `: []`.  You can set a list of additional roles to give to this particular user instead of the role `discord_role_to_assign_id`.

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
