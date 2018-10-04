# Introduction to the Command Line

The command line or terminal environment is widely used by SysAdmins, software developers, and other engineers as this interface provides them with greater access and control over their machines. As William Shotts notes in *[The Linux Command Line](http://linuxcommand.org/tlcl.php)*, "graphical user interfaces make easy tasks easy, while command line interfaces make difficult tasks possible." In addition to making it possible to perform complex tasks, a command line interface provides users with the ability to automate tasks and is commonly used to access remote servers.

In this guide, we'll go through some common commands to familiarize yourself with the terminal environment. We'll assume a UNIX-like system; Windows users should run PowerShell as an administrator to be able to use similar commands.

## pwd

The `pwd` command is used to show the current working directory. It stands for **p**rint **w**orking **d**irectory.

```
pwd
```

When you press enter following this command, you will receive output that prints out where you currently are in your system:

```
/Users/your-user-name
```

With this feedback, you should now know what directory you're currently accessing from the terminal.

## ls

The `ls` command is used to *list* the contents of the current directory:

```
ls
```

When you run this command, you may see output like the following:

```
Applications
Desktop
Documents
Downloads
Library
Movies
Music
Pictures
Public
```

This shows all the directories you have within your working directory (the directory you're currently in).

You can use some flags with `ls` to receive more information about the files available.

For example, `ls -l` will show ownership and read/write permissions of files:

```
ls -l
```

```
drwx------    4 user-name  staff      136 Jul 18  2016 Applications
drwx------+ 414 user-name  staff    14076 Sep 28 12:59 Desktop
drwx------+  26 user-name  staff      884 Sep 18 13:40 Documents
drwx------+ 789 user-name  staff    26826 Oct  4 00:36 Downloads
```

You can read more about access rights and what the letters mean in [this tutorial](http://www.ee.surrey.ac.uk/Teaching/Unix/unix5.html).

The `-a` flag with `ls` will show you invisible files that typically contain settings or data for programs to run as expected. Hidden files begin with a `.`.

```
ls -a
```

In addition to seeing hidden files below, you'll also see `.` and `..` that show relative paths — `.` is the current working directory and `..` refers to the directory that is a level up from the current one.

```
.
..
.ansible
.bash_history
.bash_profile
...
Applications
Desktop
Documents
...
```

(Above, the `...` is being used as an ellipses and will not appear on your terminal.)

You generally will not need to access hidden files, but there are occasions when you may need to manually edit settings (with great power comes great responsibility).

## cd

The `cd` command stands for **c**hange **d**irectory. To execute the command you will need to pass the path or relative path to a directory to the command, as in:

```
cd directory-name
```

From the user directory that we have shown above, we can `cd` into the `Documents` directory like so:

```
cd Documents
```

Note that for Windows and Mac terminal interfaces, file naming conventions are not case sensitive.

Now, when you type `pwd`, you should see the following output:

```
/Users/your-user-name/Documents
```

To move up a directory (in this case to the previous one), you can use `..`:

```
cd ..
```

Now you will be back in your user's main directory.

You can always return to your user's main directory with the following command:

```
cd ~
```

You can also always move into the primary root directory by using `/` with `cd`:

```
cd /
```

If you run the `ls` command in this directory, you should see files like this:

```
Applications			bin				private
Library				dev				sbin
Network				etc				tmp
System				home				usr
var 				Users				net
Volumes				opt
```

Practice navigating around your file system with the commands you have learned so far.

## Autocompletion and History

Versions of the command line allow you to autocomplete and to reuse commands easily.

Try typing the first few letters of a directory you would like to `cd` into, and then press the `TAB` key to autocomplete the directory name.

Press the `UP` arrow to cycle through the previous commands you have already run.

You can also summon the entire history of this session:

```
history
```

Here you should see all the commands you have run since opening the terminal window.

## Connecting to a Server

You can connect to a remote server or computer through the terminal. To do so, you'll be using the `ssh` command, which stands for **S**ecure **S**ocket **S**hell. You'll need to have a user on the server and to know the user's password or have an SSH key to connect.

To initialize the connection, you will use the following format:

```
ssh user-name@ip-address
```

The IP address will be a series of numbers that will direct you to the correct server.

If you do not have an SSH key, you'll be prompted for a password. When you type the password in, you won't have any visual feedback of your keystrokes. When you are done typing your password, press the `ENTER` key.
