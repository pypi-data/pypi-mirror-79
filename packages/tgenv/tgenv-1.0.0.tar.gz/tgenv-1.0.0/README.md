# Introduction

tgenv is a Python CLI tool for managing [terragrunt](https://github.com/gruntwork-io/terragrunt/) versions.

If you have any questions, any remarks or even bugs, feel free to open an issue.

There is currently no or will ever be any support for windows.

## Prerequisites

You need python3.8 installed.

## Installation

```bash
pip install tgenv
```

## Usage

- Show available versions
    ```bash
    tgenv list-remote
    ```
- Install a version
  ```bash
  tgenv install v0.24.4
  ```
- Use an installed version
  ```bash
  tgenv use v0.24.4
  ```
- Show installed version
  ```bash
  tgenv list
  ```
- Remove installed versions
  ```bash
  tgenv remove v0.24.4
  ```
- Remove all versions
  ```bash
  tgenv purge
  ```

# Licensing
This program is published under the GPL-3.0-only. See the `LICENSE` file.
