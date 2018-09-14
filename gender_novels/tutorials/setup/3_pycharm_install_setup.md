# PyCharm Installation and Setup

In the Digital Humanities Lab, we'll be using the PyCharm IDE from JetBrains.

An IDE or **I**ntegrated **D**evelopment **E**nvironment gives you the ability to write, run, test, and lint code all in one place. The PyCharm interface looks like this:

![PyCharm IDE interface](../images/pycharm_1.png)

By standardizing the IDE across the lab, we hope to facilitate collaboration and standardize support. This tutorial will walk you through installation and setup of PyCharm.


## Installation

As students with a `.edu` email address, you can get PyCharm for free by [signing up for an educational account](https://www.jetbrains.com/student/).


Once you have signed up for an account, you will receive an email activation to confirm your email. When you click on the link you will be able to download PyCharm among other JetBrains offerings.

![JetBrains Student Installation Page](../images/pycharm_2.png)

Alternately you can download PyCharm through this [direct link](https://www.jetbrains.com/pycharm/download/) — be sure to get the Professional Edition.

![PyCharm Installation](../images/pycharm_3.png)

The installation process differs slightly between Mac and Windows but you can select the default settings in both cases.

## Initialization
Once the installation process is finished, open up the PyCharm application. This
will open up an activation screen. You can activate PyCharm by entering the email
and password that you used before to sign up for a Jetbrains account.
![](../images/pycharm_activation_1.png)

Next, you will get to a setup menu.

In the first window, select "Do not import settings". We'll import settings at a
later stage.
![](../images/pycharm_init_1.png)

(Mac only)
Select the Mac OS X 10.5+ keymap

![](../images/pycharm_init_2.png)


Select either the dark ("Darcula") or Light theme. (Note: you might have
to set it again later after you import )
![](../images/pycharm_init_3.png)


Don't create a launcher script--leave the checkbox empty.
![](../images/pycharm_init_4.png)


Click on the buttons to install Markdown and BashSupport.
![](../images/pycharm_init_5.png)

Once the setup is finished, you will be greeted by the screen below. Select "Open"
to select the existing gender_novels repo.
![](../images/pycharm_init_6.png)

Select the path to your gender_novels repo (in my case: ~/code/gender_novels)
![](../images/pycharm_init_7.png)

This will bring up the main PyCharm window with the loaded gender_novels directory
on the left.
![](../images/pycharm_config_1.png)

## Configuration

Next, we're going to import the DH Lab PyCharm settings. First
[download the settings file.](https://github.com/dhmit/gender_novels/raw/master/gender_novels/tutorials/setup/pycharm_settings.jar)
Then, go to file, "Import Settings..."
![](../images/pycharm_config_2.png)

Import all components.
![](../images/pycharm_config_3.png)

As a final step, we'll change some configuration settings.

On Mac, select PyCharm -> Preferences, On Windows File -> Settings
![](../images/pycharm_config_4.png)


Under "Appearance & Behavior" -> Appearance, you can select either the dark
"Darcula" theme or the "Light" theme.
![](../images/pycharm_config_5.png)

Then, you need to configure your Python interpreter under "Project: gender_novels"
-> Project Interpreter. Click on the wheel in the top right and select "Add".
![](../images/pycharm_config_6.png)

Select "Existing environment" and click on the "..." to the right.
![](../images/pycharm_config_7.png)

Here, you need to navigate to the environment directory of
gender_novels Python environment that you had
First, you need to navigate to the directory of the gender_novels Python
environment that you had set up in the "Install Python 3" tutorial. From
there, you select the python executable in the bin folder. So the full path is
`<environment_directory>/bin/python`.
![](../images/pycharm_config_8.png)

Back in the main menu, click "Apply" to activate the updated settings.
![](../images/pycharm_config_9.png)

Congratulations. You're now done with the PyCharm installation and configuration.
