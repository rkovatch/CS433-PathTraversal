# CS 433/533 Path Traversal Demo
## What is path traversal?
[Path traversal](https://owasp.org/www-community/attacks/Path_Traversal) is a common software exploit that attackers can
take advantage of to gain arbitrary read/write abilities on a filesystem. It involves strategically using dot-dot ("..")
to reference parent directories and traverse out of the usual scope of a program's filesystem access. If a program does 
not account for dot-dots in file paths, it may mistakenly assume that it is writing to a valid directory when it is in 
fact not. This is an especially big risk when file paths are user-provided.

## What is this app?
This is a web application mimicking a social media site which contains a photo upload function that is vulnerable to
path traversal. The goal is to demonstrate how simple of an exploit it is while also showing how grave of an impact it
can have. Included is a Python script which exploits the path traversal vulnerability and injects a credential stealer 
on the home page of the app (TODO).

## Usage
The application is a multi-container setup orchestrated with Docker Compose. You can learn how to install that 
[here](https://docs.docker.com/compose/install/). Before bringing up the app for the first time, we need to set a secret
key in the environment that's used to compute login session keys: `export SECRET_KEY=<key goes here>`. Then you can run 
`docker compose up -d` from the project's main directory to bring up the web server and MongoDB instance (which stores 
the users and posts on the site).

The web app should then be accessible at http://localhost:5001. You will be prompted to log in. There are three user
accounts defined in `database/seeder.py`:
- `admin` / `banana`: the admin user account (can delete posts by any user).
- `bobby` / `hunter2`: a regular user account (can only delete its own posts).
- `alice` / `passw0rd`: another regular user account (can only delete its own posts).

The vulnerable photo upload function can be accessed by clicking "Edit profile" in the sidebar. Uploading a photo there
will update the current user's profile picture and save the uploaded photo to the `photos` directory. This is where the
vulnerability lies: when a photo is uploaded, the client sends its filename along with the data, and the server blindly
trusts this field when writing to disk. If a client modifies the filename to contain `..`, they can write that file to
any arbitrary directory. Additionally, the server does not check filetypes, so any type of file can be uploaded as a 
user's profile picture. This grants arbitrary write privileges to the web root.

To read arbitrarily, a vulnerable `get_photo` API is provided. It is even simpler to exploit: just craft a URL like 
http://localhost:5001/get_photo?file=../web_server.py. Now, with read and write privileges, we can make any number of 
changes to the application's files remotely while it runs.

TODO: credential stealer usage

## How can I prevent path traversal vulnerabilities?
The best way is to not accept any user input at all when handling file paths. The vulnerability in this app would be
fixed if we completely ignored the provided filename and generated one based on the user's unique ID in the database,
keeping only the extension. This way, we'd know it could only be written to the `photos` directory. There are also other
options:
- Use built-in or external libraries to "normalize" file paths. These functions parse file path strings and collapse 
dots and dot-dots to produce paths that only travel downward. They can eliminate dot-dots at the beginning of paths to
prevent traversing upward in the filesystem.
- Use a CDN for user-uploaded content. This creates valuable separation between your web server and potentially unsafe
uploads. If file traversal were to happen on your CDN, it might only affect other static files -- not your source code.
- Restrict the read/write access of your program at the operating system level by running it in a sandbox of some kind.

## Attribution
Google's experimental Gemini 2.0 Flash Thinking 01-21 model was used to generate static HTML templates and CSS 
stylesheets to serve as a starting point for the project. Prompt information is available as comments in the HTML
templates, which can be found in the `templates` folder. All functional parts, including the entire Flask web server and
all of its components, are the authors' own work. Our use of the Netflix avatar constitutes fair use for educational
purposes.