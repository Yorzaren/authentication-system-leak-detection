# Development

* Get XAMPP for Linux 8.2.0 from <https://www.apachefriends.org/download.html>
* To reopen the panel: `sudo /opt/lampp/manager-linux-x64.run`
* Copy the folder called `web` into `/opt/lampp/htdocs`
  * Get a copy of the main repo:
    * `git clone https://github.com/Yorzaren/authentication-system-leak-detection.git`
  * Move into the repository folder:
    * `cd authentication-system-leak-detection`
  * Copy the code to the website:
    * `sudo cp web -r /opt/lampp/htdocs`
  * Site should be live at `localhost/web`