# Donno

A simple note-take CLI application.

## Usage

```
don add        # create a new note
don list       # list existing notes
don search nim thunder    # search notes contains "nim" and "thunder"
don edit 3     # edit note #3 in note list or searching results
don delete 3   # delete note #3 in note list or searching results
don backup     # backup notes to remote repository
don restore    # restore notes from remote repository
don preview 3  # preview note #3 in console editor
don phtml 3    # preview note #3 in browser
don ads -n nim -t config -c compile  # search notes which "nim" in its title, "config" in tags and "compile" in contents
don ads -r "[nim|thunder]"  # search notes contains "nim" or "thunder"
don publish    # publish notes to blog
```

Note: `phtml` command depends on pandoc and a browser.

## Configuration

File path: ~/.config/donno/donno.conf

### General

* editor: which editor to use to create/update note, default: `nvim`
* notebook: current notebook name, no default value
* base_dir: root folder of donno data files, default: ~/.donno
* vimrc_home: when editor is vim or neovim, the configuration home folder, default: ~/.config/nvim
* resource_dir: folder name (in base_dir) to store attachments of notes, default: resources

### Blog

* url: blog url
* publish_cmd: command to publish note to blog

## Roadmap

1. Basic note-taking functions: add, delete, list, search, view, update notes

1. Configuration module: see [Configuration](#configuration);

1. Support adding attachments into notes, espeicially images

1. Preview: render markdown notes to HTML and previewed in browser

1. Synchronize notes between hosts (based on VCS, such as git)

1. Import/Export from/to other open source note-taking apps, such as [Joplin]()

1. Advanced search function: search by title, tag, notebook and content

1. Search with regular expression;

1. Basic publishing module: publish to blog, such as github.io

1. Advanced publishing function: publish specific note, or notes in specific notebook

