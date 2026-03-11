# JTC PowerBI Automation Tool

## About this Program

This is a command line program meant to automate workflow processes on JTC's PowerBI server, that would otherwise be tedious  and time-consuming if done manually.

As of the time of writing this documentation, the only automated process is for the `Adding of Users` to `Row Level Security` and `Security` for a given project dashboard.

This program employs the use of an API requestor to send data through the PowerBI site's APIs. It also uses `time-sensitive cookies`, which can be extracted via one of
my scripts. More on that below.

### Table of Contents

## Installation

### Terminal Based Applications

As mentioned before, this is a terminal based application. Although it may seem
intimidating at first, with patience, effort and some help from ChatGPT it can
be a rather straightforward process.

First let's open the default terminal application for your operating system:

- On Windows: Press the `Windows Key`, type `Terminal` and then right click and `Run as Administrator`
- On Mac: Press `Cmd + Space`, type `Terminal` and then press `Enter`

And viola, your terminal should be open. You do not to know extensive details
about how to use the terminal and following the instructions below should get
you up and running, but just in case here are some links to help learn the
basics:

- [Windows](https://www.reddit.com/r/PowerShell/comments/17m9auw/basic_and_beginner_commands/)
- [Mac](https://www.educative.io/blog/bash-shell-command-cheat-sheet)

If not, you will likely only need to use two commands for navigation:

1. `cd`
2. `ls`

To go to your home directory use `cd ~`. To go to another directory like
`Downloads` simply use `cd Downloads`. If you are unusure of what files are in
your current directory, list them by simply typing `ls`.

### Package Managers

If this is your first time working with software on a terminal, I reccommend
using a package manager. Package managers save a lot of headache on finding the
correct website, the correct executables, and whatever else there is to find on
the internet when it comes to installing a specific piece of software. Although
intimidating at first, it makes managing software on your computer far easier.

For Windows and Mac respectively, I reccommend the following software:

- On Windows: [Chocolatey](https://chocolatey.org/install)
- On Mac: [Brew](https://brew.sh/)

For each of the package managers above, run the commands they provide on
`Terminal`.

Once installed simply run:

- On Windows: `choco install {software name}`
- On Mac: `brew install {software name}`

And your desired software from Spotify to Python, is installed with just one line![^1]

[^1]: Note that these package managers usually only support well established
    programs, so programs like this automation tool cannot be directly
installed through these package managers.

### Git and Github

`Git` is a version control system that allows you to quickly move between
current and past versions of code, mainly for the rationale of testing
different features or implementations. The code and its history is stored by
`Git` is called a repository. These repositories are then stored in a registry.
The most popular and commonly used one being `GitHub`. In some sense, `Git` can
be thought of as a storage container, while `GitHub` is the company that
manages all these storage containers.

First you need to install git: `choco install git` or `brew install git`

Since this is a private repository, before you can `clone` (or copy) this
repository you will need to login. There are various ways to login but I find
that this is the most straightforward method:

1. Download the GitHub CLI by running: `choco install gh` or `brew install gh`
2. Prompt the GitHub CLI to log you in using: `gh auth login`
3. Follow the rest of the instructions to login to GitHub

After this process, you will be able to run `git clone` on private repositories
you have access to. If you need help in cloning a repository follow the link
[here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

### Installing Docker

Normally when running a new project, the user would need to download multiple
pieces of software for the program to work properly, for this program it would
have been python, python dependencies as well as a chromedriver. However,
[`Docker`](https://docs.docker.com/get-started/) solves this issue by having
all the software mentioned pre-installed, even the operating system. So
regardless of whether you have a Windows or Mac or Linux the software should
work without any issues.

To install `Docker` run the following commands:

- On Windows: `choco install docker-desktop -y`
- On Mac: `brew install --cask docker`

If you are a windows user you will also need to run this command: `wsl
--update`. And `restart` your computer to have the updates applied.

To check that it has been installed successfully run: `docker --version`

After installing `Docker`, you also need to startup `Docker Desktop` so that it
is running in the background. To do so run: `docker desktop start`. Feel free
to close the application after it has loaded, it should still continue running
in the background so long as you have not restarted your compter.

### Excel

The final pre-requisite that is good to have is Microsoft Excel. This will be
helpful in editing CSV files that will be used to create the correct
configurations.

## Post-Installation

>[!IMPORTANT]
>If you are on `Windows`, before starting, run this command in the terminal to
enable `Powershell` to run scripts: `Set-ExecutionPolicy RemoteSigned`  
>Alternatively, you can download Anaconda (https://www.anaconda.com/download) and use `Anaconda Powershell Prompt` to run scripts, in place of the regular `Powershell`

### Clone GitHub Repository
Before running the subsequent steps, remember to clone the github repository by running the following script.

`git clone <HTTPS link of the repository from github>`

### Pulling Docker Images

Images are essentially the program, its dependencies and the operating system
in one file. To download the necessary images onto the system, a script has
been provided for you. Simply run the following script while in the `root` of
your program and wait for the images to be installed: 

- On Windows: `.\scripts\powershell\pull.ps1`
- On Mac: `./scripts/bash/pull.sh`

### Retrieving Cookies

As mentioned above, before we can properly use the APIs, we need the correct
time-sensitive cookies. These cookies will expire after around 1 hour, so it
will be necessary to redo this step from time to time. For retrieving cookies,
a script has also been created to facilitate this.

Run this script while in `root`:

- On Windows: `.\scripts\powershell\cookies.ps1`
- On Mac: `./scripts/bash/cookies.sh`

You will notice that halfway through, the program will prompt you with the
following message:
```
Please enter a valid token :
```

Here is where you should paste the `token` generated by the TokenGenerator in the AWS Console instance. If you don't know what that is, refer to the file titled
`"JTC OPTIMUS v2.0 - Admin Training (PowerBI Configuration).pdf"`, found [here](docs/JTC%20OPTIMUS%20v2.0%20-%20Admin%20Training%20(PowerBI%20Configuration).pdf) in the `docs` folder.

After this process is complete, your cookies will now have been updated and you can proceed to the next step.
Close the `localhost` page and return to your terminal.

### Adding Users to Row Level Security and Security

Before running the script to add users, you should first configure the input data,such as **user emails**, their **assigned roles** and **which project dashboard** they will be added for.
All input data will be placed in the CSV files in `/data/csv`. Detailed explanations of how to configure the fields can be found in the [User Guide](USERGUIDE.md).

After the CSVs are done, run the script while in `root`:

- On Windows: `.\scripts\powershell\api.ps1 configure`
- On Mac: `./scripts/bash/api.sh configure`

The "configure" at the end is an argument passed, to tell the program to perform the flows relevant to "configure mode".
Since as of the time of writing there are no other automated processes besides adding of users to row level security and security, this is the only mode.

Just like that, the specified users will have been added to Row Level Security and Security for the specified project dashboard, all according to your inputs in the CSVs.

### Commonly faced problems

If the script to add users fails, it could likely be for any of the following reasons...

1. User's email already added  
If the user's email was already added to row level security/security for that project, you will see something like "Error 409: failed to add user".

2. User's email does not exist within JTC PowerBI database  
Even when done manually, you cannot add a user with a non-JTC email to any project's row level security/security.

3. Cookies expired  
Like said before, cookies are time-sensitive. If the script terminates basically from the start, it probably means the cookies have expired. Run the cookie extraction script again to extract them again.

4. Non-existent project/roles indicated in input  
Of course, the program can't add users to projects that don't exist, or roles within them that don't exist. Check your input data carefully.

Final reminder to leave Docker running before running any of the scripts.