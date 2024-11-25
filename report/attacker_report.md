# Security Mini Project - Attacking

- [Security Mini Project - Attacking](#security-mini-project---attacking)
  - [Information Gathering](#information-gathering)
  - [Initial Access](#initial-access)
  - [Privilege Escalation](#privilege-escalation)
  - [Security Goal Violations](#security-goal-violations)
  - [Maintaining Access](#maintaining-access)

## Information Gathering

## Initial Access

After figuring out that the input field’s translation was run on the server as a shell-command, we tried figuring out what user these commands would be run on, which was `student`. After this we tried figuring out a way for us to gain access to the server without having to translate our commands to `Brainfuck` first. For this, we generated ssh-keys and added them to `authorized_keys` so that we could ssh into the server without having to provide a password for `student`.

## Privilege Escalation

After gaining access to the server using ssh, we played around with the server looking for different files that we could access and looked at the web applications code, which did not give us much information. Therefore we instead used `sudo -l` to figure out what commands we had access to on our `student`-user, which led us to a hidden file named `exam.py` which we were able to run with root-access. `exam.py` would use an environment-variable `CMD` which would have its text shifted with a random number and then executed via `root`. So to gain access to `root` we would have to somehow have the text shifted by 0 and run a command that would open a new shell for us: `/bin/bash`. From there we just ran `exam.py` until it hit 0 and we then had a shell running with `root`-access.

## Security Goal Violations

## Maintaining Access

After we got root access we wanted to make sure that we maintained access. We did this by running the following commands:
`sudo useradd attacker`
This commands uses super user privileges to create a new user called attacker with super user access
`sudo passwd attacker`
This command creates a password for the user of attacker that only we will know
`sudo usermod -aG sudo attacker`
Which adds the user attacker to the group sudo such that attacker now have the privileges of the sudo group

After these steps we used the command
`sudo visudo`
to open /etc/sudoers where we added the following line:
`attacker ALL=(ALL:ALL) NOPASSWD: ALL`
which ensures that we can use sudo commands on the user attacker without having to write root’s password
