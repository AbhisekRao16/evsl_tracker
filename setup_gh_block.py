from prefect_github import GitHubRepository

GitHubRepository(
    name="my-gh-block",
    repository="https://github.com/AbhisekRao16/evsl_tracker",  # your repo
    reference="master",  # branch name
).save("my-gh-block", overwrite=True)
