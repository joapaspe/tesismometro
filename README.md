# Tesismometro
Tesismometro (Thesis-O-meter) is a project to keep track of your Thesis writing by computing daily statistics.
It seeks several objectives:

- Track the number of words, pages, equations during the writing. Having a control of a quantitative work every day help
to achieve the goals and milestones during this (sometimes tedious) process.
- Motivate the writing. Similar to other gamification techniques, seeing your progress regarding graphs and
comparison between colleagues.
- Competitive with other members. It sounds a bit evil, but with (a healthy) competition with your colleagues checking
who can advance faster and do progress.

It provides nice graphs and progress during your thesis, as well as a ranking with your colleagues.

## What do I need?
Tesismometro is developed as a web application which stores the progress of the Ph.D. students.
The application is meant to run with the Google AppEngine SDK, and a working version could be found in [tesismometro.appspot.com/](tesismometro.appspot.com) 

## Installation and local run
Assuming you want to try it you can run it locally, you would need:
 - Python 2.7
 - The Google AppEngine SDK ([https://cloud.google.com/appengine/docs](here))
 - A web browser. (who doesn't?)
 
### Running locally
 
 First, you clone the repository in the `$INSTALLED_DIR`.
 With the installed appengine run the following command line:
 ```
 /usr/bin/python2.7 $APP_ENGINE_DIR/google_appengine/dev_appserver.py --host 127.0.0.1 $INSTALLED_DIR
 ```
 Run a browser and open http://localhost:8000
 
 That's all :)
 
## Creating users
Luckily we have an admin interface which allows adding a user to the system.
$SERVER/admin
For production, it is required a Google ID (mainly a Gmail account) since the user authentication is done
 by this service.
 So a user is added with a name and the underlying email (ID).
 
## I have a user I want to update my stats.
Well, this is kind of tricky. The *user's interface* shows how to upload (and update your data).
 
There is a bash script that does all the counting and updates it to the server (as explained in the user's area).
But, you need
- A Linux/Unix terminal.
- texcount
- curl
- Your thesis in latex

If it is not the case, you can compute your stats (by hand or your script), and send a POST request to
$SERVER/post, like
```
curl --data "name=$USER&words=$words&equations_inline=$inlines&equations=$equations&figures=$figures&cites=$cites&pages=$pages&token=$TOKEN"\
 $SERVER/post
```
