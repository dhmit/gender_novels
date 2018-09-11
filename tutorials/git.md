# Git Tutorial

This tutorial presupposes that you have set up git, Github, and Github
Desktop as described in the
[setup tutorial.](https://github.com/dhmit/gender_novels/blob/devbranch/tutorials/setup.md)

#### Overview

The problem with git is that it is too powerful and gives you too many options
and comes with a vocabulary of its own, filled with pushes, pulls, merges, and
branches. 

![](https://imgs.xkcd.com/comics/git.png)

This tutorial isn't a deep dive into the curious world of git. What it covers
are only the essential parts that you need to know to work in the DH Lab. To
make your and our life easier we also won't cover git's command line interface
and only look at the Github Desktop GUI (It's generally easier to make mistakes
with a command line because the GUI will usually ask you multiple times if 
you are sure that you want to delete your work.)


#### General Outline: Local, Remote, and Upstream

In every project, we will work with three different versions of the same 
repository. You have already worked with all of them during the setup process. 

![](images/git_init_1.png) 
First, there is the 
[master repository](https://github.com/dhmit/gender_novels)
on Github. It contains the authoritative current version of our project. It is
also the repository that we all contribute our documented and tested code to.

![](images/git_init_2.png) 


Second, there is your personal fork of the project on Github. When you set it 
up, this fork was an exact copy of the upstream master repo. However, the fork
is created, this repo is under your control and you can use it to stage changes
before submitting them to the upstream master.

![](images/git_init_3.png) 

Third, there is the clone of the project on your local computer. This is the 
version that you'll actually be working with. Again, this local repository 
starts out as an exact copy of your remote fork but once you start coding, 
you will make changes to this repository that are independent of both your 
Github fork and the upstream master.

#### Workflow: Code Pushes and Pull Requests

#### Code Pushes and Pull Requests


#### Branches