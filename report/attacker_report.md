# Security Mini Project - Attacking

- [Security Mini Project - Attacking](#security-mini-project---attacking)
  - [Information Gathering](#information-gathering)
  - [Initial Access](#initial-access)
  - [Privilege Escalation](#privilege-escalation)
  - [Security Goal Violations](#security-goal-violations)
  - [Maintaining Access](#maintaining-access)

## Information Gathering

The first thing we did was to explore the website to figure out if we could find any apparent vulnerabilities.
The steps taken to do this were to create a user and try using every possible button and input field to see if it was possible to get access.
When inputting values in the different input fields, we noticed that the import note could only take numbers and no strings with the exception of it being able to also take a single character. We thought this was a bit out of the ordinary. Therefore, we tried playing with inputting different characters, but it had no effect.
Our next steps were to use the developer tools in a browser to inspect the HTML. We did this to explore any forgotten or unwanted elements that we could exploit. 
We found that on the main page there was a hidden input field with some weird text as a placeholder:

![Image showing a weird input field that could be exploited.](images/Weird_input_field_that_was_hidden_but_looked_like_we_could_exploit.png)

We also found that if you input something in this input field and press enter you submit a form based on what is written in the input field.
We looked into the placeholder as it looked odd to us and figured out that it was written in the language `brainfuck`. And when pressing enter it open an alert that uses the following format:

```
Input:
Translated to command:
Output of command:
```

We first attempted to use the placeholder as an input which translated to `Godt det ikke er os, held og lykke!` and had no output. This suggested that the input gets translated to brainfuck and is then run on the command line(maybe as part of a command). We then tried inputting the command `whoami` as `brainfuck`. (To translate whoami to `brainfuck` we used a `brainfuck` interpreter on the internet) And in the `output of command` field it returned: `student`.
Which told us that we through this input field could write commands on the command line as the user `student` .

## Initial Access

After figuring out that the input field’s translation was run on the server as a shell-command, we had to convert this to actual full shell access. Since we were receiving the text output of our commands we could, albeit tediously, do a quick look around just using `ls`. Doing for example `ls -la ..` gave us the following output:
```
total 48 
drwxr-xr-x 7 student student 4096 Nov 20 12:38 . 
drwxr-xr-x 1 root        996 4096 Oct 29 14:37 .. 
-rwxr-xr-x 1 student student  237 Nov  7 14:12 .bash_logout 
-rwxr-xr-x 1 student student 3808 Nov  7 14:12 .bashrc 
drwxr-xr-x 3 student student 4096 Nov  6 12:23 .cache 
drwxr-xr-x 3 student student 4096 Nov  6 13:26 .config 
drwxr-xr-x 5 student student 4096 Nov  6 12:23 .local 
-rwxr-xr-x 1 student student  807 Feb 25  2020 .profile 
-rwxr-xr-x 1 student student    0 Nov  7 13:19 .selected_editor 
drwxr-xr-x 2 student student 4096 Nov 10 17:36 .ssh 
-rwxr-xr-x 1 student student    0 Nov  7 10:59 .sudo_as_admin_successful drwxr-xr-x 7 student student 4096 Nov 20 12:56 MySecretNotes-security-handin 
-rwxr-xr-x 1 student student  816 Nov  7 10:59 logbook.txt 
```

The `.ssh` folder suggested we could gain access via ssh if we authorized our own ssh keys. We did this using `echo "<ssh pub key>" >> ../.ssh/authorized_keys`. This meant we had straight ssh access to the server.

## Privilege Escalation

After gaining access to the server using ssh, we played around with the server looking for different files that we could access and looked at the web applications code, which did not give us much information. Therefore we instead used `sudo -l` to figure out what commands we had access to run with sudo on our `student`-user, which led us to a hidden file named `exam.py` in the `/etc/`-folder. `exam.py` would use an environment-variable `CMD` which would have its text shifted by a random integer between -12 and 12 and then executed on the command line. Running this python file with `sudo python3 exam.py` with the `CMD`-variable set would run the value of the variable on the command line as root. So to gain access to `root` we set the environment variable to `/bin/bash` and ran the file manually until it shifted by 0 and gave us a root shell. This could also easily have been done using a python script and taking advantage of the way seeding works in python, but this was not necessary as the range of the random integer was so small. 

## Security Goal Violations

During the information-gathering phase, we found a hidden input field that allowed execution of arbitrary commands on the server. This phase directly compromised **Confidentiality** and **Privacy**, as we accessed hidden elements not intended for user view. Additionally, the ability to run server-side commands violated **Access Control** since unauthorized commands were allowed through the input field.

By exploiting the hidden input field to execute shell commands (`whoami`) and eventually adding SSH keys to `authorized_keys`, several security goals were compromised:
- **Confidentiality**: We gained unauthorized access to sensitive information by listing users on the system.
- **Access Control**: We bypassed intended restrictions by exploiting the hidden field, which should have had proper access constraints.
- **Authentication**: Adding an SSH key without proper validation or user authentication means we bypassed security mechanisms to authenticate ourselves as a legitimate user.

After gaining initial access as the `student` user, we escalated our privileges to `root` by exploiting a vulnerability in the `exam.py` file and again several security goals were compromised:
- **Integrity**: Modifying the environment variable `CMD` to execute arbitrary shell commands compromised the integrity of the system, allowing unauthorized code execution.
- **Accountability**: By exploiting root privileges, the actions taken were not properly logged or traceable to the original `student` user, undermining the accountability of user actions.
- **Access Control**: Elevating to `root` compromised the access control policy, allowing us to perform actions restricted to super users.

To maintain access, we created a new user with superuser privileges, ensuring future unrestricted access. Thereby we violated:
- **Confidentiality**: By adding a backdoor user, we ensured that sensitive information could be continuously accessed without detection.
- **Access Control**: Creating a new superuser (`attacker`) directly violated access control policies as it circumvented standard authorization and user verification processes.
- **Non-repudiation**: By modifying `/etc/sudoers` to allow `NOPASSWD` for the `attacker` user, actions performed by this user would not be easily traceable or deniable, affecting non-repudiation.


## Maintaining Access

After we got root access we wanted to make sure that we maintained access. We did this by running the following commands: `sudo useradd attacker` which uses super user privileges to create a new user called `attacker`, `sudo passwd attacker` which creates a password for the user of attacker that only we will know,`sudo usermod -aG sudo attacker` which adds the user `attacker` to the group `sudo` such that attacker now have the privileges of the sudo group

After these steps we used the command
`sudo visudo`
to open `/etc/sudoers` where we added the following line:
`attacker ALL=(ALL:ALL) NOPASSWD: ALL`
which ensures that we can use sudo commands on the user attacker without having to write root’s password.

We could theoretically have done much more to keep out the original owners and make sure we were the only ones with root access, but this seemed excessive considering the nature of the assignment.
