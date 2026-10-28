# Pending GitHub Repository Setup

GitHub remote creation is pending because the GitHub CLI (`gh`) is not installed in the current environment. No remote repository has been created or pushed.

When the project is ready for an authenticated GitHub action:

1. Sign in to [GitHub](https://github.com/) in the student's browser.
2. Select the **+** menu in the upper-right corner and choose **New repository**.
3. Set **Owner** to the student's own GitHub account.
4. Enter a new repository name, such as `cse4095-hangman-web-game`.
5. Choose the visibility required by the course or make it public for grader access.
6. Leave **Add a README**, **Add .gitignore**, and **Choose a license** unselected because those files already exist locally.
7. Select **Create repository**.
8. Copy the repository's HTTPS or SSH URL without sharing credentials in chat.
9. From this local repository, add that exact URL as `origin` and verify it with `git remote -v`.
10. Push only when the user requests the publishing phase, then verify the remote branch and commit rather than assuming the push succeeded.
