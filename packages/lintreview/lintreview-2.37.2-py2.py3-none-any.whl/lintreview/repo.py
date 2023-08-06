import lintreview.github as github
import logging
import json

log = logging.getLogger(__name__)


class GithubRepository(object):
    """Abstracting wrapper for the
    various interactions we have with github.

    This will make swapping in other hosting systems
    a tiny bit easier in the future.
    """
    repo = None

    def __init__(self, config, user, repo_name):
        self.config = config
        self.user = user
        self.repo_name = repo_name

    def repository(self):
        """Get the underlying repository model
        """
        if not self.repo:
            self.repo = github.get_repository(
                self.config,
                self.user,
                self.repo_name)
        return self.repo

    def pull_request(self, number):
        """Get a pull request by number.
        """
        pull = self.repository().pull_request(number)
        return GithubPullRequest(pull)

    def ensure_label(self, label):
        """Create label if it doesn't exist yet
        """
        repo = self.repository()
        if not repo.label(label):
            repo.create_label(
                name=label,
                color="bfe5bf",  # a nice light green
            )

    def create_status(self, sha, state, description):
        """Create a commit status
        """
        context = self.config.get('APP_NAME', 'lintreview')
        repo = self.repository()
        repo.create_status(
            sha,
            state,
            None,
            description,
            context)

    def update_checkrun(self, run_id, checkrun):
        repo = self.repository()
        url = repo._build_url('check-runs', run_id, base_url=repo._api)
        data = json.dumps(checkrun)
        res = repo._patch(
            url,
            data=data,
            headers=github.CHECKSUITE_HEADER)
        return repo._json(res, 200)


class GithubPullRequest(object):
    """Abstract the underlying github models.
    This makes other code simpler, and enables
    the ability to add other hosting services later.
    """

    def __init__(self, pull_request):
        self.pull = pull_request

    @property
    def display_name(self):
        data = self.pull.as_dict()
        return u'%s/pull/%s' % (data['head']['repo']['full_name'],
                                data['number'])

    @property
    def number(self):
        return self.pull.number

    @property
    def head(self):
        data = self.pull.as_dict()
        return data['head']['sha']

    @property
    def base(self):
        data = self.pull.as_dict()
        return data['base']['sha']

    @property
    def clone_url(self):
        """Get the clone url

        If this pull is from a private fork, we read
        from the base repository to get around permission
        issues where github applications don't have access
        to forked repositories.
        """
        data = self.pull.as_dict()
        if self.from_private_fork:
            return data['base']['repo']['clone_url']
        return data['head']['repo']['clone_url']

    @property
    def target_branch(self):
        data = self.pull.as_dict()
        return data['base']['ref']

    @property
    def head_branch(self):
        """Get the head branch name

        If the pull request is from a private fork, the
        head branch will be pull ref so we can read it
        from the base repo.
        """
        data = self.pull.as_dict()
        if self.from_private_fork:
            return u'refs/pull/{}/head'.format(self.number)
        return data['head']['ref']

    @property
    def from_private_fork(self):
        data = self.pull.as_dict()
        head = data['head']['repo']
        base = data['base']['repo']

        # If the base and head are the same its not a fork
        if base['full_name'] == head['full_name']:
            return False
        # Private head repo or forked head counts
        return head['private'] and head['fork']

    @property
    def maintainer_can_modify(self):
        """Whether or not the maintainers can update this pull
        request.

        Maintainers can always edit pulls from the head repo.
        """
        data = self.pull.as_dict()
        if data['base']['repo']['full_name'] == \
                data['head']['repo']['full_name']:
            return True
        return data['maintainer_can_modify']

    def commits(self):
        return self.pull.commits()

    def review_comments(self):
        return self.pull.review_comments()

    def files(self):
        return list(self.pull.files())

    def remove_label(self, label_name):
        issue = self.pull.issue()
        labels = issue.labels()
        if not any(label_name == label.name for label in labels):
            return
        log.debug("Removing issue label '%s'", label_name)
        issue.remove_label(label_name)

    def add_label(self, label_name):
        issue = self.pull.issue()
        issue.add_labels(label_name)

    def create_comment(self, body):
        self.pull.create_comment(body)

    def create_review(self, review):
        url = self.pull._build_url('reviews', base_url=self.pull._api)
        self.pull._json(self.pull._post(url, data=review), 200)

    def create_review_comment(self, body, commit_id, path, position):
        self.pull.create_review_comment(body, commit_id, path, position)
