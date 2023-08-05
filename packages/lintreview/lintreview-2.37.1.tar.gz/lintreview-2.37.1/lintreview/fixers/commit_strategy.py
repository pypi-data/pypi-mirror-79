from lintreview.fixers.error import WorkflowError
import lintreview.git as git
import logging

log = logging.getLogger(__name__)


class CommitStrategy(object):
    """Fixer strategy for updating the pull request branch in place.
    Appends a commit to the branch that created the pull request.
    """

    def __init__(self, context):
        self.path = context['repo_path']
        self.author_name = context['author_name']
        self.author_email = context['author_email']
        self.pull_request = context['pull_request']

    def execute(self, diffs):
        if not self.pull_request.maintainer_can_modify:
            msg = ('Cannot apply automatic fixing, '
                   'as this pull request cannot be '
                   'modified by maintainers.')
            raise WorkflowError(msg)
        if self.pull_request.from_private_fork:
            msg = ('Cannot apply automatic fixing, '
                   'as this pull request comes from a private fork.')
            raise WorkflowError(msg)

        git.create_branch(self.path, 'stylefixes')
        git.checkout(self.path, 'stylefixes')
        for diff in diffs:
            git.apply_cached(self.path, diff.as_diff())

        author = u'{} <{}>'.format(self.author_name, self.author_email)
        remote_branch = self.pull_request.head_branch

        git.commit(self.path, author, 'Fixing style errors.')
        try:
            git.push(self.path, 'origin', u'stylefixes:{}'.format(remote_branch))
        except IOError as err:
            message = str(err)
            log.debug(message)
            if '(permission denied)' in message:
                raise WorkflowError(
                    'Could not push fix commit because permission was denied. '
                    'This can happen when pull requests are submitted from forks.'
                )
            if '[remote rejected]' in message:
                raise WorkflowError('Could not push fix commit because it was not a fast-forward.')
            raise err
