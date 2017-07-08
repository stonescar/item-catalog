# Item catalog app

An app that keeps track of, and categorizes, various items. Users can log in with Facebook, Google or GitHub to add, edit or delete categories or items. This project is part of my Full Stack Nanodegree at[http://udacity.com](Udacity.com).

## Prerequisits

It is recommended to run this app using a VM. To set up this app using a VM, install the following software and follow the instructions below

* [Python2.7](http://python.org)
* [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)
* [GIT](https://git-scm.com/downloads) _(Recommended for Windows)_

## Installation

1. Make sure you have installed all software listed above
2. Clone this repository to desired folder<br>
    `git clone https://github.com/stonescar/item-catalog`
3. Boot the VM by running `vagrant up`
4. When the is ready, log in with `vagrant ssh`
5. cd to the shared folder with `cd /vagrant`
6. To create the database run<br>
    `python modules/setup/database.py`
7. Run `python run.py` to start the server
8. The application is now available at http://localhost:5000

## Using the app

The Item Catalog stores and categorizes any items you want. The categories is allways available in the panel on the left side. On the front page the 10 most recently added items are listed.

By logging in with Google, Facebook or Github you can add edit or delete categories and items. Categories can only be edited or deleted by the user who created the category. The same goes for items, but the creator of a category can allways edit or delete items in his/her category, even if he/she didn't create that item.

When adding a new item, you can add title, description and URL to a picture. If you check the box "Get random image from google", a random image will be linked to the item based on the item title.
    

## Licencing
This project is licensed under the [MIT License](LICENSE)