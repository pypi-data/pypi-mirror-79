# muscle

The Muse On-Demand CLI Tool 

## Requirement
1. Have [pipenv installed](https://pypi.org/project/pipenv/)
2. Run `pipenv install` once in the current directory to ensure the availability of dependencies 
3. Set *environment variable* `USER_TOKEN` with your JWT token (alternatively, set it in the `--token` option of each command)

## Usage
`./muscle --help`
```
Usage: muscle [OPTIONS] COMMAND [ARGS]...

Options:
  --token TEXT  Overrides environment variable USER_TOKEN
  --help        Show this message and exit.

Commands:
  analyze  (--help for subcommand usage)
  status   (--help for subcommand usage)
  results   (--help for subcommand usage)
```
`./muscle analyze --help`
```
Usage: muscle analyze [OPTIONS] REPO

Options:
  --branch TEXT  The branch to analyze, default to 'master'
  --commit TEXT  Hash of the commit to analyze, overrides --branch
  --help         Show this message and exit.
```
`./muscle status --help `
```
Usage: muscle status [OPTIONS] [JOB_ID]...

Options:
  --help  Show this message and exit.
```
`./muscle result --help`
```
Usage: muscle results [OPTIONS] [JOB_ID]...

Options:
  --help  Show this message and exit.
```

## Examples:
* Run analysis on a branch: `USER_TOKEN=MY_SECRET_JWT muscle analyze https://github.com/tommd/libacvp --branch master`
* Run analysis on a commit: `muscle --token MY_SECRET_JWT analyze https://github.com/tommd/libacvp --commit h1a2s3h`
* Get analysis status `muscle --token MY_SECRET_JWT status jobID`
* Get analysis results `USER_TOKEN=MY_SECRET_JWT muscle results jobID1 jobID2 jobID3`