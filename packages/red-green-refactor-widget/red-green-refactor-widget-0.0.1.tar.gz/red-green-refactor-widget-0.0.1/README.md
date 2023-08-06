# Red-Green-Refactor Widget

When you are learning to follow the _red-green-refactor_ workflow, this app
will help you to keep track of your progress by reminding you of which stage
of the workflow you are right now and which actions you need to undertake
before proceeding to the next stage. See **Usage** section for details.

# Prerequisites

The package depends on [`pyqtkeybind`](https://github.com/codito/pyqtkeybind),
which, at the time of writing this readme (version 0.0.6), has support for
Windows and Linux only.

## Dependencies

* PyQt5
* pyqtkeybind

If you are installing it through `pip`, all necessary python dependencies
are going to be pulled in automatically. Depending on your platform, you
might need to install Qt5 binary packages.

# Installation

From `pip`:
```
$ pip install red-green-refactor-widget
```

# Usage

To launch the app, simply run the following command from terminal:
```
$ red-green-refactor-widget
```
After you launched the app, you should see a small window. It displays
a stage of the red-green-refactor workflow.
When you finished a stage, press _Alt-F12_, and the widget will
change to the next stage of the workflow.
By default, the window is created with the always-on-top flag on,
and the hotkey is global, thus you don't need to worry about keeping
the window in focus.

# License

Distributed under MIT license. See `LICENSE` file for more information.
