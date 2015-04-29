# jekyllclient

An easy jekyllclient to manager your posts in your local host.

## How to use

That's easy to use once you configure it :) !

All the configure items are in the conf/blog.conf and it easy to configure !

```conf
[site]
base = <the root path of your blog>
posts = <the posts path, default '_posts'>
username = <your usename>
```

Once you finish the work above, Let's go!

Don't know show to work ? Run './blog help' to show help messages:

```
usage: blog [--version] [--debug] <subcommand> ...

A shell to manager blog

positional arguments:
  <subcommand>
    create         Create a new post.
    delete         Delete specified post.
    list           List all the posts.
    ls             Equivalent to list.
    show           Read a Post
    bash-completion
    help           Display help about this program or one of its subcomands.

optional arguments:
  --version        show program's version number and exit
  --debug          Print debugging output

See "blog help COMMAND" for help on a specific command.
```

Just as shown above, you can run `blog help COMMAND` for help on a specific command.

Want to list all your posts ? Just run `./blog list`:
```
+-------------------------------+----------+------------+
| title                         | filetype | date       |
+-------------------------------+----------+------------+
| scriptnote                    | markdown | 2015-04-26 |
| HowToInstallJekyll            | markdown | 2015-04-26 |
| java-concurrency              | markdown | 2014-09-20 |
+-------------------------------+----------+------------+
```

A Pretty table ? Thanks to `python prettytab`.

If you want to show more details on the posts, run `./blog list -d`:
```
+---------------------------------+------------+----------+--------+------------------------------+----------+----------+
| title                           | date       | category | layout | tags                         | filetype | comments |
+---------------------------------+------------+----------+--------+------------------------------+----------+----------+
| HelloWorld1                     | 2015-03-18 | linux    | post   | bash                         | markdown | true     |
| HelloWrold2                     | 2014-11-30 | linux    | post   | c                            | markdown | true     |
+---------------------------------+------------+----------+--------+------------------------------+----------+----------+
```

You'd like to show the contend of specified post ? Just run `./blog show -t HelloWorld1`.

You can also set your style to read the post, choice from `cat, less, more` styles.

Once you get a new fresh idea and want to write down to your blog, run `blog create`, 
this smart script will set your metedata automatically, and call your editor depend on your EDITOR environment

Let's record our life by jekyll from now!

## Issure & PR

Yes, welcome! 


