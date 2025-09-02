#Update Aug 2025

Clock stopped working - this was due to an error in the high tide formatting. 

To run it, connect to a terminal and write
'''ssh tony@raspberrypi.local'''

get into the right directory - below you can make the directory, for now you can just find it

'''Making the GIT repository
tony@raspberrypi:~ $ ls
Bookshelf  Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos
tony@raspberrypi:~ $ cd Documents
tony@raspberrypi:~/Documents $ ls
tony@raspberrypi:~/Documents $ mkdir tideclock
tony@raspberrypi:~/Documents $ ls tideclock
tony@raspberrypi:~/Documents $ cd tideclock
tony@raspberrypi:~/Documents/tideclock $ git clone https://https://github.com/philipbates/tideclock'''

When in the correct directory, here is how to sync to the github
'''git stath: needed because otherwise you get sync errors.
git fetch: Retrieves updates from the remote repository.
git merge: Merges the changes into the current branch.
'''

Then, you need to re-start the timer service
'''
Reload systemd:
'''
sudo systemctl daemon-reload
'''
Enable the service to start at boot:
'''
sudo systemctl enable tideclock.timer
'''



