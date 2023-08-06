import os
import asana


class AsanaWrapper:
    def __init__(self, token, workspace):
        self.client = asana.Client.access_token(token)
        self.workspace = workspace

    def comment_task(self, task_id, comment):
        t_gid = self._find_task(task_id)
        self._create_story(t_gid, comment)

    def _find_task(self, task_id):
        result = self.client.typeahead.typeahead_for_workspace(
            self.workspace,
            {
                'resource_type': 'task',
                'query': task_id,
                'count': 1
            }
        )
        tasks = list(result)
        if tasks:
            return tasks[0]['gid']

    def _create_story(self, task_gid, html_text):
        result = self.client.stories.create_story_for_task(
            task_gid,
            {
                'html_text': html_text
            }
        )
